import json
import re
from typing import List, Dict, Any, Optional

from backend.config import settings
from backend.database import get_conn

# === Abstraction: External API Client ===

class AnthropicClient:
    """Wrapper for Anthropic API to decouple from business logic."""
    def __init__(self, api_key: str):
        import anthropic
        self._client = anthropic.Anthropic(api_key=api_key)

    def create_message(
        self,
        model: str,
        max_tokens: int,
        messages: List[Dict[str, Any]]
    ) -> Any:
        return self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
        )

    def create_batch(self, requests: List[Dict[str, Any]]) -> Any:
        return self._client.messages.batches.create(requests=requests)

    def retrieve_batch(self, batch_id: str) -> Any:
        return self._client.messages.batches.retrieve(batch_id)

    def get_batch_results(self, batch_id: str):
        return self._client.messages.batches.results(batch_id)

# === Abstraction: Configuration Constants ===

MODEL = "claude-haiku-4-5-20251001"
BATCH_SIZE = 50
MAX_OUTPUT_TOKENS = 4096

# Comprehensive keyword mappings for extraction
# ticker, company name, short name, CEO, key products, subsidiaries
TICKER_KEYWORDS: Dict[str, List[str]] = {
    "BABA": ["alibaba", "ali baba", "baba", "daniel zhang", "joe tsai",
             "taobao", "tmall", "alipay", "ant group", "alicloud",
             "aliyun", "cainiao", "lazada", "ele.me"],
    "AAPL": ["apple", "aapl", "tim cook", "iphone", "ipad", "macbook",
             "apple watch", "vision pro", "app store", "ios", "macos"],
    "TSLA": ["tesla", "tsla", "elon musk", "model 3", "model y",
             "model s", "model x", "cybertruck", "gigafactory",
             "supercharger", "autopilot", "full self-driving", "fsd"],
    "NVDA": ["nvidia", "nvda", "jensen huang", "geforce", "rtx",
             "cuda", "a100", "h100", "h200", "b100", "b200",
             "dgx", "drive", "omniverse", "tensorrt"],
    "GLD": ["spdr gold", "gld", "gold trust", "gold etf", "gold shares"],
    "MSFT": ["microsoft", "msft", "satya nadella", "windows", "azure",
             "office 365", "xbox", "linkedin", "github", "copilot"],
    "GOOGL": ["google", "alphabet", "googl", "goog", "sundar pichai",
              "youtube", "waymo", "deepmind", "gemini", "android",
              "google cloud", "pixel"],
    "AMZN": ["amazon", "amzn", "andy jassy", "aws", "prime",
             "alexa", "kindle", "whole foods"],
    "META": ["meta platforms", "meta", "facebook", "zuckerberg",
             "instagram", "whatsapp", "threads", "oculus", "quest"],
    "AMD":  ["amd", "advanced micro", "lisa su", "radeon", "ryzen",
             "epyc", "xilinx", "instinct"],
}

EXTRACT_THRESHOLD = 500

# === Domain: Keyword Management ===

def _get_keywords(symbol: str) -> List[str]:
    """Get all keywords for a ticker. Falls back to just the symbol."""
    kws = [symbol.lower()]
    kws.extend(TICKER_KEYWORDS.get(symbol, []))
    return kws

# === Domain: Text Extraction ===

def _extract_relevant_text(description: str, symbol: str) -> str:
    """For long descriptions, extract only sentences mentioning the company.

    Short descriptions (<500 chars) are returned in full.
    Long descriptions are filtered to company-relevant sentences + 1 neighbor.
    """
    if not description:
        return ""

    desc = description.strip()
    if len(desc) < EXTRACT_THRESHOLD:
        return desc

    keywords = _get_keywords(symbol)
    sentences = re.split(r'(?<=[.!?])\s+', desc)

    # Find sentences with keyword matches
    relevant: set = set()
    for i, sent in enumerate(sentences):
        lower = sent.lower()
        if any(kw in lower for kw in keywords):
            # Keep this sentence + 1 before + 1 after for context
            for j in range(max(0, i - 1), min(len(sentences), i + 2)):
                relevant.add(j)

    if not relevant:
        # No keyword match — just return first 2 sentences
        return " ".join(sentences[:2])

    return " ".join(sentences[i] for i in sorted(relevant))

# === Domain: Prompt Construction ===

