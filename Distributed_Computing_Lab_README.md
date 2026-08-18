# Distributed Computing Lab Programs --- README

This README explains how to install, configure, run, and test all the
distributed-computing programs discussed in this set of tasks.

## Programs Covered

1.  Task 1 --- Message Passing System
2.  Centralized Coordinator Algorithm
3.  Ricart--Agrawala Algorithm
4.  Token Passing Algorithm
5.  Task 1 --- Lamport's Logical Clock
6.  Task 2 --- Vector Clocks
7.  Task 1 --- Basic Client-Server Communication
8.  Task 2 --- Object Serialization using `pickle`
9.  Remote Method Invocation (RMI) using Pyro4

------------------------------------------------------------------------

# 1. Prerequisites

## Python

Install Python 3.9 or later.

Check your installation:

``` bash
python --version
```

On some Linux systems, use:

``` bash
python3 --version
```

## Recommended folder structure

Keep all programs in one project folder, for example:

``` text
distributed-computing/
│
├── README.md
│
├── Message_Passing/
│   ├── server.py
│   └── client.py
│
├── Centralized_Coordinator/
│   ├── server.py
│   └── client.py
│
├── Ricart_Agrawala/
│   └── ricart.py
│
├── Token_Passing/
│   └── token-passing.py
│
├── Logical_Clocks/
│   └── lamport.py
│
├── Vector_Clocks/
│   └── vector_clock.py
│
├── Basic_Client_Server/
│   ├── client_basic_ipc.py
│   └── server_basic_ipc.py
│
├── Object_Serialization/
│   ├── client_pickle.py
│   └── server_pickle.py
│
└── RMI/
    ├── Calculator_server.py
    └── Calculator_client.py
```

The exact folder names are optional. The important part is to keep the
corresponding server/client files together.

------------------------------------------------------------------------

# 2. Installing Dependencies

Most programs use only Python's standard library:

-   `socket`
-   `threading`
-   `time`
-   `sys`
-   `queue`
-   `pickle`

Therefore, no external package is required for those programs.

Only the RMI program requires Pyro4.

Install it with:

``` bash
pip install Pyro4
```

If `pip` is not recognized:

``` bash
python -m pip install Pyro4
```

On Linux:

``` bash
python3 -m pip install Pyro4
```

Verify:

``` bash
python -c "import Pyro4; print(Pyro4.__version__)"
```

------------------------------------------------------------------------

# 3. Important Socket Concepts

Before running the socket programs, understand these terms:

### Host

Most examples use:

``` python
HOST = "127.0.0.1"
```

or:

``` python
HOST = "localhost"
```

This means the programs communicate on the same computer.

### Port

A port identifies the network service.

Examples used here:

``` text
8000
9000
9001
9002
9003
5000
5001
```

Make sure two different servers are not trying to use the same port at
the same time.

### TCP

The examples use:

``` python
socket.AF_INET
socket.SOCK_STREAM
```

which means IPv4 + TCP.

------------------------------------------------------------------------

# 4. Task 1 --- Message Passing System

## Files

``` text
server.py
client.py
```

## Purpose

The server accepts multiple clients. Each client can send messages. The
server broadcasts a client's message to the other connected clients.

Architecture:

``` text
                 SERVER
                   |
        +----------+----------+
        |          |          |
     Client 1   Client 2   Client 3
        |          |          |
        +---- messages -------+
```

The server uses a separate thread for each connected client.

## Run the server

Open Terminal 1:

``` bash
cd Message_Passing
python server.py
```

Expected output:

``` text
<Server> Server listening on 127.0.0.1:8000
```

## Run Client 1

Open Terminal 2:

``` bash
cd Message_Passing
python client.py
```

## Run Client 2

Open Terminal 3:

``` bash
cd Message_Passing
python client.py
```

You can open a fourth terminal and run another client if required.

## Test

In Client 1:

``` text
Enter message: Hello
```

The other clients should receive a message similar to:

``` text
<CLIENT_ADDRESS> Hello
```

Then Client 2 can send:

``` text
Hi Client 1
```

The server broadcasts it to the other clients.

## Exit

Type:

``` text
bye
```

The client disconnects.

## Important

The server should be started before the clients.

------------------------------------------------------------------------

# 5. Centralized Coordinator Algorithm

## Files

``` text
server.py
client.py
```

## Purpose

A single coordinator controls access to the Critical Section (CS).

Only one client can enter the CS at a time.

Architecture:

``` text
Client 1 ----\
Client 2 -----+----> Coordinator ----> Critical Section access
Client 3 ----/
```

The coordinator maintains a request queue.

