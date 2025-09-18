import csv
from envelope import Envelope
from strategy import RandomStrategy, NMaxStrategy, BetterThanPercentStrategy
from tournament import DeathMatchTournament, RoundRobinTournament, EliminationTournament, LeagueTournament, ChampionshipTournament

def make_envelopes():
    return [Envelope() for _ in range(100)]

strategies = [
    RandomStrategy(),
    NMaxStrategy(),
    BetterThanPercentStrategy(0.25)
]

# פונקציה לשמירת היסטוריה ל-CSV
def save_history_to_csv(filename, history):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Strategy1", "Chosen1", "Max1", "Success1",
                         "Strategy2", "Chosen2", "Max2", "Success2", "Winner"])
        for match in history:
            if len(match) == 3:  # DeathMatch
                r1, r2, winner = match
                s1, s2 = "Strategy1", "Strategy2"
            else:  # כל השאר
                s1, r1, s2, r2, winner = match
            writer.writerow([
                s1, r1.chosen_amount, r1.max_amount, r1.success,
                s2, r2.chosen_amount, r2.max_amount, r2.success,
                winner
            ])


# --- DeathMatch ---
print("\n=== DeathMatch Tournament ===")
dm = DeathMatchTournament(strategies[:2], make_envelopes, win_goal=2)
result = dm.run()
print(f"Winner: {result['winner']}")
print("Scores:", result["scores"])
save_history_to_csv("deathmatch.csv", result["history"])


# --- RoundRobin ---
print("\n=== RoundRobin Tournament ===")
rr = RoundRobinTournament(strategies, make_envelopes, rounds=2)
result = rr.run()
print("Final Points Table:")
for name, pts in result["points"].items():
    print(f"  {name:25} {pts:3} pts")
save_history_to_csv("roundrobin.csv", result["history"])


# --- Elimination ---
print("\n=== Elimination Tournament ===")
elim = EliminationTournament(strategies, make_envelopes)
result = elim.run()
print(f"Winner: {result['winner']}")
save_history_to_csv("elimination.csv", result["history"])


# --- League ---
print("\n=== League Tournament ===")
league = LeagueTournament(strategies, make_envelopes)
result = league.run()
print("League Table:")
for name, stats in result["table"].items():
    print(f"  {name:25} W:{stats['wins']} L:{stats['losses']} Pts:{stats['points']}")
save_history_to_csv("league.csv", result["history"])


# --- Championship ---
print("\n=== Championship Tournament ===")
champ = ChampionshipTournament(strategies, make_envelopes, groups=2)
result = champ.run()
print(f"Champion: {result['playoff']['winner']}")
save_history_to_csv("championship.csv", result["playoff"]["history"])
