import random

# --- Base class for all strategies ---
class BaseStrategy:
    def __init__(self, envelopes):
        self.envelopes = envelopes

    def display(self):
        return self.__class__.__name__

    def play(self):
        print(f"\nRunning {self.display()} strategy...")
        self.perform_strategy()

    def perform_strategy(self):
        # Child classes must override this
        raise NotImplementedError("Subclasses must implement perform_strategy()")


# --- Strategy 1: Manual user choice ---
class ManualStrategy(BaseStrategy):
    def perform_strategy(self):
        print("You have 100 envelopes to choose from (1-100).")

        try:
            num = int(input("Pick an envelope number: "))
            if 0 < num+1 <= len(self.envelopes):
                print(f"You selected envelope with {self.envelopes[num+1].money}$")
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")


# --- Strategy 2: Automatic random choice ---
class Automatic_BaseStrategy(BaseStrategy):
    def perform_strategy(self):
        choice = random.choice(self.envelopes)
        print(f"Randomly selected envelope with {choice.money}$")


# --- Strategy 3: Stop after N maximum values ---
class N_max_strategy(BaseStrategy):
    def __init__(self, envelopes, N=3): # if not changed the N is 3
        super().__init__(envelopes)
        self.N = N

    def perform_strategy(self):
        current_max = self.envelopes[0].money
        n_left = self.N - 1  # we already counted the first max

        for i in range(1, len(self.envelopes)):
            if self.envelopes[i].money > current_max:
                current_max = self.envelopes[i].money
                n_left -= 1
                print(f"Found new max: {current_max}$ at envelope {i}, remaining={n_left}")
                if n_left == 0:
                    print(f"Stopped at envelope {i} with {current_max}$")
                    return

        print("Did not reach the required N maximums")


# --- Strategy 4: Find envelope better than X% group max ---
class More_then_N_percent_group_strategy(BaseStrategy):
    def __init__(self, envelopes, percent=0.25): # if not changed the N is 25%
        super().__init__(envelopes)
        self.percent = percent

    def perform_strategy(self):
        k = int(len(self.envelopes) * self.percent)
        first_group = self.envelopes[:k]
        max_first = max(env.money for env in first_group) # chooses the max out of all envelopes that are in the group
        print(f"Max in the first {int(self.percent*100)}% group: {max_first}$")

        for env in self.envelopes[k:]:
            if env.money > max_first:
                print(f"Found a better envelope: {env.money}$")
                return
        print("No better envelope found")
