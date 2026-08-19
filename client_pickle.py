#client_pickle.py
'''
import socket
import pickle
class DataObject:
    def __init__(self, name, values):
        self.name = name
        self.values = values

HOST = "127.0.0.1"
PORT = 5001
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
obj = DataObject("Alice", [10, 20, 30, 40])
serialized = pickle.dumps(obj)
client.send(serialized)
response = client.recv(1024).decode()
print(response)
client.close()
''' 
import socket
import pickle
s = socket.socket()
s.connect(("localhost", 12345))
name = input("Name: ")
values = list(map(int, input("Values: ").split()))
data = {
    "name": name,
    "values": values
}
s.send(pickle.dumps(data))
result = s.recv(1024).decode()
print("Sum =", result)
s.close()

