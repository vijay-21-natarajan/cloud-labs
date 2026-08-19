# client_basic_ipc.py 

'''
import socket
HOST = "127.0.0.1"
PORT = 5000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
message = "10 20 30 40"
client.send(message.encode())
response = client.recv(1024).decode()
print("Server Response:", response)
client.close()
'''
import socket
s = socket.socket()
s.connect(("localhost", 12345))
while True:
    data = input("Enter numbers: ")
    s.send(data.encode())
    if data == "exit":
        break
    result = s.recv(1024).decode()
    print("Sum =", result)
s.close()

