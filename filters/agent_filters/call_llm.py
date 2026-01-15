import requests
import json
from typing import Optional


OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen3:8b"  # или llama3, qwen, mistral и т.д.


def call_llm(
    prompt: str,
    model: str = DEFAULT_MODEL,
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    timeout: int = 300000
) -> str:
    """
    Call local Ollama LLM and return plain text response
    """

    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"

    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=timeout
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Ollama request failed: {e}")

    data = response.json()

    if "response" not in data:
        raise RuntimeError(f"Invalid Ollama response: {data}")

    return data["response"].strip()


if __name__ == "__main__":
    print(call_llm("Explain software architecture in one sentence"))
