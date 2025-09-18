from envelope import Envelope
from strategy import ManualStrategy, RandomStrategy, NMaxStrategy, BetterThanPercentStrategy
from game import Game

# מייצרים 100 מעטפות
envelopes = [Envelope() for _ in range(100)]

# בוחרים אסטרטגיה
strategy = ManualStrategy()

# מריצים משחק
g = Game(envelopes, strategy, interactive=True)
result = g.play()

print(result)