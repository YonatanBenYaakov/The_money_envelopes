import random

# --- Base class for all strategies ---
class BaseStrategy:
    def display(self):
        return self.__class__.__name__

    def play(self, envelopes, interactive=False):
        raise NotImplementedError("Subclasses must implement play()")


# --- Strategy 1: Manual user choice ---
class ManualStrategy(BaseStrategy):
    def play(self, envelopes, interactive=False):
        if interactive:
            print("You have", len(envelopes), "envelopes to choose from (0-based index).")
            try:
                num = int(input("Pick an envelope number: "))
                if 0 <= num < len(envelopes):
                    print(f"You selected envelope with {envelopes[num].money}$")
                    return num, 1
                else:
                    print("Invalid choice, defaulting to last envelope")
                    return len(envelopes) - 1, 1
            except ValueError:
                print("Invalid input, defaulting to last envelope")
                return len(envelopes) - 1, 1
        else:
            # סימולציה – פשוט בוחר את האחרון
            return len(envelopes) - 1, 1


# --- Strategy 2: Automatic random choice ---
class RandomStrategy(BaseStrategy):
    def play(self, envelopes, interactive=False):
        idx = random.randrange(len(envelopes))
        if interactive:
            print(f"Randomly selected envelope {idx} with {envelopes[idx].money}$")
        return idx, 1


# --- Strategy 3: Stop after N maximum values ---
class NMaxStrategy(BaseStrategy):
    def __init__(self, N=3):
        self.N = N

    def play(self, envelopes, interactive=False):
        current_max = envelopes[0].money
        n_left = self.N - 1
        steps = 1
        for i in range(1, len(envelopes)):
            steps += 1
            if envelopes[i].money > current_max:
                current_max = envelopes[i].money
                n_left -= 1
                if interactive:
                    print(f"New max {current_max}$ at envelope {i}, remaining={n_left}")
                if n_left == 0:
                    return i, steps
        return len(envelopes) - 1, steps


# --- Strategy 4: Better than max of first percent group ---
class BetterThanPercentStrategy(BaseStrategy):
    def __init__(self, percent=0.25):
        self.percent = percent

    def play(self, envelopes, interactive=False):
        k = int(len(envelopes) * self.percent)
        first_group = envelopes[:k]
        max_first = max(env.money for env in first_group)
        steps = k
        if interactive:
            print(f"Max in first {int(self.percent*100)}% group: {max_first}$")
        for i in range(k, len(envelopes)):
            steps += 1
            if envelopes[i].money > max_first:
                if interactive:
                    print(f"Found a better envelope: {envelopes[i].money}$ at {i}")
                return i, steps
        return len(envelopes) - 1, steps
