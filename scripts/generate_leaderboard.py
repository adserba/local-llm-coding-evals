
import csv
from pathlib import Path

scorecard = Path("results/scorecard.csv")
output = Path("docs/leaderboard.md")

rows = []
with open(scorecard, newline="") as f:
    reader = csv.DictReader(f)
    for r in reader:
        try:
            total = float(r["total"]) if r["total"] else 0
        except:
            total = 0
        r["_total"] = total
        rows.append(r)

rows.sort(key=lambda r: r["_total"], reverse=True)

lines = []
lines.append("# Model Leaderboard\n")
lines.append("| Model | Provider | Context | Total Score | Notes |")
lines.append("|------|----------|--------|-------------|------|")

for r in rows:
    lines.append(f'| {r["model_name"]} | {r["provider"]} | {r["context"]} | {r["total"]} | {r["notes"]} |')

output.write_text("\n".join(lines))

print("Leaderboard generated at docs/leaderboard.md")
