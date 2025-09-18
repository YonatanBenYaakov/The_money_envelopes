import random

class Envelope:
    def __init__(self):
        self.money = random.randint(1, 1000)
        self.used = False

    def get_value(self):
        return self.money

    def __repr__(self):
        return f"Envelope({self.money}$, used={self.used})"
