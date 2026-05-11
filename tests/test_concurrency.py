from src.common.models import Request
from src.workers.gpu_worker import GPUWorker
from concurrent.futures import ThreadPoolExecutor


def test_concurrent_requests():
    worker = GPUWorker(id=0)

    def send_request(i):
        request = Request(
            id=i,
            query=f"Query {i}"
        )
        return worker.process(request)

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(send_request, range(10)))

    assert len(results) == 10

    for response in results:
        assert response["status"] == "success"