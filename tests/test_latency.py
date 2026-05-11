from src.common.models import Request
from src.workers.gpu_worker import GPUWorker


def test_worker_returns_latency():
    worker = GPUWorker(id=0)
    request = Request(id=1, query="What is CUDA?")

    response = worker.process(request)

    assert "latency" in response
    assert response["latency"] >= 0