import time, argparse, uvicorn, itertools
from fastapi import FastAPI
from ..llm.inference import run_llm

from src.rag.retriever import retrieve_context
from src.common.models import Request
app = FastAPI()
PORT = 8001

class GPUWorker:
    def __init__(self, id):
        self.id = id

    def process(self, request):
        start = time.time()

        print(f"[Worker {self.id}] Processing request {request.id}")

        # RAG Step
        context = retrieve_context(request.query)

        # LLM step
        result = run_llm(request.query, context)

        latency = time.time() - start

        return {
            "worker_id": self.id,
            "worker_port": PORT,
            "id": request.id,
            "result": result,
            "latency": latency
        }

worker = GPUWorker(id=PORT)

counter = itertools.count(1)

@app.post("/infer")
async def infer(payload: dict):
    query = payload.get("query", "")
    request = Request(id=next(counter), query=query)
    return worker.process(request)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()
    PORT = args.port
    worker = GPUWorker(id=PORT)
    uvicorn.run(app, host="127.0.0.1", port=PORT)