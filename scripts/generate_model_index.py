#!/usr/bin/env python3
"""
Generate docs/models-tested.md from results/scorecard.csv
"""
from __future__ import annotations
import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCORECARD = REPO_ROOT / "results" / "scorecard.csv"
OUT = REPO_ROOT / "docs" / "models-tested.md"

rows = []
with open(SCORECARD, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)

def num(value: str) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0

rows.sort(key=lambda r: num(r.get("total", "0")), reverse=True)

lines = [
    "# Tested Models",
    "",
    "| Model | Provider | Context | Total | Verdict |",
    "|---|---|---:|---:|---|",
]
for r in rows:
    lines.append(
        f'| {r.get("model_name","")} | {r.get("provider","")} | {r.get("context","")} | {r.get("total","")} | {r.get("verdict","")} |'
    )
lines.append("")
lines.append("See also: `docs/leaderboard.md` and individual notes under `results/models/`.")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT}")
