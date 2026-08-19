# server_basic_ipc.py  
'''
import socket
HOST = "127.0.0.1"
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("Server is waiting for connection...")
conn, addr = server.accept()
print("Connected by:", addr)
message = conn.recv(1024).decode()
print("Client sent:", message)
numbers = list(map(int, message.split()))
total = sum(numbers)
conn.send(f"Sum = {total}".encode())
conn.close()
server.close()
''' 
import socket
s = socket.socket()
s.bind(("localhost", 12345))
s.listen(1)
c, addr = s.accept()
print("Client connected")
while True:
    data = c.recv(1024).decode()
    if data == "exit":
        break
    nums = map(int, data.split())
    total = sum(nums)
    c.send(str(total).encode())
c.close()
s.close()
