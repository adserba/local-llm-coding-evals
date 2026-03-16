# Benchmark Tasks

Use the exact same prompts for every model.

Reset the repo before each test:

```bash
git checkout -- .
git clean -fd
```

## Task 1 — Feature addition

Prompt:

> Add a pause menu to this game. Pressing Escape should pause movement, show a centered overlay with Resume and Restart buttons, and dim the background. Keep changes minimal and preserve current structure.

What this tests:

- Multi-file editing
- Constraint following
- Whether the model preserves structure
- Whether it adds a feature without unnecessary rewrites

---

## Task 2 — Bug fix

Prompt:

> Find and fix the issues causing the camera follow jitter, stale speed display, and stuck controls after tab switching. Explain briefly what was wrong.

What this tests:

- Debugging
- Root-cause analysis
- Whether fixes are real or just cosmetic

Expected underlying issues in this benchmark app:

- Camera follow is too abrupt
- Speed label is not refreshed after throttle changes
- Held keys can remain active after focus loss

---

## Task 3 — Refactor without changing behaviour

Prompt:

> Refactor the movement logic into smaller functions, reduce duplication, and improve naming, but do not change gameplay behaviour.

What this tests:

- Discipline
- Refactoring ability
- Ability to avoid accidental feature creep

---

## Task 4 — Repo-aware change

Prompt:

> Add a settings section to the README documenting controls, and make sure the in-game overlay matches that documentation.

What this tests:

- Cross-file consistency
- README awareness
- Whether the model keeps docs and code aligned

---

## Task 5 — Follow-up correction

After the model answers Task 1, apply this follow-up prompt:

> Good start, but keep the existing layout and only patch the current implementation. Do not rewrite the UI. Also make restart preserve the initial camera position.

What this tests:

- Whether the model accepts correction cleanly
- Iteration quality
- Real-world usability in Continue chat/edit

---

## Optional stretch task

Prompt:

> Add a very simple checkpoint system: three rings ahead of the plane, a counter for passed rings, and reset the counter when Restart is pressed. Keep the implementation lightweight.

Use this only if you want to separate strong models from decent ones.
