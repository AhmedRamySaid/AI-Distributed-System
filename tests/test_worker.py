from src.common.models import Request
from src.workers.gpu_worker import GPUWorker


def test_worker_process_request():
    worker = GPUWorker(id=0)
    request = Request(id=1, query="What is CUDA?")

    response = worker.process(request)

    assert response["id"] == 1
    assert response["result"] is not None
    assert response["latency"] >= 0