## Run the coordinator

Terminal 1:

``` bash
cd Centralized_Coordinator
python server.py
```

Expected:

``` text
[Coordinator] Listening on localhost:9000
```

## Run Client 1

Terminal 2:

``` bash
cd Centralized_Coordinator
python client.py
```

## Run Client 2

Terminal 3:

``` bash
cd Centralized_Coordinator
python client.py
```

Run a third client in another terminal if desired.

## What happens

A client sends:

``` text
REQUEST_CS
```

The coordinator puts the request in its queue.

If the CS is free:

``` text
GRANT_CS
```

is sent to the client.

The client enters the CS for approximately 3 seconds.

After finishing, it sends:

``` text
RELEASE_CS
```

The coordinator then grants access to the next waiting client.

## Expected behavior

If Client 1 gets the CS first:

``` text
Client 1 -> REQUEST_CS
Coordinator -> GRANT_CS
Client 1 -> ENTER CS

Client 2 -> REQUEST_CS
Client 3 -> REQUEST_CS

Client 1 -> RELEASE_CS
Coordinator -> GRANT_CS to Client 2
```

This demonstrates centralized mutual exclusion.

------------------------------------------------------------------------

# 6. Ricart--Agrawala Algorithm

## File

``` text
ricart.py
```

## Purpose

Ricart--Agrawala is a distributed mutual exclusion algorithm.

There is no central coordinator.

Each process communicates directly with the other processes.

For three processes:

``` text
Node 1 <----> Node 2
   ^             |
   |             |
   +---- Node 3 -+
```

Each node:

1.  Requests the Critical Section.
2.  Sends `REQUEST` messages to the other nodes.
3.  Waits for `N - 1` replies.
4.  Enters the CS.
5.  Sends deferred replies after leaving the CS.

## Ports

The implementation uses:

``` text
Node 1 -> 9001
Node 2 -> 9002
Node 3 -> 9003
```

## Start Node 1

Terminal 1:

``` bash
cd Ricart_Agrawala
python ricart.py 1
```

## Start Node 2

Terminal 2:

``` bash
cd Ricart_Agrawala
python ricart.py 2
```

## Start Node 3

Terminal 3:

``` bash
cd Ricart_Agrawala
python ricart.py 3
```

Each node should show that it is listening.

## Request the Critical Section

At any node, press:

``` text
Enter
```

The node sends requests to the other two nodes.

For example:

``` text
[1] Requesting CS
```

It waits until it receives:

``` text
2/2 replies
```

Then:

``` text
>>> ENTERING CRITICAL SECTION
```

After approximately 3 seconds:

``` text
<<< EXITING CRITICAL SECTION
```

## Important

Start all three nodes before requesting the CS.

If one node is not running, the requesting node may wait forever for the
missing reply.

------------------------------------------------------------------------

# 7. Token Passing Algorithm

## File

``` text
token-passing.py
```

## Purpose

A token circulates between processes arranged in a logical ring.

Only the process holding the token can enter the Critical Section.

Example:

``` text
Node 1
  |
  v
Node 2
  |
  v
Node 3
  |
  +------> Node 1
```

There should be exactly one token.

## Ports

Use:

``` text
Node 1 -> 9001
Node 2 -> 9002
Node 3 -> 9003
```

## Start Node 1 with the token

Terminal 1:

``` bash
cd Token_Passing
python token-passing.py 9001 9002 yes
```

The arguments mean:

``` text
9001 = this node's port
9002 = next node's port
yes   = this node initially owns the token
```

## Start Node 2

Terminal 2:

``` bash
python token-passing.py 9002 9003
```

## Start Node 3

Terminal 3:

``` bash
python token-passing.py 9003 9001
```

The ring is now:

``` text
9001 -> 9002 -> 9003 -> 9001
```

## Request Critical Section

At any node, type:

``` text
request
```

The node marks that it wants the CS.

It waits until the token reaches it.

When it receives the token:

``` text
>>> Entering critical section...
```

After approximately 3 seconds:

``` text
<<< Exiting critical section...
```

The token is then passed to the next node.

## Important

The token must continue circulating even when a node does not currently
need the CS.

Only one node should start with:

``` text
yes
```

Otherwise you would create multiple tokens, which violates the
token-ring algorithm.

------------------------------------------------------------------------

# 8. Lamport's Logical Clock

## File

``` text
lamport.py
```

## Purpose

Lamport logical clocks assign logical timestamps to events in
distributed systems.

The main rules are:

### Internal event

``` text
Clock = Clock + 1
```

### Send event

``` text
Clock = Clock + 1
```

The timestamp is attached to the message.

