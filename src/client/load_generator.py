import requests
import threading

def simulate_user(user_id):
    url = "http://197.39.16.85/infer"
    query = f"Query {user_id}"

    response = requests.post(url, json={"query": query})
    print(response.json())

def run_load_test(num_users=1000):
    threads = []
    for i in range(num_users):
        t = threading.Thread(target=simulate_user, args=(i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()