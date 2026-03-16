# Scoring Rubric

Score each task out of 10.

## Correctness — 4 points

- 4 = works correctly
- 3 = mostly works, minor issues
- 2 = partially works
- 1 = barely works
- 0 = broken or fake

## Precision — 2 points

- 2 = targeted edits only
- 1 = some unnecessary churn
- 0 = rewrote too much or touched unrelated files

## Code quality — 2 points

- 2 = clean and maintainable
- 1 = acceptable but messy
- 0 = confusing, brittle, or sloppy

## Instruction following — 2 points

- 2 = followed prompt closely
- 1 = partial drift
- 0 = ignored key constraints

## Penalties

Subtract after scoring:

- -2 invented functionality not requested
- -2 unnecessary rewrite of unrelated code
- -2 dead code left behind
- -3 confidently wrong explanation
- -3 looks good but does not really work

## Interpretation

- 45–50: excellent local daily-driver
- 38–44: strong, likely worth keeping
- 30–37: usable with caution
- 20–29: weak or inconsistent
- below 20: not worth defaulting to

## Recommendation rule

If two models are close, prefer the one with:

- better bug-fixing
- fewer rewrites
- better follow-up correction handling

That usually matters more than first-pass visual polish.
