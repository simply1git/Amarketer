#!/usr/bin/env python3
"""Standalone OpenRouter runner — queries OpenRouter chat completions API.

Zero external dependencies required (uses urllib.request).
Loads OPENROUTER_API_KEY from environment or .env file.
"""
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Fallback active model priority list
MODELS = [
    os.getenv("OPENROUTER_MODEL", "openrouter/auto"),
    "meta-llama/llama-3.3-70b-instruct",
    "deepseek/deepseek-chat",
    "qwen/qwen-2.5-72b-instruct",
    "google/gemini-2.0-flash-001",
]


def load_env():
    env_file = REPO / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

def query_openrouter(prompt: str) -> str:
    load_env()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is missing.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://amarketer.25012004.xyz",
        "X-Title": "Amarketer SoloStack AI",
    }

    last_error = None
    import time
    for attempt in range(3):
        # Try preferred model and fallbacks
        for model in MODELS:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are an autonomous affiliate marketing AI assistant operating the SoloStack website. "
                            "Adhere strictly to FTC disclosure requirements, prohibit income claims, use verified KB terms, "
                            "and produce content with status: draft."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 4096,
            }

            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    choices = data.get("choices", [])
                    if choices and "message" in choices[0]:
                        content = choices[0]["message"].get("content", "").strip()
                        if content:
                            return content
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="replace")
                last_error = f"HTTP {e.code}: {err_body}"
                print(f"[OpenRouter] Model {model} failed ({e.code}), trying next model...", file=sys.stderr)
            except Exception as e:
                last_error = str(e)
                print(f"[OpenRouter] Model {model} error: {e}, trying next model...", file=sys.stderr)
        time.sleep(2)

    raise RuntimeError(f"OpenRouter query failed across all models after retries. Last error: {last_error}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/run_openrouter_task.py \"<prompt>\"", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]
    try:
        res = query_openrouter(prompt)
        print(res)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
