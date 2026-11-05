# Tasks

## 1. Accepted term

- [x] 1.1 Add a test to `evals/tests/test_cli.py` (next to the `review-protected` load test) that runs the loaded `review-protected` check on a report whose Spec section names the option only as "JSON output" and expects no "Spec section lacks" finding
- [x] 1.2 Add "JSON output" to the `spec` param of `evals/scenarios/review-protected.toml`; verify the test from 1.1 passes

## 2. Eval scenario

- [x] 2.1 Run `uv run python -m warrant_evals --agent codex --agent claude --scenario review-protected`; verify both entries pass

## 3. Review

- [x] 3.1 Check the diff; remove speculative generality, unused options, unrequested features and dependencies

## 4. Verification

- [x] 4.1 Run `uv run pytest`
  Result: exit 0, 309 passed in 110.44s (0:01:50)
- [x] 4.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
