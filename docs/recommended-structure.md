# Recommended Repo Structure

```text
local-llm-coding-evals/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── model-eval.md
│   └── workflows/
│       └── leaderboard.yml
├── benchmarks/
│   └── arcade-flight/
│       ├── README.md
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── docs/
│   ├── leaderboard.md
│   ├── models-tested.md
│   ├── recommended-structure.md
│   ├── scoring-rubric.md
│   └── tasks.md
├── prompts/
│   ├── task1_feature_addition.txt
│   ├── task2_bug_fix.txt
│   ├── task3_refactor.txt
│   ├── task4_repo_aware_change.txt
│   └── task5_follow_up_correction.txt
├── results/
│   ├── auto-scores/
│   ├── models/
│   ├── raw-runs/
│   ├── example-model-report.md
│   └── scorecard.csv
├── scripts/
│   ├── auto_score.py
│   ├── generate_leaderboard.py
│   ├── generate_model_index.py
│   ├── README.md
│   └── run_ollama_eval.py
├── templates/
│   ├── model-report.json
│   └── model-report.md
├── README.md
└── .gitignore
```
