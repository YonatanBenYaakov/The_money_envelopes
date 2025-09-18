import random
from game import Game
from game_result import GameResult

# --- Base Tournament ---
class Tournament:
    def __init__(self, strategies, envelopes_factory):
        """
        strategies: list of strategies
        envelopes_factory: function that returns a fresh list of envelopes
        """
        self.strategies = strategies
        self.envelopes_factory = envelopes_factory

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")


# --- DeathMatchTournament ---
class DeathMatchTournament(Tournament):
    def __init__(self, strategies, envelopes_factory, win_goal=3):
        super().__init__(strategies, envelopes_factory)
        self.win_goal = win_goal

    def run(self):
        if len(self.strategies) != 2:
            raise ValueError("DeathMatchTournament requires exactly 2 strategies")

        scores = {s.display(): 0 for s in self.strategies}
        history = []

        while max(scores.values()) < self.win_goal:
            envelopes = self.envelopes_factory()
            results = [Game(envelopes, s).play() for s in self.strategies]

            # מי ניצח
            if results[0].chosen_amount > results[1].chosen_amount:
                winner = self.strategies[0].display()
            elif results[1].chosen_amount > results[0].chosen_amount:
                winner = self.strategies[1].display()
            else:
                winner = None  # תיקו

            if winner:
                scores[winner] += 1
            history.append((results[0], results[1], winner))

        winner = max(scores, key=scores.get)
        return {"winner": winner, "scores": scores, "history": history}


# --- RoundRobinTournament ---
class RoundRobinTournament(Tournament):
    def __init__(self, strategies, envelopes_factory, rounds=1):
        super().__init__(strategies, envelopes_factory)
        self.rounds = rounds

    def run(self):
        points = {s.display(): 0 for s in self.strategies}
        history = []

        for _ in range(self.rounds):
            for i in range(len(self.strategies)):
                for j in range(i + 1, len(self.strategies)):
                    s1, s2 = self.strategies[i], self.strategies[j]
                    envelopes = self.envelopes_factory()
                    r1, r2 = Game(envelopes, s1).play(), Game(envelopes, s2).play()

                    if r1.chosen_amount > r2.chosen_amount:
                        points[s1.display()] += 3
                        winner = s1.display()
                    elif r2.chosen_amount > r1.chosen_amount:
                        points[s2.display()] += 3
                        winner = s2.display()
                    else:
                        points[s1.display()] += 1
                        points[s2.display()] += 1
                        winner = None

                    history.append((s1.display(), r1, s2.display(), r2, winner))

        return {"points": points, "history": history}


# --- EliminationTournament ---
class EliminationTournament(Tournament):
    def __init__(self, strategies, envelopes_factory):
        super().__init__(strategies, envelopes_factory)

    def run(self):
        round_num = 1
        competitors = list(self.strategies)
        history = []

        while len(competitors) > 1:
            next_round = []
            random.shuffle(competitors)
            for i in range(0, len(competitors), 2):
                if i + 1 >= len(competitors):
                    # bye
                    next_round.append(competitors[i])
                    continue

                s1, s2 = competitors[i], competitors[i + 1]
                envelopes = self.envelopes_factory()
                r1, r2 = Game(envelopes, s1).play(), Game(envelopes, s2).play()

                if r1.chosen_amount >= r2.chosen_amount:
                    winner = s1
                else:
                    winner = s2

                next_round.append(winner)
                history.append((s1.display(), r1, s2.display(), r2, winner.display()))

            competitors = next_round
            round_num += 1

        return {"winner": competitors[0].display(), "history": history}


# --- LeagueTournament ---
class LeagueTournament(Tournament):
    def run(self):
        table = {s.display(): {"games": 0, "wins": 0, "losses": 0, "points": 0}
                 for s in self.strategies}
        history = []

        for i in range(len(self.strategies)):
            for j in range(len(self.strategies)):
                if i == j: continue
                s1, s2 = self.strategies[i], self.strategies[j]
                envelopes = self.envelopes_factory()
                r1, r2 = Game(envelopes, s1).play(), Game(envelopes, s2).play()

                table[s1.display()]["games"] += 1
                table[s2.display()]["games"] += 1

                if r1.chosen_amount > r2.chosen_amount:
                    table[s1.display()]["wins"] += 1
                    table[s2.display()]["losses"] += 1
                    table[s1.display()]["points"] += 3
                    winner = s1.display()
                elif r2.chosen_amount > r1.chosen_amount:
                    table[s2.display()]["wins"] += 1
                    table[s1.display()]["losses"] += 1
                    table[s2.display()]["points"] += 3
                    winner = s2.display()
                else:
                    table[s1.display()]["points"] += 1
                    table[s2.display()]["points"] += 1
                    winner = None

                history.append((s1.display(), r1, s2.display(), r2, winner))

        return {"table": table, "history": history}


# --- ChampionshipTournament ---
class ChampionshipTournament(Tournament):
    def __init__(self, strategies, envelopes_factory, groups=2):
        super().__init__(strategies, envelopes_factory)
        self.groups_num = groups

    def run(self):
        random.shuffle(self.strategies)
        groups = [self.strategies[i::self.groups_num] for i in range(self.groups_num)]
        group_results = []

        # שלב בתים
        for g in groups:
            rr = RoundRobinTournament(g, self.envelopes_factory, rounds=1)
            result = rr.run()
            group_results.append(result)

        # לוקחים את 2 הראשונים מכל בית
        qualifiers = []
        for res, g in zip(group_results, groups):
            sorted_group = sorted(res["points"].items(), key=lambda x: -x[1])
            top2_names = [name for name, _ in sorted_group[:2]]
            qualifiers.extend([s for s in g if s.display() in top2_names])

        # פלייאוף (הדחות)
        elim = EliminationTournament(qualifiers, self.envelopes_factory)
        elim_result = elim.run()

        return {"groups": group_results, "playoff": elim_result}
