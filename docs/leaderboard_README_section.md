
## Leaderboard

The leaderboard is automatically generated from `results/scorecard.csv`.

Generate it locally:

```bash
python scripts/generate_leaderboard.py
```

This produces:

```
docs/leaderboard.md
```

You can commit this file so visitors can immediately see model rankings.

### Example

| Model | Provider | Context | Total Score |
|------|----------|--------|-------------|
| qwen3.5:9b | ollama | 48k | 38 |
| qwen2.5:14b | ollama | 32k | 31 |