### Receive event

``` text
Clock = max(local_clock, received_timestamp) + 1
```

## Run

No server is required.

Simply run:

``` bash
cd Logical_Clocks
python lamport.py
```

Expected output is similar to:

``` text
Process 1 internal event -> Clock: 1
Process 1 sends message -> Clock: 2
Process 2 received message -> Clock: 3
Process 2 internal event -> Clock: 4
```

This program is a simulation. It does not require network sockets.

------------------------------------------------------------------------

# 9. Vector Clocks

## File

``` text
vector_clock.py
```

## Purpose

Vector clocks track the logical state of multiple processes and can
represent both:

-   Causal relationships
-   Concurrent events

For three processes:

``` text
P0 -> [x, x, x]
P1 -> [x, x, x]
P2 -> [x, x, x]
```

Each position represents one process.

## Rules

### Internal event

Increment the process's own component:

``` text
V[pid] = V[pid] + 1
```

### Send

Increment the sender's component and send the vector.

### Receive

Merge:

``` text
V[i] = max(V[i], received[i])
```

Then increment the receiver's own component.

## Run

``` bash
cd Vector_Clocks
python vector_clock.py
```

No server is required.

Expected output is similar to:

``` text
Process 0 internal event -> [1, 0, 0]
Process 0 sends message -> [2, 0, 0]
Process 1 received message -> [2, 1, 0]
Process 2 internal event -> [0, 0, 1]
Process 1 sends message -> [2, 2, 0]
Process 2 received message -> [2, 2, 2]
```

------------------------------------------------------------------------

# 10. Task 1 --- Basic Client-Server Communication

## Files

``` text
server_basic_ipc.py
client_basic_ipc.py
```

## Purpose

The client sends:

``` text
10 20 30 40
```

The server converts them into integers, calculates the sum, and sends
the result back.

Expected result:

``` text
Sum = 100
```

## Start server

Terminal 1:

``` bash
cd Basic_Client_Server
python server_basic_ipc.py
```

Expected:

``` text
Server is waiting for connection...
```

## Start client

Terminal 2:

``` bash
cd Basic_Client_Server
python client_basic_ipc.py
```

Expected client output:

``` text
Server Response: Sum = 100
```

Expected server output:

``` text
Connected by: ('127.0.0.1', <port>)
Client sent: 10 20 30 40
```

## Important

Start the server before starting the client.

------------------------------------------------------------------------

# 11. Task 2 --- Object Serialization using Pickle

## Files

``` text
server_pickle.py
client_pickle.py
```

## Purpose

The client creates:

``` text
DataObject(
    "Alice",
    [10, 20, 30, 40]
)
```

The object is serialized using:

``` python
pickle.dumps(obj)
```

The server receives the bytes and reconstructs the object using:

``` python
pickle.loads(data)
```

The server then calculates the sum.

## Start server

Terminal 1:

``` bash
cd Object_Serialization
python server_pickle.py
```

Expected:

``` text
Waiting for client...
```

## Start client

Terminal 2:

``` bash
python client_pickle.py
```

Server:

``` text
Name: Alice
Values: [10, 20, 30, 40]
```

Client:

``` text
Hello Alice, Sum = 100
```

## Security warning

Do not use:

``` python
pickle.loads()
```

on untrusted network data.

Python pickle data can execute arbitrary code during deserialization. It
is suitable here as a controlled classroom demonstration where the
client and server are your own programs.

------------------------------------------------------------------------

# 12. Remote Method Invocation (RMI) using Pyro4

## Files

``` text
Calculator_server.py
Calculator_client.py
```

## Purpose

RMI allows a client to call methods that execute on a remote server.

The server provides:

``` text
add_numbers(a, b)
multiply(a, b)
```

The client calls them through:

``` python
Pyro4.Proxy
```

## Install Pyro4

``` bash
python -m pip install Pyro4
```

Verify:

``` bash
python -c "import Pyro4; print('Pyro4 installed')"
```

## Server

Start the server first:

``` bash
cd RMI
python Calculator_server.py
```

Expected:

``` text
Server is ready.
URI: PYRO:obj_xxxxxxxxxxxxx@localhost:xxxxx
```

Copy the complete URI.

Example format:

``` text
PYRO:obj_xxxxxxxxxxxxx@localhost:xxxxx
```

## Client

Open another terminal:

``` bash
cd RMI
python Calculator_client.py
```

When prompted:

``` text
Enter the server URI:
```

Paste the URI printed by the server.

Then enter:

``` text
Enter first number: 10
Enter second number: 20
```

Expected:

``` text
Addition: 30
Multiplication: 200
```

## Important

