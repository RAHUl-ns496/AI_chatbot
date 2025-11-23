import os
import json
import requests
import time

# Optional OpenAI support
try:
    import openai
except Exception:
    openai = None


def ask_llm(prompt: str, model: str = "gpt-4"):
    """
    Unified LLM interface:
    - If OPENAI_API_KEY is set and openai package available -> call OpenAI with streaming (requires openai>=1.0.0)
    - Else, if OLLAMA_HOST is set (or default localhost:11434) -> call Ollama streaming endpoint
    This function yields partial responses (generator) to match the existing app streaming code.
    """
    openai_key = os.environ.get("OPENAI_API_KEY")
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    # --- OpenAI path (streaming) ---
    if openai_key and openai is not None:
        try:
            # Use OpenAI v1.0+ API (required)
            client = openai.OpenAI(api_key=openai_key)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.2,
                stream=True,
            )
            full_text = ""
            for event in resp:
                if event.choices and len(event.choices) > 0:
                    delta = event.choices[0].delta
                    content = getattr(delta, 'content', None)
                    if content:
                        full_text += content
                        yield full_text
        except Exception as e:
            yield f"❌ OpenAI error: {e}"
        return

    # --- Ollama (or compatible local) streaming path ---
    try:
        url = f"{ollama_host}/api/generate"
        r = requests.post(url, json={"model": model, "prompt": prompt, "stream": True}, stream=True, timeout=120)
        r.raise_for_status()
        full = ""
        for chunk in r.iter_lines():
            if chunk:
                try:
                    decoded = chunk.decode("utf-8", errors="ignore")
                    data = json.loads(decoded)
                    if "response" in data:
                        full += data["response"]
                        yield full
                    if data.get("done"):
                        break
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
        return
    except requests.exceptions.RequestException as e:
        yield f"❌ Connection error to Ollama: {e}"
    except Exception as e:
        yield f"❌ Unexpected LLM error: {e}"
