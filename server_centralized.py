#server_centralized.py

import socket
import threading
from queue import Queue

HOST = "localhost"
PORT = 9000

request_queue = Queue()
cs_in_use = False

lock = threading.Lock()


def process_queue():
    global cs_in_use

    if not cs_in_use and not request_queue.empty():
        conn = request_queue.get()

        cs_in_use = True

        conn.sendall("GRANT_CS".encode())


def handle_client(conn, addr):
    global cs_in_use

    print(f"[+] Connected by {addr}")

    while True:
        try:
            msg = conn.recv(1024).decode()

            if not msg:
                break

            if msg == "REQUEST_CS":

                print(f"[{addr}] Requested CS")

                with lock:
                    request_queue.put(conn)
                    process_queue()

            elif msg == "RELEASE_CS":

                print(f"[{addr}] Released CS")

                with lock:
                    cs_in_use = False
                    process_queue()

        except:
            break

    conn.close()
    print(f"[-] Disconnected: {addr}")


# Create coordinator socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.bind((HOST, PORT))
    s.listen()

    print(f"[Coordinator] Listening on {HOST}:{PORT}")

    while True:

        conn, addr = s.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )

        thread.start()