The RMI server must remain running while the client makes remote calls.

------------------------------------------------------------------------

# 13. Running Everything in VS Code

If you are using VS Code:

1.  Open the project folder.
2.  Open the integrated terminal.
3.  Navigate to the required folder.
4.  Start the server.
5.  Open additional terminals using the `+` button.
6.  Start the clients/nodes in the additional terminals.

For example:

``` text
Terminal 1 -> server
Terminal 2 -> client 1
Terminal 3 -> client 2
Terminal 4 -> client 3
```

This is particularly important for:

-   Message Passing
-   Centralized Coordinator
-   Ricart--Agrawala
-   Token Passing
-   Basic Client-Server
-   Pickle
-   RMI

------------------------------------------------------------------------

# 14. Troubleshooting

## Error: Address already in use

Example:

``` text
OSError: [Errno 98] Address already in use
```

or on Windows:

``` text
OSError: [WinError 10048]
```

This usually means another program is already using the port.

Solutions:

1.  Stop the previous server.
2.  Wait a few seconds.
3.  Run again.
4.  If necessary, change the port.

On Windows:

``` cmd
netstat -ano | findstr :8000
```

Then identify and stop the process if necessary.

On Linux:

``` bash
lsof -i :8000
```

------------------------------------------------------------------------

## Error: Connection refused

Example:

``` text
ConnectionRefusedError
```

Usually this means the client started before the server.

Correct order:

``` text
Start Server
     ↓
Server listening
     ↓
Start Client
```

------------------------------------------------------------------------

## Error: ModuleNotFoundError: No module named 'Pyro4'

Install Pyro4:

``` bash
python -m pip install Pyro4
```

Then try again.

------------------------------------------------------------------------

## Client is waiting forever

For Ricart--Agrawala, make sure all required nodes are running:

``` text
Node 1
Node 2
Node 3
```

The requesting node needs replies from the other nodes.

For Token Passing, make sure:

-   Exactly one node initially owns the token.
-   The next-port values form a complete ring.
-   All nodes are running.

------------------------------------------------------------------------

## Port conflict between experiments

Do not run two programs that use the same port simultaneously.

For example:

``` text
Message Passing -> 8000
Coordinator     -> 9000
Basic IPC       -> 5000
Pickle          -> 5001
```

You can stop the previous experiment before starting another.

------------------------------------------------------------------------

# 15. Quick Run Reference

  -------------------------------------------------------------------------------------------------
  Experiment              Server/Node Command                       Client/Node Command
  ----------------------- ----------------------------------------- -------------------------------
  Message Passing         `python server.py`                        `python client.py`

  Centralized Coordinator `python server.py`                        `python client.py`

  Ricart--Agrawala        `python ricart.py 1` / `2` / `3`          Same program

  Token Passing           `python token-passing.py 9001 9002 yes`   Other nodes use next-port

  Lamport Clock           No server                                 `python lamport.py`

  Vector Clock            No server                                 `python vector_clock.py`

  Basic Client-Server     `python server_basic_ipc.py`              `python client_basic_ipc.py`

  Pickle Serialization    `python server_pickle.py`                 `python client_pickle.py`

  Pyro4 RMI               `python Calculator_server.py`             `python Calculator_client.py`
  -------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 16. Algorithm Summary

## Message Passing

``` text
Client -> Server -> Other Clients
```

Uses:

-   TCP sockets
-   Threads
-   Broadcasting

## Centralized Coordinator

``` text
Client -> Coordinator -> Grant
Client -> Coordinator -> Release
```

Uses:

-   Central queue
-   One coordinator
-   Mutual exclusion

## Ricart--Agrawala

``` text
REQUEST -> All other processes
REPLY   <- All other processes
ENTER CS
EXIT CS
Deferred REPLY
```

Uses:

-   Logical timestamps
-   Distributed mutual exclusion
-   No central coordinator

## Token Passing

``` text
Node 1 -> Node 2 -> Node 3 -> Node 1
```

Uses:

-   One circulating token
-   Token ownership for CS access

## Lamport Clock

``` text
Internal: clock += 1
Send:     clock += 1
Receive:  max(local, received) + 1
```

## Vector Clock

``` text
Internal:
V[pid] += 1

Send:
V[pid] += 1

Receive:
V[i] = max(V[i], received[i])
V[pid] += 1
```

## Basic Client-Server

``` text
Client -> numbers -> Server
Server -> sum -> Client
```

## Object Serialization

``` text
Python Object
     ↓
pickle.dumps()
     ↓
Socket
     ↓
pickle.loads()
     ↓
Python Object
```

## RMI

