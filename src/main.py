from client.load_generator import run_load_test

def main():
    # Run Simulation
    run_load_test(num_users=100)

if __name__ == '__main__':
    main()