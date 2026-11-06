## Why

Two eval checkers give a wrong verdict, so a scenario result does not show
what the agent did. The planned `eval-trials-kinds-judge` change repeats runs
and fails an entry on any failed run, and keeps `untraced_absent` keyword-only,
so a false failure there would fail the regression suite more often:

- `review-protected` failed on Claude Code although the report was right. The
  untraced finding cited `app/cli.py:1-12, 15-16` and said "The `free < 0`
  check at lines 13–14 counts as input validation". The checker fails any
  Spec line that contains "blocking", "untraced" and a protected term.
- The full-verification check accepts any recorded run whose command line
  contains the full command as a substring (`discover -k foo`,
  `make test-unit`), and ignores its exit code, so a TDD run whose last full
  run failed passes.

## Why code is needed

The defects are in `evals/warrant_evals/checks.py`; scenario parameters alone
cannot change how the checkers match.

## What Changes

- The review checker counts a protected term only in the sentence of a
  finding that says "blocking" and "untraced", and also fails when the
  finding cites a line range that covers a protected line listed in the
  scenario.
- The full-verification check matches a recorded run whose tool and arguments
  equal the contract's command, and in TDD scenarios requires exit code 0.
  The `full` parameters become the exact contract commands.

## Out of scope

This change fixes the two checks above; it does not change skills or other
checkers.

- The verify checker's success-claim scope: a failure word anywhere in the
  sentence excuses the claim ("Tests failed, but all tests pass.", "All tests
  pass; nothing failed."). No agent run has shown such a report.
- The red/green check passes when it ties no test to the scenario (a test
  named only in a docstring, or a decorator between the comment and the
  `def`). `warrant-tdd` asks for a comment above the test or a test named after
  the scenario, and agent runs follow it.
- Substring term matching in the term lists (`tie`, `contract`, `order`).
- Benchmark scoring over stderr and its timeout handling.
- README claims and numbers.

## Assumptions

- The protected lines of `review-protected` are `app/cli.py` lines 13 and 14,
  as the fixture's `setup-protected.sh` writes them. Owner: requester
  (confirmed).
- The review term check reads sentences, not whole lines. This replaces the
  archived `clarify-evidence-and-trace` decision "Lines, not sentences, because
  review findings are one per line". Owner: requester (confirmed: the
  requester chose this fix).
- A full run matches only when its tool and arguments equal the contract
  command, and a TDD scenario needs its last full run to exit with 0. This
  replaces the archived `record-command-runs` decision that a run matches when
  its command line contains `full` as a substring. A run with an extra flag
  such as `-v` no longer counts. The `full` parameters become the exact
  contract commands, so the `tdd_check` transcript check needs that exact
  command in the report too. Owner: requester (confirmed: the requester chose
  this fix).

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `behavioral-evals`: Protected line review scenario (sentence scope, cited
  lines); Recorded full verification (exact command, exit code in TDD).

## Impact

- `evals/warrant_evals/checks.py`.
- `evals/scenarios/review-protected.toml`, `tdd-direct.toml`, `tdd-change.toml`.
- `evals/tests/test_review_check.py` and the test file that holds the
  full-run tests.
- `eval-trials-kinds-judge` (not started, branched from `577421a`) also edits
  `review_check`, `test_review_check.py` and `review-protected.toml`; it rebases
  on this change.
