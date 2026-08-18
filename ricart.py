#ricart.py

import socket
import threading
import time
import sys

HOST = "localhost"

NODES = {
    1: 9001,
    2: 9002,
    3: 9003
}

my_id = int(sys.argv[1])
my_port = NODES[my_id]

# Ricart-Agrawala state
lamport_clock = 0
request_timestamp = None
requesting_cs = False

replies_received = 0
replies_needed = len(NODES) - 1

deferred_replies = []

lock = threading.Lock()


def send_message(to_port, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, to_port))
            s.sendall(message.encode())
    except Exception as e:
        print(f"[{my_id}] Failed to send message: {e}")


def listen():
    global lamport_clock
    global replies_received

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, my_port))
    server.listen()

    print(f"[{my_id}] Listening on port {my_port}")

    while True:

        conn, addr = server.accept()

        msg = conn.recv(1024).decode()
        conn.close()

        if not msg:
            continue

        parts = msg.split()

        # ------------------------------------------------
        # REQUEST
        # ------------------------------------------------

        if parts[0] == "REQUEST":

            req_ts = int(parts[1])
            sender_id = int(parts[2])

            with lock:

                # Update Lamport clock
                lamport_clock = max(
                    lamport_clock,
                    req_ts
                ) + 1

                print(
                    f"[{my_id}] Received REQUEST "
                    f"from Node {sender_id} "
                    f"(timestamp={req_ts})"
                )

                # If I am NOT requesting CS,
                # immediately send REPLY
                if not requesting_cs:

                    send_message(
                        NODES[sender_id],
                        f"REPLY {my_id}"
                    )

                # If I am requesting CS,
                # compare timestamps
                elif (
                    request_timestamp,
                    my_id
                ) < (
                    req_ts,
                    sender_id
                ):

                    # My request has priority
                    deferred_replies.append(sender_id)

                else:

                    # Other node has priority
                    send_message(
                        NODES[sender_id],
                        f"REPLY {my_id}"
                    )

        # ------------------------------------------------
        # REPLY
        # ------------------------------------------------

        elif parts[0] == "REPLY":

            sender_id = int(parts[1])

            with lock:

                replies_received += 1

                print(
                    f"[{my_id}] Received REPLY "
                    f"from Node {sender_id} "
                    f"({replies_received}/{replies_needed})"
                )


def request_cs():

    global lamport_clock
    global request_timestamp
    global requesting_cs
    global replies_received

    with lock:

        # Increment Lamport clock
        lamport_clock += 1

        request_timestamp = lamport_clock

        requesting_cs = True
        replies_received = 0

        print(
            f"[{my_id}] Requesting CS "
            f"(timestamp={request_timestamp})"
        )

    # Send REQUEST to every other node
    for pid, port in NODES.items():

        if pid != my_id:

            send_message(
                port,
                f"REQUEST {request_timestamp} {my_id}"
            )

    # Wait for N-1 replies
    while True:

        with lock:

            if replies_received >= replies_needed:
                break

        time.sleep(0.1)

    # ------------------------------------------------
    # Critical Section
    # ------------------------------------------------

    print(f"[{my_id}] >>> ENTERING CRITICAL SECTION")

    time.sleep(3)

    print(f"[{my_id}] <<< EXITING CRITICAL SECTION")

    # ------------------------------------------------
    # Send deferred replies
    # ------------------------------------------------

    with lock:

        requesting_cs = False
        request_timestamp = None

        pending = deferred_replies.copy()
        deferred_replies.clear()

    for pid in pending:

        print(
            f"[{my_id}] Sending deferred REPLY "
            f"to Node {pid}"
        )

        send_message(
            NODES[pid],
            f"REPLY {my_id}"
        )


# ------------------------------------------------
# Start listener
# ------------------------------------------------

threading.Thread(
    target=listen,
    daemon=True
).start()


time.sleep(1)


# ------------------------------------------------
# Main loop
# ------------------------------------------------

while True:

    inp = input(
        f"[{my_id}] Press Enter to request CS "
        f"or type 'exit': "
    )

    if inp.strip().lower() == "exit":
        break

    request_cs()