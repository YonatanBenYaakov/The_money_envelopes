import csv
import glob
import os
from collections import defaultdict

def load_matches_from_csv(file):
    matches = []
    with open(file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            matches.append(row)
    return matches

def aggregate_results(folders=["."]):
    points = defaultdict(int)
    wins = defaultdict(int)
    losses = defaultdict(int)
    total_games = defaultdict(int)

    for folder in folders:
        for file in glob.glob(os.path.join(folder, "*.csv")):
            matches = load_matches_from_csv(file)
            for row in matches:
                s1, s2, winner = row["Strategy1"], row["Strategy2"], row["Winner"]
                total_games[s1] += 1
                total_games[s2] += 1
                if winner == s1:
                    points[s1] += 3
                    wins[s1] += 1
                    losses[s2] += 1
                elif winner == s2:
                    points[s2] += 3
                    wins[s2] += 1
                    losses[s1] += 1
                else:  # תיקו או לא צוין מנצח
                    points[s1] += 1
                    points[s2] += 1

    ranking = []
    for strategy in points.keys():
        ranking.append({
            "Strategy": strategy,
            "Games": total_games[strategy],
            "Wins": wins[strategy],
            "Losses": losses[strategy],
            "Points": points[strategy]
        })

    ranking.sort(key=lambda x: (-x["Points"], -x["Wins"]))
    return ranking

if __name__ == "__main__":
    results = aggregate_results([".", "results"])
    print("=== Final Ranking Across All Tournaments ===")
    if not results:
        print(" No results found. Make sure CSV files are in current or results/ folder.")
    else:
        for row in results:
            print(f"{row['Strategy']:25} Games:{row['Games']:3} Wins:{row['Wins']:3} Losses:{row['Losses']:3} Points:{row['Points']:3}")

        # שמירה ל-CSV
        with open("final_ranking.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Strategy", "Games", "Wins", "Losses", "Points"])
            writer.writeheader()
            writer.writerows(results)
        print("\n Final ranking saved to final_ranking.csv")
