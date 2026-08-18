#server_message.py
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

clients = []


def handle_client(client_socket, addr):
    print(f"<Connected> {addr} connected.")

    while True:
        try:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            print(f"<{addr}> {data}")

            if data.lower() == "bye":
                break

            # Broadcast message to other clients
            for client in clients:
                if client != client_socket:
                    client.send(f"<{addr}> {data}".encode())

        except:
            break

    print(f"<Disconnected> {addr} disconnected.")

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()


# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

print(f"<Server> Server listening on {HOST}:{PORT}")


while True:
    client_socket, addr = server.accept()

    clients.append(client_socket)

    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, addr)
    )

    thread.start()