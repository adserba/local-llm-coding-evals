# Local LLM Coding Evals

A reproducible benchmark framework for evaluating **local coding models** (Ollama and similar) using realistic development tasks.

This repository helps determine which models work best in **real coding workflows**, especially when used with tools like **Continue.dev**, AI coding assistants, or editor integrations.

Unlike many comparisons that rely on synthetic benchmarks or single prompts, this project evaluates models on **editing an existing codebase**.

---

# Goal

Use the same:

* repository
* prompts
* scoring rules

every time you test a new model.

This allows you to **compare models fairly over time** instead of judging them from a single impressive demo.

---

# What This Benchmark Includes

### Benchmark Project

```text
benchmarks/arcade-flight/
```

A small intentionally imperfect **multi-file web app** representing a prototype arcade flight game.

Files:

```
index.html
styles.css
app.js
README.md
```

The project includes built-in flaws so models can be evaluated on realistic tasks:

* jerky camera follow behaviour
* stale HUD speed display
* keys sticking after tab switching
* missing pause system
* duplicated logic
* incomplete documentation

---

### Benchmark Tasks

The benchmark evaluates five realistic development scenarios:

| Task                 | Description                                       |
| -------------------- | ------------------------------------------------- |
| Feature Addition     | Add a pause system with overlay                   |
| Bug Fixing           | Diagnose and fix runtime issues                   |
| Refactoring          | Improve code structure without changing behaviour |
| Repository Awareness | Synchronize documentation with code               |
| Follow-Up Correction | Modify a previous solution under constraints      |

Task prompts are stored in:

```
prompts/
```

This ensures **repeatable evaluation across models**.

---

# Repository Structure

```
local-llm-coding-evals
│
├── benchmarks/
│   └── arcade-flight/
│
├── prompts/
│
├── scripts/
│   ├── run_ollama_eval.py
│   ├── auto_score.py
│   ├── generate_leaderboard.py
│   └── generate_model_index.py
│
├── docs/
│   ├── leaderboard.md
│   ├── models-tested.md
│   ├── tasks.md
│   └── scoring-rubric.md
│
├── results/
│   ├── raw-runs/
│   ├── auto-scores/
│   ├── models/
│   └── scorecard.csv
│
└── templates/
```

---

# Quick Start (Manual Benchmark)

1. Open the benchmark project:

```
benchmarks/arcade-flight/
```

2. Select a model in **Continue.dev**.

3. Reset the repo before each task:

```bash
git checkout -- .
git clean -fd
```

4. Run the prompt from:

```
docs/tasks.md
```

5. Test the result manually.

6. Score the result using:

```
docs/scoring-rubric.md
```

7. Record the result in:

```
results/scorecard.csv
```

8. Optionally write a detailed report using:

```
templates/model-report.md
```

---

# Automated Model Testing

You can run the prompts automatically against a local Ollama model.

Example:

```bash
python scripts/run_ollama_eval.py qwen3.5:9b
```

Results are stored in:

```
results/raw-runs/<model>/<timestamp>/
```

These contain the raw model outputs for each task.

---

# Automated Scoring

A heuristic scoring tool evaluates the benchmark project after model edits.

Example:

```bash
python scripts/auto_score.py \
  --model qwen3.5:9b \
  --provider ollama \
  --context 48k \
  --write-json \
  --append-scorecard
```

Generated results appear in:

```
results/auto-scores/
```

Important:

Automated scoring is **heuristic** and should be combined with manual review.

---

# Leaderboard

All benchmark results are stored in:

```
results/scorecard.csv
```

The leaderboard is generated automatically from this file.

Generate locally:

```bash
python scripts/generate_leaderboard.py
```

Output:

```
docs/leaderboard.md
```

A GitHub Action automatically updates the leaderboard when the scorecard changes.

---

# Suggested Model Naming

Use consistent names when recording results:

```
qwen3.5-9b-q4
qwen2.5-coder-14b
deepseek-coder-v2-lite
llama3.1-8b-instruct
```

This keeps the leaderboard readable.

---

# How to Rank Models

Do **not** rank models based on visual output alone.

Prioritize:

1. Correctness
2. Precision of edits
3. Instruction following
4. Recovery after follow-up corrections
5. Code quality

---

# Minimal Benchmark Set

For quick testing, run only three tasks:

1. Bug fix
2. Small feature addition
3. Follow-up correction

This is usually enough to determine whether a model is usable.

---

# Full Benchmark

For complete evaluation, run all tasks described in:

```
docs/tasks.md
```

---

# Notes

This benchmark is intentionally small.

The goal is **not** to prove which model is best globally.

The goal is to determine **which model works best for your local development workflow**.
