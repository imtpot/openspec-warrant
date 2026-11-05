# Tasks

## 1. Log next to the workspace

- [x] 1.1 In `evals/tests/test_record.py`, change the log test to expect the log at `<workspace>.warrant/runs.jsonl` next to the workspace, nothing new inside the workspace (`git status` clean and no `.warrant` entry in a listing), and a run logged with a read-only `.git` directory (Run log outside the workspace: Codex sandbox, Agent's view)
- [x] 1.2 Replace the literal `.git/warrant` paths in `evals/tests/test_tdd_check.py`, `test_verify_propose_checks.py` and `test_runner.py` with `run_log(...)` and its parent
- [x] 1.3 Change `run_log`, `install_shims` (`WARRANT_WORKSPACE`) and `main()` in `evals/warrant_evals/record.py` as in design.md; verify every test in the four files passes
- [x] 1.4 Replace the sentence about Codex in `docs/benchmark.md` with where the log lives

## 2. Codex runs

- [x] 2.1 Run on Codex with `--keep`: `tdd-change`, `tdd-direct`, `verify`, `verify-no-contract`, `tdd-no-tests`, `discovery`, `minimal-change`, `minimal-change-implicit`, `shortcut-ledger`, `artifact-review-flawed`, `artifact-review-sound`, `receive-comments`, `review-no-change`, `review-branch`, `review-empty`, `review-two-changes`, `review-named-base`, `review-protected`; record per scenario pass, fail or not run, and for each failure whether the checker, the harness or the agent is wrong, judged from the transcript and the run log
  Outcome: 17 of 18 pass on Codex 0.166, including `tdd-change`, `tdd-direct` and `verify`, whose run logs next to the workspace show red then green runs and the full run (the shims work under Codex's sandbox). `review-protected` fails with "Spec section lacks: --json": Codex reported the option as "JSON output" (untraced, `app/cli.py:2–7,11,15–16`) and correctly left the protected check on lines 13–14 out. The checker's accepted terms are too narrow; the agent is right. Not fixed here.

## 3. Review

- [x] 3.1 Check the diff against the delta spec; remove speculative generality, unused options, unrequested features and dependencies

## 4. Verification

- [x] 4.1 Run `uv run pytest`
  Result: exit 0, 308 passed in 111.03s (0:01:51)
- [x] 4.2 Run `openspec validate --all --strict`
  Result: exit 0, Totals: 11 passed, 0 failed (11 items)
