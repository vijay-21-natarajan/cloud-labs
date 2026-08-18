#token_passing.py 

import socket
import threading
import time
import sys


class TokenRingNode:

    def __init__(
        self,
        port,
        next_host,
        next_port,
        has_token=False
    ):
        self.port = port
        self.next_host = next_host
        self.next_port = next_port

        self.has_token = has_token
        self.request_cs = False

        self.running = True

        self.lock = threading.Lock()

    def listen(self):

        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server.bind(
            ("localhost", self.port)
        )

        server.listen(5)

        print(
            f"[{self.port}] Listening for token..."
        )

        while self.running:

            conn, _ = server.accept()

            token = conn.recv(1024).decode()

            conn.close()

            if token == "TOKEN":

                print(
                    f"[{self.port}] Token received"
                )

                self.has_token = True

                # If this node requested CS,
                # enter the critical section
                if self.request_cs:

                    self.enter_critical_section()

                # Always pass the token
                self.send_token()

        server.close()

    def send_token(self):

        if not self.has_token:
            return

        try:

            s = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            s.connect(
                (
                    self.next_host,
                    self.next_port
                )
            )

            s.sendall(
                "TOKEN".encode()
            )

            s.close()

            print(
                f"[{self.port}] "
                f"Token passed to {self.next_port}"
            )

            self.has_token = False

        except Exception as e:

            print(
                f"[{self.port}] "
                f"Failed to send token: {e}"
            )

    def enter_critical_section(self):

        print(
            f"[{self.port}] "
            f">>> Entering critical section..."
        )

        time.sleep(3)

        print(
            f"[{self.port}] "
            f"<<< Exiting critical section..."
        )

        self.request_cs = False

    def start(self):

        # Start listening thread
        listener_thread = threading.Thread(
            target=self.listen,
            daemon=True
        )

        listener_thread.start()

        time.sleep(1)

        # If this node initially has token,
        # start the token circulation
        if self.has_token:

            if self.request_cs:
                self.enter_critical_section()

            self.send_token()

        # User interaction
        while self.running:

            user_input = input(
                f"[{self.port}] "
                f"Type 'request' to enter CS "
                f"or 'exit' to quit: "
            ).strip().lower()

            if user_input == "request":

                self.request_cs = True

                print(
                    f"[{self.port}] "
                    f"CS requested"
                )

            elif user_input == "exit":

                self.running = False
                break

        print(
            f"[{self.port}] Shutting down..."
        )


if __name__ == "__main__":

    port = int(sys.argv[1])

    next_port = int(sys.argv[2])

    has_token = False

    request_cs = False

    if len(sys.argv) > 3:

        has_token = (
            sys.argv[3].lower() == "yes"
        )

    if len(sys.argv) > 4:

        request_cs = (
            sys.argv[4].lower() == "yes"
        )

    node = TokenRingNode(
        port,
        "localhost",
        next_port,
        has_token
    )

    node.request_cs = request_cs

    node.start()