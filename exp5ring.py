# Ring Election Algorithm Simulation

class RingElection:
    def __init__(self, processes):
        self.processes = processes
        self.alive = {p: True for p in processes}
        self.coordinator = max(processes)

    def crash(self, pid):
        self.alive[pid] = False
        print(f"Process {pid} crashed.")

    def start_election(self, starter):
        print(f"\nProcess {starter} starts election")

        active_list = []
        n = len(self.processes)

        # Find index of starter process
        index = self.processes.index(starter)

        # Traverse ring
        for i in range(n):
            pid = self.processes[(index + i) % n]
            if self.alive[pid]:
                active_list.append(pid)

        print("Active Processes:", active_list)

        # Select highest ID as coordinator
        new_leader = max(active_list)
        self.coordinator = new_leader

        print(f"Process {new_leader} elected as Coordinator")

    def show_coordinator(self):
        print("Current Coordinator:", self.coordinator)


# Example Execution
processes = [1, 2, 3, 4]

ring = RingElection(processes)

ring.show_coordinator()

ring.crash(4)  # Highest process crashes

ring.start_election(2)

ring.show_coordinator()