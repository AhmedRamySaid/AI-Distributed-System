import time

def run_llm(query, context):
    # Stimulate GPU inference delay
    time.sleep(0.2)

    return f"LLM Answer to 'query' using [{context}]"