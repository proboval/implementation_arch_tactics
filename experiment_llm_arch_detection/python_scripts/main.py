import csv
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
from llm_client import call_llm
from dotenv import load_dotenv


load_dotenv()
# -----------------------------
# CONFIG
# -----------------------------
INPUT_CSV = "artifacts/dataset_normalized.csv"
ARTIFACTS_DIR = Path("artifacts/repo_artifacts")
OUTPUT_CSV = "arch_detection_metrics/architecture_detection_results_minimax.csv"

MODEL = "minimax-m2.7:cloud"
TEMPERATURE = 0.2
TIMEOUT = 300
RETRIES = 2

# Если True — пропускать строки, для которых уже есть все 4 ответа
RESUME = True


ALLOWED_LABELS = [
    "script_based",
    "layered",
    "modular_monolith",
    "monolith",
]

SYSTEM_PROMPT = """You are a software architecture analysis assistant.

Your task is to infer the dominant architecture of a Python backend repository
from repository-level evidence.

You must classify the repository into exactly one of the following labels:
- script_based
- layered
- modular_monolith
- monolith

Definitions:
- script_based: repository is centered around a few scripts or entry files, with weak package structure and limited modular decomposition.
- layered: repository clearly separates concerns into layers such as api/controllers, services, repositories/data access, models, db, config.
- modular_monolith: repository is one deployable application but organized into multiple modules/packages with meaningful internal boundaries.
- monolith: repository is mostly one large tightly coupled codebase without clear layering or modular boundaries.

Return ONLY valid JSON with this schema:
{
  "architecture_label": "one of allowed labels",
  "confidence": 0.0,
  "evidence": ["short evidence 1", "short evidence 2", "short evidence 3"],
  "reasoning": "brief explanation"
}

Rules:
- confidence must be between 0 and 1
- do not use markdown
- do not add extra text before or after JSON
- rely only on the provided evidence
"""

# Поля, которые не надо включать в metrics prompt
EXCLUDED_METRIC_FIELDS = {
    "architecture_label",
    "architecture_label_raw",
    "architecture_variant",
    "architecture_label_source",
    "annotation_confidence",
    "annotation_notes",
    "repo_tree_path",
    "import_graph_path",
    "repo_signatures_path",
}


# -----------------------------
# HELPERS
# -----------------------------
def load_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore").strip()
    except Exception:
        return ""


def get_repo_artifact_paths(repo_full_name: str) -> Dict[str, Path]:
    owner, repo = repo_full_name.split("/", 1)
    repo_dir = ARTIFACTS_DIR / owner / repo

    return {
        "repo_tree": repo_dir / "repo_tree.txt",
        "import_graph": repo_dir / "import_graph.txt",
        "repo_signatures": repo_dir / "repo_signatures.txt",
    }