def _build_batch_prompt(symbol: str, articles: List[Dict[str, Any]]) -> str:
    """Build a single prompt containing up to 50 articles."""
    lines = []
    for i, art in enumerate(articles):
        extract = _extract_relevant_text(art.get("description") or "", symbol)
        lines.append(f"[{i}] {art['title']}")
        if extract:
            lines.append(f"  > {extract}")

    return f"""Rate these {len(articles)} articles for {symbol}. Return JSON array only.

{chr(10).join(lines)}

Format: [{{"i":0,"r":"y"|"n","s":"+"|"-"|"0","e":"summary","u":"up reason","d":"down reason"}}]
r: "y" = article specifically discusses {symbol}, "n" = irrelevant/brief mention
s: "+" positive, "-" negative, "0" neutral
e: 10-word summary of what happened (empty if irrelevant)
u: why this could push {symbol} stock UP, e.g. "strong earnings beat expectations" (empty if none or irrelevant)
d: why this could push {symbol} stock DOWN, e.g. "antitrust lawsuit threatens App Store revenue" (empty if none or irrelevant)
JSON:"""

# === Domain: Data Access ===

def _get_pending_articles(symbol: str, limit: int = 10000) -> List[Dict[str, Any]]:
    """Get articles that passed Layer 0 but haven't been processed by Layer 1."""
    conn = get_conn()
    try:
        rows = conn.execute(
            """SELECT nr.id, nr.title, nr.description
               FROM news_raw nr
               JOIN layer0_results l0 ON nr.id = l0.news_id AND l0.symbol = ?
               WHERE l0.passed = 1
               AND nr.id NOT IN (
                   SELECT news_id FROM layer1_results WHERE symbol = ?
               )
               LIMIT ?""",
            (symbol, symbol, limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

# === Domain: Result Persistence ===

def _save_layer1_results(
    conn: Any,
    symbol: str,
    articles: List[Dict[str, Any]],
    results: List[Dict[str, Any]]
) -> Dict[str, int]:
    """Save processed results to database and compute stats."""
    stats = {"processed": 0, "relevant": 0, "irrelevant": 0, "errors": 0}

    for item in results:
        idx = item.get("i")
        if idx is None or idx >= len(articles):
            stats["errors"] += 1
            continue

        art = articles[idx]
        is_relevant = item.get("r") in ("y", "relevant")
        relevance = "relevant" if is_relevant else "irrelevant"
        raw_s = item.get("s", "0")
        sentiment = {"+": "positive", "-": "negative"}.get(raw_s, "neutral")

        conn.execute(
            """INSERT OR REPLACE INTO layer1_results
               (news_id, symbol, relevance, key_discussion, sentiment,
                reason_growth, reason_decrease)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                art["id"],
                symbol,
                relevance,
                item.get("e", ""),
                sentiment,
                item.get("u", ""),
                item.get("d", ""),
            ),
        )
        stats["processed"] += 1
        if is_relevant:
            stats["relevant"] += 1
        else:
            stats["irrelevant"] += 1

    return stats

# === Domain: Batch Processing ===

def _process_batch_group(
    symbol: str,
    articles: List[Dict[str, Any]],
    client: Optional[AnthropicClient] = None
) -> Dict[str, int]:
    """Process a group of up to 50 articles in a single API call."""
    api_client = client or AnthropicClient(api_key=settings.anthropic_api_key)
    conn = get_conn()

    stats = {"processed": 0, "relevant": 0, "irrelevant": 0, "errors": 0}

    prompt = _build_batch_prompt(symbol, articles)

    try:
        message = api_client.create_message(
            model=MODEL,
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        text = message.content[0].text if message.content else "[]"

        # Parse JSON array
        start = text.find("[")
        end = text.rfind("]") + 1
        if start < 0 or end <= start:
            stats["errors"] = len(articles)
            return stats

        results = json.loads(text[start:end])
        stats.update(_save_layer1_results(conn, symbol, articles, results))

    except (json.JSONDecodeError, KeyError) as e:
        stats["errors"] = len(articles)
        print(f"Batch error for {symbol}: {e}")

    conn.commit()
    conn.close()
    return stats

# === Domain: Orchestration ===

def run_layer1(symbol: str, max_articles: int = 10000) -> Dict[str, Any]:
    """Run Layer 1 on all pending articles for a symbol.

    Processes in groups of 50 articles per API call.
    """
    articles = _get_pending_articles(symbol, limit=max_articles)
    if not articles:
        return {"status": "no_pending", "total": 0}

    total_stats = {
        "total": len(articles), "processed": 0, "relevant": 0,
        "irrelevant": 0, "errors": 0, "api_calls": 0,
    }

    for i in range(0, len(articles), BATCH_SIZE):
        chunk = articles[i : i + BATCH_SIZE]
        stats = _process_batch_group(symbol, chunk)

        total_stats["processed"] += stats["processed"]
        total_stats["relevant"] += stats["relevant"]
        total_stats["irrelevant"] += stats["irrelevant"]
        total_stats["errors"] += stats["errors"]
        total_stats["api_calls"] += 1

        print(f"  [{symbol}] Batch {total_stats['api_calls']}: "
              f"{stats['processed']}/{len(chunk)} ok, {stats['relevant']} relevant")

    return total_stats

# === Batch API Support ===

def submit_batch_api(symbol: str, articles: List[Dict[str, Any]]) -> str:
    """Submit to Anthropic Batch API for async processing."""
    client = AnthropicClient(api_key=settings.anthropic_api_key)

    requests = []
    for i in range(0, len(articles), BATCH_SIZE):
        chunk = articles[i : i + BATCH_SIZE]
        chunk_ids = "|".join(a["id"] for a in chunk)
        prompt = _build_batch_prompt(symbol, chunk)

        requests.append(
            {
                "custom_id": f"{symbol}|{i}|{chunk_ids}",
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_OUTPUT_TOKENS,
                    "messages": [{"role": "user", "content": prompt}],
                },
            }
        )

    batch = client.create_batch(requests=requests)

    conn = get_conn()
    try:
        conn.execute(
            """INSERT INTO batch_jobs (batch_id, symbol, status, total, created_at)
               VALUES (?, ?, ?, ?, datetime('now'))""",
            (batch.id, symbol, batch.processing_status, len(articles)),
        )
        conn.commit()
    finally:
        conn.close()
    return batch.id


def check_batch_status(batch_id: str) -> Dict[str, Any]:
    """Check the status of a batch job."""
    client = AnthropicClient(api_key=settings.anthropic_api_key)
    batch = client.retrieve_batch(batch_id)

    conn = get_conn()
    try:
        conn.execute(
            "UPDATE batch_jobs SET status = ? WHERE batch_id = ?",
            (batch.processing_status, batch_id),
        )
        conn.commit()
    finally:
        conn.close()

    return {
        "batch_id": batch.id,
        "status": batch.processing_status,
        "request_counts": {
            "processing": batch.request_counts.processing,
            "succeeded": batch.request_counts.succeeded,
            "errored": batch.request_counts.errored,
            "canceled": batch.request_counts.canceled,
            "expired": batch.request_counts.expired,
        },
    }


def collect_batch_results(batch_id: str) -> Dict[str, int]:
    """Collect results from a completed batch API job."""
    client = AnthropicClient(api_key=settings.anthropic_api_key)
    conn = get_conn()

    stats = {"processed": 0, "relevant": 0, "irrelevant": 0, "errors": 0}

    for result in client.get_batch_results(batch_id):
        custom_id = result.custom_id
        parts = custom_id.split("|", 2)
        if len(parts) < 3:
            stats["errors"] += 1
            continue

        symbol = parts[0]
        article_ids = parts[2].split("|")

        if result.result.type != "succeeded":
            stats["errors"] += len(article_ids)
            continue

        message = result.result.message
        text = message.content[0].text if message.content else "[]"

        try:
            start = text.find("[")
            end = text.rfind("]") + 1
            if start < 0 or end <= start:
                stats["errors"] += len(article_ids)
                continue

            items = json.loads(text[start:end])
            articles = [{"id": aid} for aid in article_ids]
            stats.update(_save_layer1_results(conn, symbol, articles, items))

        except (json.JSONDecodeError, KeyError):
            stats["errors"] += len(article_ids)

    try:
        conn.execute(
            "UPDATE batch_jobs SET status = 'collected', finished_at = datetime('now') WHERE batch_id = ?",
            (batch_id,),
        )
        conn.commit()
    finally:
        conn.close()
    return stats
