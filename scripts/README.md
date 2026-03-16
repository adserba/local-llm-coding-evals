# Scripts

## `run_ollama_eval.py`

Runs one-shot benchmark prompts against a local Ollama model and saves raw outputs.

Example:

```bash
python scripts/run_ollama_eval.py qwen3.5:9b
```

Outputs are stored under:

```text
results/raw-runs/<model>/<timestamp>/
```

## `auto_score.py`

Heuristic scorer for the benchmark app after a model edits the files.

Example:

```bash
python scripts/auto_score.py --model qwen3.5:9b --provider ollama --context 48k --write-json --append-scorecard
```

This is strongest for:

- Task 1
- Task 2
- Task 4

It is still useful for Task 3 and Task 5, but you should manually verify those.

## `generate_model_index.py`

Builds `docs/models-tested.md` from `results/scorecard.csv`.
