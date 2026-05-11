from workers.gpu_worker import GPUWorker
from client.load_generator import run_load_test

def main():
    # Create GPU workers
    workers = [GPUWorker(i) for i in range(4)] # simulate 4 GPUs

    # Run Simulation
    run_load_test()

if __name__ == '__main__':
    main()