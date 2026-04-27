# Bully Election Algorithm Simulation

class BullyElection:
    def __init__(self, processes):
        self.processes = processes  # list of process IDs
        self.alive = {p: True for p in processes}
        self.coordinator = max(processes)

    def crash(self, pid):
        self.alive[pid] = False
        print(f"Process {pid} crashed.")

    def start_election(self, pid):
        print(f"\nProcess {pid} starts election")

        # Find higher-ID active processes
        higher = [p for p in self.processes if p > pid and self.alive[p]]

        if not higher:
            self.coordinator = pid
            print(f"Process {pid} becomes new Coordinator")
        else:
            print(f"Process {pid} sends Election to {higher}")
            new_leader = max(higher)
            self.start_election(new_leader)

    def show_coordinator(self):
        print("Current Coordinator:", self.coordinator)


# Example Execution
processes = [1, 2, 3, 4, 5]

bully = BullyElection(processes)

bully.show_coordinator()

bully.crash(5)  # Highest process crashes

bully.start_election(2)

bully.show_coordinator()