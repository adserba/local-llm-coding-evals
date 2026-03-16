#!/usr/bin/env python3
"""
Heuristic auto-scoring for the arcade-flight benchmark after a model has edited the repo.

Important:
- This is a helper, not a perfect judge.
- It is strongest for tasks 1, 2, and 4.
- Task 3 and task 5 still benefit from manual review.
"""

from __future__ import annotations
import argparse
import csv
import datetime as dt
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = REPO_ROOT / "benchmarks" / "arcade-flight"
AUTO_SCORE_DIR = REPO_ROOT / "results" / "auto-scores"
SCORECARD = REPO_ROOT / "results" / "scorecard.csv"

def read(rel: str) -> str:
    return (APP_DIR / rel).read_text(encoding="utf-8")

def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE | re.MULTILINE) for p in patterns)

def score_task1(index_html: str, styles_css: str, app_js: str) -> dict:
    notes = []
    score = 0

    checks = {
        "pause overlay markup": has_any(index_html, [r'pause', r'resume', r'restart']),
        "escape key handling": has_any(app_js, [r'escape']),
        "pause state": has_any(app_js, [r'paused', r'isPaused']),
        "resume button logic": has_any(app_js, [r'resume']),
        "restart button logic": has_any(app_js, [r'restart']),
        "dim/background overlay": has_any(styles_css, [r'rgba\(.+0\.[3-9]', r'backdrop', r'overlay']),
    }

    for label, ok in checks.items():
        if ok:
            score += 1.5 if label in {"pause overlay markup", "escape key handling", "pause state"} else 1.0
            notes.append(f"yes: {label}")
        else:
            notes.append(f"no: {label}")

    return {"task": "task1_feature_addition", "score": round(min(score, 10), 1), "notes": notes}

def score_task2(index_html: str, styles_css: str, app_js: str) -> dict:
    notes = []
    score = 0

    checks = {
        "speed label updated": has_any(app_js, [r'speedLabel\.textContent', r'getElementById\(["\']speed["\']\).*textContent', r'renderHud.*speed']),
        "blur or visibility reset": has_any(app_js, [r'blur', r'visibilitychange', r'keys\s*=\s*\{\}', r'for\s*\(.+keys']),
        "camera smoothing present": has_any(app_js, [r'cameraX.*0\.[0-2][0-9]', r'lerp', r'smooth']),
        "bug-fix explanation comment": has_any(app_js + index_html, [r'fix', r'jitter', r'stuck controls', r'stale speed']),
    }

    if checks["speed label updated"]:
        score += 3
        notes.append("yes: speed label update logic found")
    else:
        notes.append("no: speed label update logic not found")

    if checks["blur or visibility reset"]:
        score += 3
        notes.append("yes: key reset on blur/visibility found")
    else:
        notes.append("no: key reset on blur/visibility not found")

    if checks["camera smoothing present"]:
        score += 2
        notes.append("yes: camera smoothing adjustment found")
    else:
        notes.append("no: camera smoothing adjustment not found")

    if checks["bug-fix explanation comment"]:
        score += 1
        notes.append("yes: explanation/comment signal found")
    else:
        notes.append("no: explanation/comment signal not found")

    if score >= 6:
        score += 1

    return {"task": "task2_bug_fix", "score": round(min(score, 10), 1), "notes": notes}

def score_task3(index_html: str, styles_css: str, app_js: str) -> dict:
    notes = []
    score = 0

    function_count = len(re.findall(r'function\s+\w+\s*\(', app_js))
    const_count = len(re.findall(r'const\s+\w+\s*=', app_js))
    duplicated_update_calls = len(re.findall(r'update\w+\(', app_js))

    if function_count >= 8:
        score += 3
        notes.append(f"yes: function count looks refactored ({function_count})")
    else:
        notes.append(f"partial: limited function extraction ({function_count})")

    if has_any(app_js, [r'handleThrottle', r'handleTurn', r'handlePitch', r'renderHud', r'resetGame']):
        score += 3
        notes.append("yes: clearer naming present")
    else:
        notes.append("partial: naming improvements not obvious")

    if duplicated_update_calls >= 4:
        score += 2
        notes.append("yes: structured update flow still present")
    else:
        notes.append("partial: update flow unclear")

    if const_count >= 5:
        score += 1
        notes.append("yes: constants/helpers present")
    else:
        notes.append("partial: few constants/helpers")

    return {"task": "task3_refactor", "score": round(min(score, 10), 1), "notes": notes}

