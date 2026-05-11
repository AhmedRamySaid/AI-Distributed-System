import requests
import threading

def simulate_user(query, user_id):
    url = "http://192.168.184.31/infer"

    try:
        response = requests.post(url, json={"query": query})
        data = response.json()
        print(
            f"[User {user_id}] Worker: {data.get('worker_id')} | Latency: {data.get('latency'):.2f}s | Result: {data.get('result', '')[:50]}...")
    except Exception as e:
        print(f"[User {user_id}] Error: {e}")

def run_load_test(num_users=1000):
    threads = []
    for i in range(num_users):
        t = threading.Thread(target=simulate_user, args=(f"user_id: {i}", i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()