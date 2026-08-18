# client_message.py
import socket
import threading

HOST = "127.0.0.1"
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

print("<CONNECTED> to server.")


# Receive messages continuously
def receive_messages(client):
    while True:
        try:
            data = client.recv(1024).decode()

            if not data:
                break

            print(f"<CLIENT> Received from Server: {data}")

        except:
            break


# Start receiving thread
thread = threading.Thread(
    target=receive_messages,
    args=(client,)
)

thread.start()


# Send messages
while True:
    msg = input("Enter message: ")

    client.send(msg.encode())

    if msg.lower() == "bye":
        break


client.close()