"""
llm/inference.py — LLM inference via Ollama (llama3.2:1b).

Calls the local Ollama REST API at http://localhost:11434.
Make sure Ollama is running before starting the system:
    ollama serve          # (usually auto-starts)
    ollama pull llama3.2:1b

The function run_llm(query, context) is what gpu_worker.py calls:
    result = run_llm(request.query, context)
"""

import urllib.request
import urllib.error
import json
import time

# ── Config ────────────────────────────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"
TEMPERATURE  = 0.3        # low = more focused / factual
MAX_TOKENS   = 512
TIMEOUT_SEC  = 120        # seconds before giving up on a request


# ── Prompt builder ────────────────────────────────────────────────────────────
def _build_prompt(query: str, context: str) -> str:
    """
    Constructs a RAG-style prompt:
      - System instruction  (role + rules)
      - Retrieved context   (from ChromaDB)
      - User question
    """
    return f"""You are a helpful assistant. Answer the user's question using ONLY the provided context.
If the context does not contain enough information, say so honestly — do not make things up.

--- CONTEXT START ---
{context}
--- CONTEXT END ---

User question: {query}

Answer:"""


# ── Core inference ─────────────────────────────────────────────────────────────
def run_llm(query: str, context: str) -> str:
    """
    Send query + RAG context to Ollama and return the generated answer.

    Falls back to a clear error message if Ollama is unreachable,
    so the rest of the distributed system keeps running.
    """
    prompt = _build_prompt(query, context)

    payload = json.dumps({
        "model":  MODEL_NAME,
        "prompt": prompt,
        "stream": False,               # wait for full response
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": 128,
        },
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SEC) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            answer = body.get("response", "").strip()
            return answer if answer else "[LLM returned an empty response]"

    except urllib.error.URLError as e:
        return (
            f"[LLM ERROR] Could not reach Ollama at {OLLAMA_URL}. "
            f"Is 'ollama serve' running? Details: {e.reason}"
        )
    except TimeoutError:
        return f"[LLM ERROR] Request timed out after {TIMEOUT_SEC}s."
    except Exception as e:
        return f"[LLM ERROR] Unexpected error: {e}"


# ── Stats helper (optional, used by monitoring) ────────────────────────────────
def run_llm_timed(query: str, context: str) -> tuple[str, float]:
    """Same as run_llm but also returns inference latency in seconds."""
    t0 = time.time()
    result = run_llm(query, context)
    latency = round(time.time() - t0, 3)
    return result, latency


# ── Quick test ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Import retriever only for the self-test
    from src.rag.retriever import retrieve_context

    test_queries = [
        "How can I remember things better?"
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query    : {q}")
        print("-" * 60)

        ctx = retrieve_context(q)
        print(f"Context  :\n{ctx[:300]}...\n")   # preview first 300 chars

        answer, latency = run_llm_timed(q, ctx)
        print(f"Answer   : {answer}")
        print(f"Latency  : {latency}s")