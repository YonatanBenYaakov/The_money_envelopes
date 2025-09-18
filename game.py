
from game_result import GameResult

class Game:
    def __init__(self, envelopes, strategy,interactive=False):
        self.envelopes = envelopes
        self.strategy = strategy
        self.interactive = interactive

    def play(self):
        # מפעילים את האסטרטגיה במצב אוטומטי (לא אינטראקטיבי)
        chosen_index, steps = self.strategy.play(self.envelopes, interactive=self.interactive)

        # אם האסטרטגיה לא בחרה כלום – ניקח את האחרונה
        if chosen_index is None:
            chosen_index = len(self.envelopes) - 1

        chosen_amount = self.envelopes[chosen_index].get_value()
        max_amount = max(env.get_value() for env in self.envelopes)

        return GameResult(chosen_amount, max_amount, steps)
