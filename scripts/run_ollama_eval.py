#!/usr/bin/env python3
"""
Run one-shot benchmark prompts against a local Ollama model and save raw outputs.

This does NOT replace Continue for interactive editing.
It is useful for:
- quick baseline comparisons
- repeatable one-shot prompt tests
- saving raw outputs in a consistent structure
"""

from __future__ import annotations
import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCH_ROOT = REPO_ROOT / "benchmarks" / "arcade-flight"
PROMPT_ROOT = REPO_ROOT / "prompts"
OUTPUT_ROOT = REPO_ROOT / "results" / "raw-runs"

TASKS = [
    "task1_feature_addition",
    "task2_bug_fix",
    "task3_refactor",
    "task4_repo_aware_change",
    "task5_follow_up_correction",
]

def read_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def build_context() -> str:
    parts = []
    for name in ["README.md", "index.html", "styles.css", "app.js"]:
        path = BENCH_ROOT / name
        parts.append(f"\n===== FILE: {name} =====\n{read_file(path)}\n")
    return "\n".join(parts)

def load_prompt(task_name: str) -> str:
    return read_file(PROMPT_ROOT / f"{task_name}.txt")

def run_ollama(model: str, prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ollama run failed with code {result.returncode}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result.stdout.strip()

def sanitize(name: str) -> str:
    return name.replace(":", "-").replace("/", "-").replace(" ", "_")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="Ollama model name, e.g. qwen3.5:9b")
    parser.add_argument(
        "--tasks",
        nargs="*",
        default=TASKS,
        help="Subset of tasks to run",
    )
    args = parser.parse_args()

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    model_slug = sanitize(args.model)
    out_dir = OUTPUT_ROOT / model_slug / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    context = build_context()
    manifest = {
        "model": args.model,
        "timestamp": timestamp,
        "tasks": [],
    }

    for task_name in args.tasks:
        instruction = load_prompt(task_name)
        full_prompt = f"""
You are evaluating a coding model on a small benchmark repo.

Return:
1. a brief plan
2. the exact file changes as complete replacement file contents
3. a short self-check section

Rules:
- preserve the current project structure
- keep edits minimal unless the task explicitly requires more
- do not omit unchanged files if you changed them
- when changing a file, output it in this format:

===== BEGIN FILE: relative/path =====
<full file contents>
===== END FILE =====

Current repo context:
{context}

Task:
{instruction}
""".strip()

        raw_output = run_ollama(args.model, full_prompt)
        output_file = out_dir / f"{task_name}.md"
        output_file.write_text(raw_output, encoding="utf-8")

        manifest["tasks"].append({
            "task": task_name,
            "output_file": str(output_file.relative_to(REPO_ROOT)),
        })

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Saved run to: {out_dir}")

if __name__ == "__main__":
    main()
