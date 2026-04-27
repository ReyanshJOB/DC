import threading
import time
import random

class Process:
    def __init__(self, pid, total_processes):
        self.pid = pid
        self.total = total_processes
        self.has_token = False
        self.request = False

    def request_cs(self):
        print(f"Process {self.pid} requesting Critical Section")
        self.request = True

    def enter_cs(self):
        print(f"Process {self.pid} ENTERED Critical Section")
        time.sleep(2)
        print(f"Process {self.pid} EXITING Critical Section")
        self.request = False


def singhal_algorithm(processes):
    token_holder = 0
    processes[token_holder].has_token = True

    while True:
        for p in processes:
            if p.request and processes[token_holder].has_token:
                processes[token_holder].has_token = False
                p.has_token = True
                token_holder = p.pid

                p.enter_cs()
                time.sleep(1)


# Main
n = 3
processes = [Process(i, n) for i in range(n)]

def generate_requests():
    while True:
        time.sleep(random.randint(3, 6))
        p = random.choice(processes)
        p.request_cs()

threading.Thread(target=singhal_algorithm, args=(processes,), daemon=True).start()
threading.Thread(target=generate_requests, daemon=True).start()

time.sleep(20)