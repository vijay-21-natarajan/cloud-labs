# vector_clock.py

class VectorClock:

    def __init__(self, pid, n):
        self.pid = pid
        self.n = n
        self.vector = [0] * n

    def internal_event(self):
        self.vector[self.pid] += 1

        print(
            f"Process {self.pid} internal event "
            f"-> {self.vector}"
        )

    def send_event(self):
        self.vector[self.pid] += 1

        print(
            f"Process {self.pid} sends message "
            f"-> {self.vector}"
        )

        return list(self.vector)

    def receive_event(self, received_vector):

        for i in range(self.n):
            self.vector[i] = max(
                self.vector[i],
                received_vector[i]
            )

        # Increment receiver's own component
        self.vector[self.pid] += 1

        print(
            f"Process {self.pid} received message "
            f"-> {self.vector}"
        )


# Example simulation with 3 processes

P0 = VectorClock(0, 3)
P1 = VectorClock(1, 3)
P2 = VectorClock(2, 3)


# E1
P0.internal_event()

# E2: P0 sends to P1
msg = P0.send_event()

# E3: P1 receives
P1.receive_event(msg)

# E4: P2 internal event
P2.internal_event()

# E5: P1 sends to P2
msg2 = P1.send_event()

# E6: P2 receives
P2.receive_event(msg2)