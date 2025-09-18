

class GameResult:
    def __init__(self, chosen_amount, max_amount, steps):
        self.chosen_amount = chosen_amount      # כמה כסף בחרנו
        self.max_amount = max_amount            # המקסימום האמיתי ברשימה
        self.steps = steps                      # כמה מעטפות פתחנו
        self.success = (chosen_amount == max_amount)  # האם הצלחנו להשיג את המקסימום
        self.ratio = chosen_amount / max_amount if max_amount > 0 else 0  # יחס (כמה קרוב למקס')

    def __repr__(self):
        return (f"GameResult(chosen={self.chosen_amount}, "
                f"max={self.max_amount}, steps={self.steps}, "
                f"success={self.success}, ratio={self.ratio:.2f})")
