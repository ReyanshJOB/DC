# Distributed Computing (DC) — Experiments Guide

> **Course:** Distributed Computing Lab  
> **Total Experiments:** 8  
> **Language:** Python 3  
> **Prerequisites:** Python 3.x installed, basic knowledge of sockets and threading

---

## Table of Contents

1. [Exp 1 — TCP Socket Communication](#exp-1--tcp-socket-communication)
2. [Exp 2 — Remote Procedure Call (RPC)](#exp-2--remote-procedure-call-rpc)
3. [Exp 3 — Multicast Communication](#exp-3--multicast-communication)
4. [Exp 4 — Vector Clocks](#exp-4--vector-clocks)
5. [Exp 5 — Leader Election (Bully & Ring)](#exp-5--leader-election-bully--ring)
6. [Exp 6 — Mutual Exclusion (Non-Token & Token)](#exp-6--mutual-exclusion-non-token--token)
7. [Exp 7 — Deadlock Detection](#exp-7--deadlock-detection)
8. [Exp 8 — Task Assignment](#exp-8--task-assignment)

---

## Exp 1 — TCP Socket Communication

### Summary

This experiment demonstrates **basic client-server communication** using TCP (Transmission Control Protocol) sockets in Python. The server waits for a client connection, receives a message, and sends back a response. It establishes the foundation of all distributed communication — a reliable, connection-oriented, two-way message exchange between two processes over a network.

### Key Concepts

- **TCP Socket (`SOCK_STREAM`):** Reliable, ordered, connection-based communication.
- **Bind & Listen:** Server binds to an IP/port and listens for incoming connections.
- **Accept:** Server blocks until a client connects, then receives a connection object.
- **Send/Recv:** Data is exchanged as encoded byte strings.

### Files

| File | Role |
|------|------|
| `exp1server.py` | Waits for connection, receives message, sends reply |
| `exp1client.py` | Connects to server, sends message, receives reply |

### How to Run

Open **two terminal windows**:

**Terminal 1 — Start the Server first:**
```bash
python exp1server.py
```

**Terminal 2 — Start the Client:**
```bash
python exp1client.py
```

- The client prompts you to type a message and sends it to the server.
- The server displays the received message, then prompts for a reply.
- The client displays the server's reply.

### Expected Output

```
# Server
Server: Waiting for connection...
Server: Connected to ('127.0.0.1', XXXXX)
Server: Received -> Hello Server!
Server: Enter response -> Hi Client!

# Client
Client: Enter message -> Hello Server!
Client: Received -> Hi Client!
```

---

## Exp 2 — Remote Procedure Call (RPC)

### Summary

This experiment simulates **Remote Procedure Call (RPC)** — a mechanism that allows a client to invoke functions (procedures) on a remote server as if they were local calls. The client sends a function name and arguments using Python's `pickle` serialization. The server receives the request, executes the function, and returns the result. This experiment demonstrates the **add** and **multiply** operations remotely.

### Key Concepts

- **RPC:** Client calls a function that executes on the server, not locally.
- **Pickle:** Python's built-in serialization module used to encode/decode Python objects (tuples, numbers) for transmission.
- **Dynamic Dispatch:** `getattr(server, function_name)(*args)` dynamically invokes the correct method on the server object.
- **Persistent Connection:** The client-server connection stays open for multiple calls (unlike Exp 1).

### Files

| File | Role |
|------|------|
| `exp2server.py` | Hosts `RPCServer` with `add()` and `multiply()` methods |
| `exp2client.py` | Provides menu to choose operation, sends request, displays result |

### How to Run

Open **two terminal windows**:

**Terminal 1 — Start the Server:**
```bash
python exp2server.py
```

**Terminal 2 — Start the Client:**
```bash
python exp2client.py
```

- Choose option 1 (Add) or 2 (Multiply) from the menu.
- Enter two numbers; the result is computed on the server and displayed on the client.
- Choose option 3 to exit.

### Expected Output

```
# Client
--- RPC Client Menu ---
1. Add
2. Multiply
3. Exit
Enter your choice: 1
Enter first number: 5
Enter second number: 3
Result = 8

# Server
RPC Server: Waiting for client...
RPC Server: Client connected from ('127.0.0.1', XXXXX)
RPC Server: Request -> add(5, 3)
```

---

## Exp 3 — Multicast Communication

### Summary

This experiment demonstrates **IP Multicast** — a method of sending a single message from one sender to **multiple receivers simultaneously** using a special multicast group IP address. Unlike unicast (one-to-one) or broadcast (one-to-all), multicast efficiently delivers messages to a subscribed group only. This is used in video streaming, online gaming, and distributed system coordination.

### Key Concepts

- **Multicast Group IP (`224.1.1.1`):** A Class D IP address that all receivers join to get messages.
- **UDP Socket (`SOCK_DGRAM`):** Connectionless, lightweight — suitable for one-to-many delivery.
- **TTL (Time-To-Live):** Limits how far the multicast packet travels across routers (set to 1 = local network only).
- **`SO_REUSEADDR`:** Allows multiple receivers to bind to the same port on the same machine.
- **`IP_ADD_MEMBERSHIP`:** Joins the multicast group to start receiving messages.

### Files

| File | Role |
|------|------|
| `exp3sender.py` | Sends messages to multicast group `224.1.1.1:5007` |
| `exp3receiver.py` | Joins the multicast group and listens for incoming messages |

### How to Run

Open **one sender terminal and one or more receiver terminals**:

**Terminal 1, 2, ... — Start Receiver(s) first:**
```bash
python exp3receiver.py
```

**Last Terminal — Start Sender:**
```bash
python exp3sender.py
```

- All receivers will get every message typed by the sender simultaneously.
- You can run multiple receivers to see the one-to-many delivery.

### Expected Output

```
# Sender
Sender ready...
Enter message: Hello Group!
Enter message: DC Lab is fun!

# Receiver (all instances)
Receiver ready...
Received from ('127.0.0.1', XXXXX): Hello Group!
Received from ('127.0.0.1', XXXXX): DC Lab is fun!
```

---

## Exp 4 — Vector Clocks

### Summary

This experiment implements **Vector Clocks** — a logical clock algorithm used to track **causality** (the "happened-before" relationship) between events in a distributed system. Since distributed processes don't share a global physical clock, vector clocks assign a vector of integers to each process, which gets updated on local events and message exchanges. This allows us to determine whether one event causally preceded another.

### Key Concepts

- **Vector Clock:** Each process maintains an array of size `n` (number of processes).
- **Local Event:** Process increments only its own counter.
- **Send Event:** Process increments its counter and sends its full vector with the message.
- **Receive Event:** Process takes the element-wise maximum of its vector and the received vector, then increments its own counter.
- **Happened-Before (→):** If `VC(A)[i] ≤ VC(B)[i]` for all `i`, then A → B.

### Simulated Events (3 Processes: P0, P1, P2)

| Event | Description |
|-------|-------------|
| Event 1 | P0 performs a local event |
| Event 2 | P0 sends a message to P1 |
| Event 3 | P1 receives the message from P0 |
| Event 4 | P2 performs a local event |
| Event 5 | P1 sends a message to P2 |
| Event 6 | P2 receives the message from P1 |

### Files

| File | Role |
|------|------|
| `exp4.py` | Simulates all 6 events and prints vector clock states after each |

### How to Run

```bash
python exp4.py
```

No input required — it simulates events automatically and prints the vector clock values at each step.

### Expected Output

```
Event 1: P0 performs local event
P0: [1, 0, 0]
P1: [0, 0, 0]
P2: [0, 0, 0]
------------------------------
Event 2: P0 sends message to P1
P0: [2, 0, 0]
...
Event 6: P2 receives message from P1
P0: [2, 0, 0]
P1: [2, 2, 0]
P2: [2, 2, 3]
```

---

## Exp 5 — Leader Election (Bully & Ring)

### Summary

This experiment implements two classic **Leader Election algorithms** used in distributed systems to elect a coordinator when the current leader fails.

### 5A — Bully Algorithm

The **Bully Algorithm** elects the process with the **highest ID** as the new leader. When a process notices the coordinator is down, it sends `ELECTION` messages to all processes with higher IDs. If no one responds, it declares itself the leader ("bullies" its way to the top).

#### Key Concepts
- Process with the highest ID always wins.
- A process that receives an ELECTION message from a lower-ID process takes over the election.
- Simple but causes more messages in large systems.

#### Simulated Scenario
- Processes: `[1, 2, 3, 4, 5]`
- Process 5 (highest) crashes.
- Process 2 starts the election → 3, 4 respond → 4 wins.

### 5B — Ring Algorithm

The **Ring Algorithm** arranges processes in a logical ring. When an election starts, the initiator sends its ID around the ring. Each process appends its own ID if it's larger, until the message returns to the initiator — the highest ID in the message becomes the new coordinator.

#### Key Concepts
- All processes are arranged in a circular ring.
- The message travels the full ring before a decision is made.
- More messages, but simpler coordination.

#### Simulated Scenario
- Processes: `[1, 2, 3, 4]`
- Process 4 (highest) crashes.
- Process 2 starts election → active processes identified → process 3 elected.

### Files

| File | Role |
|------|------|
| `exp5bully.py` | Simulates Bully election algorithm |
| `exp5ring.py` | Simulates Ring election algorithm |

### How to Run

**Bully Algorithm:**
```bash
python exp5bully.py
```

**Ring Algorithm:**
```bash
python exp5ring.py
```

No input required — both run automatic simulations.

### Expected Output

```
# Bully
Current Coordinator: 5
Process 5 crashed.
Process 2 starts election
Process 2 sends Election to [3, 4]
Process 3 starts election
...
Process 4 becomes new Coordinator

# Ring
Current Coordinator: 4
Process 4 crashed.
Process 2 starts election
Active Processes: [2, 3, 1]
Process 3 elected as Coordinator
```

---

## Exp 6 — Mutual Exclusion (Non-Token & Token)

### Summary

This experiment implements two algorithms for **Mutual Exclusion** in distributed systems — ensuring that only one process enters the **Critical Section (CS)** at a time without a central coordinator.

### 6A — Ricart-Agrawala Algorithm (Non-Token Based)

The **Ricart-Agrawala algorithm** is a message-passing based mutual exclusion algorithm. A process that wants to enter the CS broadcasts a `REQUEST` with a timestamp to all others. It enters the CS only after receiving `REPLY` from all processes. Processes with lower-priority (lower timestamp) defer their replies until they exit the CS.

#### Key Concepts
- No token — uses timestamps and message passing.
- A process can enter CS only after `n-1` replies (from all other processes).
- Based on Lamport timestamps for ordering requests.
- Deferred replies are sent after exiting CS.

### 6B — Singhal's Token-Based Algorithm

**Singhal's algorithm** uses a **token** (a logical privilege). Only the process holding the token can enter the CS. When a process needs the CS, it sets its `request` flag. The token is passed from the current holder to the next requesting process.

#### Key Concepts
- A single token circulates among processes.
- Simpler than non-token approaches — no quorum or voting needed.
- Starvation is possible if the token-holder doesn't release it fairly.

### Files

| File | Role |
|------|------|
| `exp6nontoken.py` | Ricart-Agrawala non-token mutual exclusion using threads |
| `exp6token.py` | Singhal's token-based mutual exclusion using threads |

### How to Run

**Non-Token (Ricart-Agrawala):**
```bash
python exp6nontoken.py
```

**Token-Based (Singhal):**
```bash
python exp6token.py
```

Both scripts run for **20 seconds** with 3 processes generating random CS requests. No user input needed.

### Expected Output

```
# Non-Token
Process 0 requesting CS at time 1714230000.12
Process 1 requesting CS at time 1714230003.45
Process 0 ENTERED Critical Section
Process 0 EXITING Critical Section
Process 1 ENTERED Critical Section
...

# Token
Process 2 requesting Critical Section
Process 2 ENTERED Critical Section
Process 2 EXITING Critical Section
```

---

## Exp 7 — Deadlock Detection

### Summary

This experiment implements **Deadlock Detection** in distributed systems using a **Wait-For Graph (WFG)** and **Depth-First Search (DFS)**. A deadlock occurs when a set of processes are each waiting for a resource held by another process in the set, forming a cycle. The algorithm builds a directed graph where an edge `i → j` means "process i is waiting for process j," and then runs DFS to detect any cycle.

### Key Concepts

- **Wait-For Graph (WFG):** A directed graph where nodes are processes and edges represent waiting relationships.
- **Cycle = Deadlock:** If DFS finds a back-edge (revisits a node on the current stack), a cycle — and thus a deadlock — exists.
- **DFS with Stack Tracking:** The `visited[]` array tracks all visited nodes; the `stack[]` array tracks the current DFS path.
- **Adjacency Matrix Input:** `graph[i][j] = 1` means process `i` waits for process `j`.

### Files

| File | Role |
|------|------|
| `exp7deadlock.py` | Reads WFG matrix, runs DFS, and reports whether deadlock exists |

### How to Run

```bash
python exp7deadlock.py
```

**Input format:**
```
Enter number of processes: 3
Enter Wait-For Graph matrix:
0 1 0
0 0 1
1 0 0
```

### Sample Input/Output — With Deadlock

```
Enter number of processes: 3
Enter Wait-For Graph matrix:
0 1 0
0 0 1
1 0 0

Deadlock Detected in the system
```

### Sample Input/Output — No Deadlock

```
Enter number of processes: 3
Enter Wait-For Graph matrix:
0 1 0
0 0 1
0 0 0

No Deadlock in the system
```

> **Tip:** A cycle like P0→P1→P2→P0 represents a deadlock. If there's no cycle (e.g., P0→P1→P2 with no back-edge), the system is deadlock-free.

---

## Exp 8 — Task Assignment

### Summary

This experiment implements a **greedy Task Assignment algorithm** in distributed computing. Given a set of tasks and processors, the goal is to assign each task to the processor with the minimum execution cost, then calculate the additional communication cost incurred when tasks assigned to different processors need to communicate. It models the classic **task scheduling** problem in parallel/distributed systems.

### Key Concepts

- **Execution Cost Matrix:** `exec_cost[i][j]` = cost of running task `i` on processor `j`.
- **Communication Cost Matrix:** `comm_cost[i][j]` = cost of communication between task `i` and task `j`.
- **Greedy Assignment:** Each task is independently assigned to the processor with the lowest execution cost.
- **Inter-Processor Communication:** If task `i` and task `j` are on different processors, `comm_cost[i][j]` is added to the total cost.
- **Total Cost = Execution Cost + Communication Cost**

### Files

| File | Role |
|------|------|
| `exp8task.py` | Reads costs, assigns tasks greedily, calculates total cost |

### How to Run

```bash
python exp8task.py
```

**Input format:**
```
Enter number of tasks: 3
Enter number of processors: 2

Enter Execution Cost Matrix:
5 8
6 3
7 4

Enter Communication Cost Matrix:
0 2 3
2 0 1
3 1 0
```

### Expected Output

```
Task Assignment:
Task 1 → Processor 1 (Cost = 5)
Task 2 → Processor 2 (Cost = 3)
Task 3 → Processor 2 (Cost = 4)

Execution Cost: 12
Communication Cost: 3
Total Cost: 15
```

> **Note:** Communication cost is counted for pairs of tasks on *different* processors. In the above example, Task 1 (P1) communicates with Task 2 (P2) and Task 3 (P2), adding `comm_cost[0][1] + comm_cost[0][2] = 2 + 3 = 5`. Both directions are counted, so the actual sum may vary based on matrix symmetry.

---

## Quick Reference — All Experiments

| Exp | Topic | Files | Input |
|-----|-------|-------|-------|
| 1 | TCP Socket Communication | `exp1server.py`, `exp1client.py` | Interactive (2 terminals) |
| 2 | Remote Procedure Call (RPC) | `exp2server.py`, `exp2client.py` | Interactive menu (2 terminals) |
| 3 | Multicast Communication | `exp3sender.py`, `exp3receiver.py` | Interactive (2+ terminals) |
| 4 | Vector Clocks | `exp4.py` | None (auto-simulation) |
| 5 | Leader Election (Bully & Ring) | `exp5bully.py`, `exp5ring.py` | None (auto-simulation) |
| 6 | Mutual Exclusion | `exp6nontoken.py`, `exp6token.py` | None (runs 20 sec) |
| 7 | Deadlock Detection | `exp7deadlock.py` | Matrix via terminal |
| 8 | Task Assignment | `exp8task.py` | Matrix via terminal |

---

## Setup & Environment

```bash
# Check Python version (3.x required)
python --version

# No external packages needed — all experiments use standard library only:
# socket, threading, time, random, struct, pickle
```

All files must be run from the directory where they are saved:
```bash
cd DC-main/
```

For experiments with separate client/server or sender/receiver files, **always start the server/receiver first**, then the client/sender in a new terminal.
