#client_centralized.py 

import socket
import time

HOST = "localhost"
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((HOST, PORT))

    print("[Client] Connected to coordinator")

    # Request access to Critical Section
    s.sendall("REQUEST_CS".encode())

    print("[Client] Requested access to CS")

    # Wait for coordinator
    msg = s.recv(1024).decode()

    if msg == "GRANT_CS":

        print("[Client] Entering critical section")

        # Simulate work
        time.sleep(3)

        print("[Client] Leaving critical section")

        # Release Critical Section
        s.sendall("RELEASE_CS".encode())

        print("[Client] Released CS")