from dotenv import load_dotenv
import os
import requests
from typing import Optional, List
from ollama import Client


LOCAL_OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(
    prompt: str,
    model: str,
    *,
    system_prompt: Optional[str] = None,
    context: Optional[List[int]] = None,
    temperature: float = 0.2,
    timeout: int = 300,
) -> str:
    """
    Universal LLM caller.

    - cloud models (name contains 'cloud'):
        → ollama.com via Client.chat
    - local models:
        → localhost via HTTP generate

    Always returns ONE string.
    """

    is_cloud = "cloud" in model.lower()

    # ---------- CLOUD ----------
    if is_cloud:
        load_dotenv()
        api_key = os.getenv("OLLAMA_API_KEY")
        if not api_key:
            raise RuntimeError("OLLAMA_API_KEY is not set")

        client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"},
        )

        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt,
            })

        messages.append({
            "role": "user",
            "content": prompt,
        })

        try:
            parts = []
            for part in client.chat(
                model=model.replace("-cloud", ""),
                messages=messages,
                stream=True,
            ):
                parts.append(part["message"]["content"])

            return "".join(parts).strip()

        except Exception as e:
            raise RuntimeError(f"Ollama cloud chat failed: {e}")

    # ---------- LOCAL ----------
    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    # context допустим ТОЛЬКО локально
    if context:
        payload["context"] = context

    try:
        response = requests.post(
            LOCAL_OLLAMA_URL,
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama local request failed: {e}")

    data = response.json()
    if "response" not in data:
        raise RuntimeError(f"Invalid Ollama response: {data}")

    return data["response"].strip()


if __name__ == "__main__":
    print(call_llm("Explain software architecture in one sentence", model="qwen3-coder:480b-cloud"))
