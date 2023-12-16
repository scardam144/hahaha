from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def for_loop(val):
    count = 0
    for i in range(0, val):
        count += i
    return count

def exec_time(executor_type):
    start_time = time.time()
    with executor_type(max_workers=4) as executor:
        results = list(executor.map(for_loop, [1000000, 10000000, 100000000, 1000000000]))

    for result in results:
        print(result)

    stop_time = time.time()
    print(f"Total Execution time ({executor_type.__name__}): {stop_time - start_time}")

if __name__ == "__main__":
    
    exec_time(ProcessPoolExecutor)
    exec_time(ThreadPoolExecutor)