def compact_json_dumps(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def normalize_cell(v: str) -> str:
    if v is None:
        return ""
    return str(v).strip()


def format_metrics(row: Dict[str, str]) -> str:
    """
    Формирует текстовый блок с метриками из CSV.
    Берём все поля, кроме явно исключённых.
    """
    parts = []

    for key, value in row.items():
        if key in EXCLUDED_METRIC_FIELDS:
            continue

        if value is None:
            continue

        value_str = str(value).strip()
        if value_str == "":
            continue

        parts.append(f"- {key}: {value_str}")

    return "\n".join(parts)


def build_prompt_repo_tree(repo_tree: str) -> str:
    return f"""Determine the dominant repository architecture using only the repository file tree.

Allowed labels:
{", ".join(ALLOWED_LABELS)}

Repository tree:
{repo_tree}
"""


def build_prompt_repo_tree_imports(repo_tree: str, import_graph: str) -> str:
    return f"""Determine the dominant repository architecture using the repository file tree and internal import graph.

Allowed labels:
{", ".join(ALLOWED_LABELS)}

Repository tree:
{repo_tree}

Internal import graph:
{import_graph}
"""


def build_prompt_repo_tree_imports_signatures(
    repo_tree: str,
    import_graph: str,
    repo_signatures: str,
) -> str:
    return f"""Determine the dominant repository architecture using the repository file tree, internal import graph, and Python file signatures.

Allowed labels:
{", ".join(ALLOWED_LABELS)}

Repository tree:
{repo_tree}

Internal import graph:
{import_graph}

Python signatures:
{repo_signatures}
"""


def build_prompt_all(
    repo_tree: str,
    import_graph: str,
    repo_signatures: str,
    metrics_text: str,
) -> str:
    return f"""Determine the dominant repository architecture using:
1) repository file tree,
2) internal import graph,
3) Python signatures,
4) repository metrics.

Allowed labels:
{", ".join(ALLOWED_LABELS)}

Repository tree:
{repo_tree}

Internal import graph:
{import_graph}

Python signatures:
{repo_signatures}

Repository metrics:
{metrics_text}
"""


def try_parse_json(raw_text: str) -> Dict[str, object]:
    """
    Пытаемся распарсить JSON-ответ модели.
    Если не получается — возвращаем сырой ответ.
    """
    raw_text = (raw_text or "").strip()

    if not raw_text:
        return {
            "architecture_label": "",
            "confidence": "",
            "evidence": "",
            "reasoning": "",
            "raw": "",
            "parse_ok": False,
        }

    # 1. пробуем как есть
    try:
        obj = json.loads(raw_text)
        return {
            "architecture_label": obj.get("architecture_label", ""),
            "confidence": obj.get("confidence", ""),
            "evidence": json.dumps(obj.get("evidence", []), ensure_ascii=False),
            "reasoning": obj.get("reasoning", ""),
            "raw": raw_text,
            "parse_ok": True,
        }
    except Exception:
        pass

    # 2. пробуем вытащить JSON из текста
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = raw_text[start:end + 1]
        try:
            obj = json.loads(candidate)
            return {
                "architecture_label": obj.get("architecture_label", ""),
                "confidence": obj.get("confidence", ""),
                "evidence": json.dumps(obj.get("evidence", []), ensure_ascii=False),
                "reasoning": obj.get("reasoning", ""),
                "raw": raw_text,
                "parse_ok": True,
            }
        except Exception:
            pass

    return {
        "architecture_label": "",
        "confidence": "",
        "evidence": "",
        "reasoning": "",
        "raw": raw_text,
        "parse_ok": False,
    }


def call_variant(prompt: str) -> Dict[str, object]:
    raw = call_llm(
        prompt=prompt,
        model=MODEL,
        system_prompt=SYSTEM_PROMPT,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
        retries=RETRIES,
    )
    return try_parse_json(raw)


def already_done(row: Dict[str, str]) -> bool:
    needed = [
        "p1_raw",
        "p2_raw",
        "p3_raw",
        "p4_raw",
    ]
    return all(str(row.get(k, "")).strip() for k in needed)


# -----------------------------
# MAIN
# -----------------------------
def main():
    input_path = Path(INPUT_CSV)
    output_path = Path(OUTPUT_CSV)

    # читаем входной CSV
    with input_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if not fieldnames:
        raise ValueError("Input CSV has no header")

    if "repo_full_name" in fieldnames:
        repo_col = "repo_full_name"
    elif "full_name" in fieldnames:
        repo_col = "full_name"
    else:
        raise ValueError("CSV must contain 'repo_full_name' or 'full_name'")

    # если output уже есть и RESUME=True, читаем его вместо input
    if output_path.exists() and RESUME:
        with output_path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames or fieldnames

    # добавим выходные колонки, если их нет
    extra_fields = [
        "p1_architecture_label",
        "p1_confidence",
        "p1_evidence",
        "p1_reasoning",
        "p1_parse_ok",
        "p1_raw",

        "p2_architecture_label",
        "p2_confidence",
        "p2_evidence",
        "p2_reasoning",
        "p2_parse_ok",
        "p2_raw",

        "p3_architecture_label",
        "p3_confidence",
        "p3_evidence",
        "p3_reasoning",
        "p3_parse_ok",
        "p3_raw",

        "p4_architecture_label",
        "p4_confidence",
        "p4_evidence",
        "p4_reasoning",
        "p4_parse_ok",
        "p4_raw",
    ]

    for col in extra_fields:
        if col not in fieldnames:
            fieldnames.append(col)

    total = len(rows)
    print(f"Loaded {total} repositories")

    for idx, row in enumerate(rows, start=1):
        repo_full_name = normalize_cell(row.get(repo_col, ""))

        if not repo_full_name:
            print(f"[{idx}/{total}] empty repo name, skip")
            continue

        if RESUME and already_done(row):
            print(f"[{idx}/{total}] skip already processed: {repo_full_name}")
            continue

        print(f"\n[{idx}/{total}] Processing {repo_full_name}")

        paths = get_repo_artifact_paths(repo_full_name)

        repo_tree = load_text_if_exists(paths["repo_tree"])
        import_graph = load_text_if_exists(paths["import_graph"])
        repo_signatures = load_text_if_exists(paths["repo_signatures"])
        metrics_text = format_metrics(row)

        if not repo_tree:
            print(f"  [WARN] missing repo_tree for {repo_full_name}")
            continue

        # ---- Prompt 1
        try:
            prompt1 = build_prompt_repo_tree(repo_tree)
            res1 = call_variant(prompt1)
            row["p1_architecture_label"] = str(res1["architecture_label"])
            row["p1_confidence"] = str(res1["confidence"])
            row["p1_evidence"] = str(res1["evidence"])
            row["p1_reasoning"] = str(res1["reasoning"])
            row["p1_parse_ok"] = str(res1["parse_ok"])
            row["p1_raw"] = str(res1["raw"])
            print(f"  p1 -> {row['p1_architecture_label']} ({row['p1_confidence']})")
        except Exception as e:
            row["p1_raw"] = f"ERROR: {e}"
            print(f"  [ERROR] p1: {e}")

        # ---- Prompt 2
        try:
            if import_graph:
                prompt2 = build_prompt_repo_tree_imports(repo_tree, import_graph)
                res2 = call_variant(prompt2)
                row["p2_architecture_label"] = str(res2["architecture_label"])
                row["p2_confidence"] = str(res2["confidence"])
                row["p2_evidence"] = str(res2["evidence"])
                row["p2_reasoning"] = str(res2["reasoning"])
                row["p2_parse_ok"] = str(res2["parse_ok"])
                row["p2_raw"] = str(res2["raw"])
                print(f"  p2 -> {row['p2_architecture_label']} ({row['p2_confidence']})")
            else:
                row["p2_raw"] = "SKIPPED: missing import_graph"
                print("  [WARN] p2 skipped: missing import_graph")
        except Exception as e:
            row["p2_raw"] = f"ERROR: {e}"
            print(f"  [ERROR] p2: {e}")

        # ---- Prompt 3
        try:
            if import_graph and repo_signatures:
                prompt3 = build_prompt_repo_tree_imports_signatures(
                    repo_tree=repo_tree,
                    import_graph=import_graph,
                    repo_signatures=repo_signatures,
                )
                res3 = call_variant(prompt3)
                row["p3_architecture_label"] = str(res3["architecture_label"])
                row["p3_confidence"] = str(res3["confidence"])
                row["p3_evidence"] = str(res3["evidence"])
                row["p3_reasoning"] = str(res3["reasoning"])
                row["p3_parse_ok"] = str(res3["parse_ok"])
                row["p3_raw"] = str(res3["raw"])
                print(f"  p3 -> {row['p3_architecture_label']} ({row['p3_confidence']})")
            else:
                row["p3_raw"] = "SKIPPED: missing import_graph or repo_signatures"
                print("  [WARN] p3 skipped: missing import_graph or repo_signatures")
        except Exception as e:
            row["p3_raw"] = f"ERROR: {e}"
            print(f"  [ERROR] p3: {e}")

        # ---- Prompt 4
        try:
            if import_graph and repo_signatures:
                prompt4 = build_prompt_all(
                    repo_tree=repo_tree,
                    import_graph=import_graph,
                    repo_signatures=repo_signatures,
                    metrics_text=metrics_text,
                )
                res4 = call_variant(prompt4)
                row["p4_architecture_label"] = str(res4["architecture_label"])
                row["p4_confidence"] = str(res4["confidence"])
                row["p4_evidence"] = str(res4["evidence"])
                row["p4_reasoning"] = str(res4["reasoning"])
                row["p4_parse_ok"] = str(res4["parse_ok"])
                row["p4_raw"] = str(res4["raw"])
                print(f"  p4 -> {row['p4_architecture_label']} ({row['p4_confidence']})")
            else:
                row["p4_raw"] = "SKIPPED: missing import_graph or repo_signatures"
                print("  [WARN] p4 skipped: missing import_graph or repo_signatures")
        except Exception as e:
            row["p4_raw"] = f"ERROR: {e}"
            print(f"  [ERROR] p4: {e}")

        # сохраняем после каждой строки
        with output_path.open("w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                normalized = {col: r.get(col, "") for col in fieldnames}
                writer.writerow(normalized)

        time.sleep(0.5)

    print(f"\nDone. Results saved to {output_path}")


if __name__ == "__main__":
    main()
