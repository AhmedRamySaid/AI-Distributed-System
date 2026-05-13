import requests
import threading
import time

def simulate_user(query, user_id):
    url = "https://wooing-foe-poker.ngrok-free.dev/infer"
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true"
    }
    start = time.time()

    try:
        response = requests.post(url, json={"query": query}, headers=headers, timeout=60)
        if response.status_code == 200:
            data = response.json()
            latency = time.time() - start
            print(f"[User {user_id}] Worker: {data.get('worker_id')} | "
                  f"Server Latency: {data.get('latency')} | Total Latency: {latency:.2f}s "
                  f"Reply: {data.get('result')}")
            return
        else:
            _ = response.status_code
    except Exception as e:
        print(f"[User {user_id}] error: {e}, retrying...")

def run_load_test(num_users=1000):
    threads = []
    for i in range(num_users):
        t = threading.Thread(target=simulate_user, args=(f"user_id: {i}", i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()