def score_task4(readme_md: str, index_html: str, styles_css: str, app_js: str) -> dict:
    notes = []
    score = 0

    readme_has_settings = has_any(readme_md, [r'^##\s+settings', r'^###\s+settings'])
    readme_has_controls = has_any(readme_md, [r'escape', r'resume', r'restart', r'controls'])
    overlay_matches = has_any(index_html + app_js, [r'hint', r'controls', r'escape', r'resume', r'restart'])

    if readme_has_settings:
        score += 4
        notes.append("yes: README settings section found")
    else:
        notes.append("no: README settings section not found")

    if readme_has_controls:
        score += 3
        notes.append("yes: README controls text found")
    else:
        notes.append("no: README controls text not found")

    if overlay_matches:
        score += 2
        notes.append("yes: in-game overlay/control text present")
    else:
        notes.append("no: in-game overlay/control text not found")

    return {"task": "task4_repo_aware_change", "score": round(min(score, 10), 1), "notes": notes}

def score_task5(index_html: str, styles_css: str, app_js: str) -> dict:
    notes = []
    score = 0

    keeps_layout = not has_any(index_html, [r'canvas', r'three\.js', r'<svg'])
    restart_resets_camera = has_any(app_js, [r'initialState', r'cameraX\s*=\s*initialState\.cameraX', r'cameraY\s*=\s*initialState\.cameraY', r'reset.*camera'])

    if keeps_layout:
        score += 4
        notes.append("yes: existing layout style appears preserved")
    else:
        notes.append("no: major layout rewrite signal found")

    if restart_resets_camera:
        score += 4
        notes.append("yes: restart preserves/resets camera state")
    else:
        notes.append("no: explicit camera reset logic not found")

    if has_any(app_js, [r'patch', r'minimal']):
        score += 1
        notes.append("yes: minimal patch signal found")
    else:
        notes.append("partial: no minimal patch signal found")

    return {"task": "task5_follow_up_correction", "score": round(min(score, 10), 1), "notes": notes}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Model name to store in the score file")
    parser.add_argument("--provider", default="ollama")
    parser.add_argument("--context", default="")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--append-scorecard", action="store_true")
    args = parser.parse_args()

    index_html = read("index.html")
    styles_css = read("styles.css")
    app_js = read("app.js")
    readme_md = read("README.md")

    results = [
        score_task1(index_html, styles_css, app_js),
        score_task2(index_html, styles_css, app_js),
        score_task3(index_html, styles_css, app_js),
        score_task4(readme_md, index_html, styles_css, app_js),
        score_task5(index_html, styles_css, app_js),
    ]
    total = round(sum(item["score"] for item in results), 1)

    verdict = (
        "excellent local daily-driver" if total >= 45 else
        "strong, likely worth keeping" if total >= 38 else
        "usable with caution" if total >= 30 else
        "weak or inconsistent" if total >= 20 else
        "not recommended"
    )

    payload = {
        "model_name": args.model,
        "provider": args.provider,
        "context": args.context,
        "date_tested": dt.date.today().isoformat(),
        "results": results,
        "total": total,
        "verdict": verdict,
        "warning": "Heuristic score only. Manual review is still recommended, especially for task 3 and task 5.",
    }

    AUTO_SCORE_DIR.mkdir(parents=True, exist_ok=True)
    slug = args.model.replace(":", "-").replace("/", "-").replace(" ", "_")
    out_file = AUTO_SCORE_DIR / f"{slug}.json"

    if args.write_json:
        out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote {out_file}")

    print(json.dumps(payload, indent=2))

    if args.append_scorecard:
        needs_header = not SCORECARD.exists()
        with open(SCORECARD, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if needs_header:
                writer.writerow(["model_name","date_tested","provider","context","task1","task2","task3","task4","task5","total","verdict","notes"])
            writer.writerow([
                args.model,
                payload["date_tested"],
                args.provider,
                args.context,
                results[0]["score"],
                results[1]["score"],
                results[2]["score"],
                results[3]["score"],
                results[4]["score"],
                total,
                verdict,
                "auto-scored heuristic run",
            ])
        print(f"Appended to {SCORECARD}")

if __name__ == "__main__":
    main()
