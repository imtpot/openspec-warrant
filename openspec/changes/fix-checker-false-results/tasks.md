# Tasks

## 1. Protected line review

- [x] 1.1 Protected line review scenario: add tests to `evals/tests/test_review_check.py` for "Check excluded in a later sentence" and "Check covered by a cited range"; see them fail, then change `review_check` in `evals/warrant_evals/checks.py`, add `untraced_lines` to `evals/scenarios/review-protected.toml`, and see all of `test_review_check.py` and `test_cli.py` pass

## 2. Full verification

- [x] 2.1 Recorded full verification: add tests for "Narrowed run with the full command as a prefix" to `evals/tests/test_verify_propose_checks.py` (next to the existing full-run tests) and for "Failing full run in a TDD scenario" to `evals/tests/test_tdd_check.py`; see them fail, then change `_full_findings`, `tdd_check`, `verify_check` the `full` params of `tdd-direct.toml` and `tdd-change.toml`, and `PARAMS['full']` in `evals/tests/test_tdd_check.py` (to the exact contract command), and see `test_verify_propose_checks.py`, `test_tdd_check.py` and `test_cli.py` pass

## 3. Evals

- [x] 3.1 Run `uv run python -m warrant_evals --agent claude --agent codex --scenario review-protected --scenario tdd-direct --scenario tdd-change --scenario verify`; report each failing entry with the cause from its transcript
  Claude: 4 of 4 pass. Codex: 4 of 4 pass.

## 4. Review

- [x] 4.1 Check the diff against the specs; remove speculative generality, unused options, unrequested features and dependencies

## 5. Verification

- [x] 5.1 Run `uv run pytest`
  Result: exit 0, 327 passed in 105.91s (0:01:45)
- [x] 5.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
