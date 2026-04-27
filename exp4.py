# Number of processes
n = 3

# Initialize vector clocks
P0 = [0] * n
P1 = [0] * n
P2 = [0] * n

# Function to print clocks
def show():
    print("P0:", P0)
    print("P1:", P1)
    print("P2:", P2)
    print("-" * 30)


# Event 1: P0 local event
P0[0] += 1
print("Event 1: P0 performs local event")
show()

# Event 2: P0 sends message to P1
P0[0] += 1
msg = P0.copy()
print("Event 2: P0 sends message to P1")
show()

# Event 3: P1 receives message from P0
P1 = [max(P1[i], msg[i]) for i in range(n)]
P1[1] += 1
print("Event 3: P1 receives message from P0")
show()

# Event 4: P2 local event
P2[2] += 1
print("Event 4: P2 performs local event")
show()

# Event 5: P1 sends message to P2
P1[1] += 1
msg2 = P1.copy()
print("Event 5: P1 sends message to P2")
show()

# Event 6: P2 receives message from P1
P2 = [max(P2[i], msg2[i]) for i in range(n)]
P2[2] += 1
print("Event 6: P2 receives message from P1")
show()