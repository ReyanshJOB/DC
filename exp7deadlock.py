# Deadlock Detection using DFS (Wait-For Graph)

n = int(input("Enter number of processes: "))

# Initialize graph
graph = []
print("Enter Wait-For Graph matrix:")

for i in range(n):
    row = list(map(int, input().split()))
    graph.append(row)

visited = [0] * n
stack = [0] * n

def dfs(v):
    visited[v] = 1
    stack[v] = 1

    for i in range(n):
        if graph[v][i]:
            if not visited[i]:
                if dfs(i):
                    return True
            elif stack[i]:
                return True

    stack[v] = 0
    return False


def detect_deadlock():
    for i in range(n):
        visited[i] = 0
        stack[i] = 0

    for i in range(n):
        if not visited[i]:
            if dfs(i):
                return True
    return False


# Output
if detect_deadlock():
    print("Deadlock Detected in the system")
else:
    print("No Deadlock in the system")