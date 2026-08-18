#Calculator_server.py 

import Pyro4

@Pyro4.expose
class Calculator:

    def add_numbers(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b


daemon = Pyro4.Daemon()

uri = daemon.register(Calculator())

print("Server is ready.")
print("URI:", uri)

daemon.requestLoop()

