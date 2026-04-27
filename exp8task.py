# Task Assignment with Execution + Communication Cost

# Input
tasks = int(input("Enter number of tasks: "))
processors = int(input("Enter number of processors: "))

# Execution Cost Matrix
exec_cost = []
print("\nEnter Execution Cost Matrix:")
for i in range(tasks):
    row = list(map(int, input().split()))
    exec_cost.append(row)

# Communication Cost Matrix
comm_cost = []
print("\nEnter Communication Cost Matrix:")
for i in range(tasks):
    row = list(map(int, input().split()))
    comm_cost.append(row)

assignment = [-1] * tasks
total_exec_cost = 0

print("\nTask Assignment:")

# Assign each task to processor with minimum execution cost
for i in range(tasks):
    min_cost = exec_cost[i][0]
    processor = 0

    for j in range(1, processors):
        if exec_cost[i][j] < min_cost:
            min_cost = exec_cost[i][j]
            processor = j

    assignment[i] = processor
    total_exec_cost += min_cost

    print(f"Task {i+1} → Processor {processor+1} (Cost = {min_cost})")

# Calculate Communication Cost
total_comm_cost = 0

for i in range(tasks):
    for j in range(tasks):
        if i != j:
            # If tasks are on different processors
            if assignment[i] != assignment[j]:
                total_comm_cost += comm_cost[i][j]

# Final Cost
total_cost = total_exec_cost + total_comm_cost

print("\nExecution Cost:", total_exec_cost)
print("Communication Cost:", total_comm_cost)
print("Total Cost:", total_cost)