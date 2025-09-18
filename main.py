from envelope import Envelope
from strategy import ManualStrategy, RandomStrategy, NMaxStrategy, BetterThanPercentStrategy

def cls(): print("\n" * 20)

envelopes = [Envelope() for _ in range(100)]
strategies = [
    ManualStrategy(),                           # user picks manually
    RandomStrategy(),                           # random choice
    NMaxStrategy(),                             # stop after N maxima
    BetterThanPercentStrategy(0.25)             # better than first 25%
]

n = -1
while n != 4:
    cls()
    for i in range(len(strategies)):
        print(i, strategies[i].display())
    print(len(strategies), "Exit")

    n = input(f'enter your choice [0-{len(strategies)}]: ')
    if n.isdigit():
        n = int(n)
        if n == 2:
            N = input("enter N max values: ")
            strategies[n].N = int(N)
        elif n == 3:
            p = input("enter 0-1 number for group size (default=0.25): ")
            try:
                strategies[n].percent = float(p)
            except ValueError:
                print("Invalid input, keeping default 0.25")
        if n != 4:
            strategies[n].play(envelopes, interactive=True)
            input('press any key to continue')
