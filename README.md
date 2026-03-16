# Local Model Eval Pack

A reusable, GitHub-friendly benchmark pack for testing local coding models in Continue (or any editor workflow).

## Goal

Use the same small repo, prompts, and scoring rules every time you try a new model.
This lets you compare models fairly over time instead of judging them from one flashy demo.

## What this pack includes

- `benchmarks/arcade-flight/` — a tiny multi-file HTML/CSS/JS app to edit
- `docs/tasks.md` — the exact benchmark tasks
- `docs/scoring-rubric.md` — how to score each run
- `templates/model-report.md` — per-model report template
- `results/scorecard.csv` — running leaderboard
- `results/example-model-report.md` — example filled report
- `.github/ISSUE_TEMPLATE/model-eval.md` — optional GitHub issue template

## Recommended workflow

1. Open `benchmarks/arcade-flight/` in VS Code.
2. Pick one model in Continue.
3. Reset to a clean state before each task.
4. Run the exact prompt from `docs/tasks.md`.
5. Test the result manually.
6. Score it using `docs/scoring-rubric.md`.
7. Add the results to `results/scorecard.csv`.
8. Create a report from `templates/model-report.md`.

## Suggested git workflow

```bash
git init
git add .
git commit -m "Initial local model eval pack"
```

For each model or run:

```bash
git checkout -- .
git clean -fd
# run task(s)
git status
git diff
```

## Suggested naming convention

Use names like:

- `qwen3.5-9b-q4`
- `qwen2.5-coder-14b`
- `deepseek-coder-v2-lite`
- `llama3.1-8b-instruct`

## How to rank models

Do not rank on looks alone. Prioritize:

1. Correctness
2. Precision of edits
3. Instruction following
4. Recovery after follow-up correction
5. Code quality

## Minimal benchmark set

The three fastest tasks are:

1. Bug fix
2. Small feature addition
3. Follow-up correction

That is enough for a quick decision.

## Full benchmark set

See `docs/tasks.md`.

## Notes

This pack is intentionally small. The aim is not to prove which model is best in the world.
The aim is to find which model is best for **your actual local workflow**.
