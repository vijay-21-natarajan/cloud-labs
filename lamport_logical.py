# lamport_logical.py 

class Process:

    def __init__(self, pid):
        self.pid = pid
        self.clock = 0

    def internal_event(self):
        self.clock += 1
        print(
            f"Process {self.pid} internal event "
            f"-> Clock: {self.clock}"
        )

    def send_event(self):
        self.clock += 1

        print(
            f"Process {self.pid} sends message "
            f"-> Clock: {self.clock}"
        )

        return self.clock

    def receive_event(self, recv_time):
        self.clock = max(
            self.clock,
            recv_time
        ) + 1

        print(
            f"Process {self.pid} received message "
            f"-> Clock: {self.clock}"
        )


# Example simulation

P1 = Process(1)
P2 = Process(2)

P1.internal_event()      # E1

t = P1.send_event()      # E2: Send message

P2.receive_event(t)      # E3: Receive message

P2.internal_event()      # E4