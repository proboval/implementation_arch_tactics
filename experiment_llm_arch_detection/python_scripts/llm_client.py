import os
import time
from typing import List, Optional

import requests
from ollama import Client


LOCAL_OLLAMA_URL = "http://localhost:11434/api/generate"

def _get_api_keys() -> List[str]:
    keys = [
        os.getenv("OLLAMA_API_KEY"),
        os.getenv("OLLAMA_API_KEY_1"),
    ]
    return [k for k in keys if k]



def _call_cloud(
    model: str,
    prompt: str,
    system_prompt: Optional[str],
    temperature: float,
    timeout: int,
) -> str:

    api_keys = _get_api_keys()

    if not api_keys:
        raise RuntimeError("No OLLAMA_API_KEY provided")

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

    last_error = None

    for key_index, api_key in enumerate(api_keys):

        client = Client(
            host="https://ollama.com",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout,
        )

        try:
            parts = []

            for part in client.chat(
                model=model.replace("-cloud", ""),
                messages=messages,
                stream=True,
                options={"temperature": temperature},
            ):
                parts.append(part["message"]["content"])

            return "".join(parts).strip()

        except Exception as e:
            last_error = e

            # если это не последний ключ — пробуем следующий
            if key_index < len(api_keys) - 1:
                time.sleep(1)
                continue

            break

    raise RuntimeError(f"Ollama cloud failed with all API keys: {last_error}")


def _call_local(
    model: str,
    prompt: str,
    system_prompt: Optional[str],
    context: Optional[List[int]],
    temperature: float,
    timeout: int,
) -> str:

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

    if context:
        payload["context"] = context

    try:
        response = requests.post(
            LOCAL_OLLAMA_URL,
            json=payload,
            timeout=timeout,
        )

        if response.status_code == 429:
            raise RuntimeError("Local Ollama quota exceeded (429)")

        response.raise_for_status()

    except requests.RequestException as e:
        raise RuntimeError(f"Ollama local request failed: {e}")

    data = response.json()

    if "response" not in data:
        raise RuntimeError(f"Invalid Ollama response: {data}")

    return data["response"].strip()


def call_llm(
    prompt: str,
    model: str,
    *,
    system_prompt: Optional[str] = None,
    context: Optional[List[int]] = None,
    temperature: float = 0.2,
    timeout: int = 300,
    retries: int = 2,
) -> str:
    """
    Universal LLM caller with:
    - multi-key fallback
    - retries
    - robust error handling
    - cloud/local routing
    """

    is_cloud = "cloud" in model.lower()

    last_error = None

    for attempt in range(retries + 1):

        try:

            if is_cloud:
                return _call_cloud(
                    model=model,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    timeout=timeout,
                )

            return _call_local(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                context=context,
                temperature=temperature,
                timeout=timeout,
            )

        except Exception as e:
            last_error = e

            if attempt < retries:
                sleep_time = 2 ** attempt
                time.sleep(sleep_time)
                continue

            break

    raise RuntimeError(f"call_llm failed after retries: {last_error}")