``` text
Client
  ↓
Pyro4.Proxy
  ↓
Network
  ↓
Pyro4 Server
  ↓
Calculator method
  ↓
Result
```

------------------------------------------------------------------------

# 17. Recommended Testing Order

If you are preparing for a lab practical, test them in this order:

### 1. Basic Client-Server

Understand:

``` text
socket()
bind()
listen()
accept()
connect()
send()
recv()
close()
```

### 2. Message Passing

Understand:

``` text
multiple clients
+
threads
+
broadcast
```

### 3. Pickle Serialization

Understand:

``` text
object
→ dumps
→ socket
→ loads
→ object
```

### 4. Lamport Clock

Understand:

``` text
logical timestamp
```

### 5. Vector Clock

Understand:

``` text
vector
+
merge
+
causality
```

### 6. Centralized Coordinator

Understand:

``` text
REQUEST
→ queue
→ GRANT
→ CS
→ RELEASE
```

### 7. Ricart--Agrawala

Understand:

``` text
REQUEST
→ timestamp comparison
→ REPLY
→ CS
→ deferred REPLY
```

### 8. Token Passing

Understand:

``` text
TOKEN
→ request?
→ CS
→ pass TOKEN
```

### 9. Pyro4 RMI

Understand:

``` text
remote object
→ URI
→ Proxy
→ remote method call
```

------------------------------------------------------------------------

# 18. Common Viva Questions

## What is a socket?

A socket is an endpoint used for communication between processes over a
network.

## Difference between TCP and UDP?

TCP is connection-oriented and reliable. UDP is connectionless and does
not guarantee delivery.

## Why use threads in the Message Passing System?

Threads allow the server to handle multiple clients concurrently.

## What is a Critical Section?

A section of code where shared resources are accessed and which must be
protected from simultaneous execution by multiple processes.

## What is Lamport's clock?

A logical clock used to establish a consistent ordering of events in a
distributed system.

## Why is `max()` used in Lamport clocks?

To ensure the receiving process's logical time is greater than the
timestamp of the received event.

## What does a vector clock represent?

It represents the logical time/state of all participating processes.

## What is the advantage of vector clocks over Lamport clocks?

Vector clocks can identify concurrency more precisely, whereas Lamport
clocks provide ordering but cannot by themselves distinguish all
concurrent events.

## What is centralized mutual exclusion?

A coordinator controls which process can enter the critical section.

## What is the disadvantage of a centralized coordinator?

The coordinator can become a bottleneck or single point of failure.

## What is Ricart--Agrawala?

A distributed mutual exclusion algorithm that uses timestamped REQUEST
and REPLY messages without a central coordinator.

## What is token passing?

A mutual exclusion approach in which a unique token circulates among
processes. The process holding the token may enter the critical section.

## What is serialization?

Converting an object into a format that can be transmitted or stored.

## What is deserialization?

Reconstructing the object from its serialized representation.

## What is RMI?

Remote Method Invocation allows a program to invoke methods on an object
running in another process or machine.

## What is Pyro4?

Pyro4 is a Python library that provides distributed object communication
and remote method invocation.

------------------------------------------------------------------------

# 19. Final Checklist Before Lab Submission

-   [ ] Python is installed.
-   [ ] All `.py` files are saved.
-   [ ] Pyro4 is installed.
-   [ ] Server files start without errors.
-   [ ] Client files connect successfully.
-   [ ] Correct ports are being used.
-   [ ] Multiple terminals are available for multi-process experiments.
-   [ ] Message Passing works with multiple clients.
-   [ ] Coordinator grants only one CS access at a time.
-   [ ] Ricart--Agrawala receives the required replies.
-   [ ] Token Passing has exactly one initial token.
-   [ ] Lamport clock updates correctly.
-   [ ] Vector clock merge works correctly.
-   [ ] Pickle object is serialized and deserialized.
-   [ ] RMI server prints a URI.
-   [ ] RMI client successfully calls both calculator methods.
-   [ ] All experiments are stopped after testing to avoid port
    conflicts.

------------------------------------------------------------------------

# 20. Important Notes

1.  Start servers before clients.
2.  For multi-node algorithms, start every required node before testing.
3.  Do not create multiple initial tokens in the Token Passing
    experiment.
4.  Do not use `pickle.loads()` on untrusted data.
5.  Keep the RMI server running while using the RMI client.
6.  If a port is busy, stop the previous program or change the port.
7.  Use `127.0.0.1`/`localhost` when all processes are running on the
    same computer.
8.  If running across different computers, replace `localhost` with the
    server's LAN IP and ensure the required ports are allowed through
    the firewall.
