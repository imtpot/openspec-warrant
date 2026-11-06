## Context

See proposal.md - Why. `behavior.py` splits a report into sentences
(`SENTENCE`). `checks.py` has `review_check` (`untraced_absent`) and
`_full_findings`; the run log
records `tool`, `args`, `exit` and `state` per run. The checkers have unit
tests in `evals/tests/`.

## Goals / Non-Goals

**Goals:** each checker gives the verdict its requirement states on the cases
in the delta spec; `review-protected` passes on Claude Code on a report like
the one in Why.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

Option ladder for every part: (1) no change keeps the wrong verdicts. (2)
Existing code: each part changes the function that carries the defect and
reuses the helpers next to it. The rungs after (2) are not needed: the
standard library (`re`, `shlex`) already in use covers the parsing.

### Protected line review (`checks.py`)

This replaces the archived `clarify-evidence-and-trace` decision "Lines, not
sentences, because review findings are one per line" for the term check.

- A Spec line with "blocking" and "untraced" still counts as a finding. A term
  counts only in a sentence of that line (split as `behavior.SENTENCE` does)
  that also contains "blocking" and "untraced", which is the finding's own
  sentence. A first version took any sentence with "untraced"; the Claude
  report in Why ends with "...only exists to serve this untraced CLI.", so it
  still failed.
- New optional param `untraced_lines`, a table `{path = [line, ...]}`. For
  each `path:` occurrence in a finding line, parse the following ranges
  (`\d+` with `-` or `–` for ranges, separated by commas and spaces) and fail
  when they cover a listed line. `review-protected.toml` gets
  `untraced_lines = {"app/cli.py" = [13, 14]}`; the finding message names the
  line.

### Full verification (`checks.py`)

This replaces the archived `record-command-runs` decision "the last run whose
`tool + " " + " ".join(args)` contains `full` as a substring".

- `_full_findings(workspace, full, exit_zero)`: a run matches when
  `[tool, *args] == shlex.split(full)`. With `exit_zero`, a matching last run
  on the final files that exited non-zero gives "full verification exited
  <code>".
- `tdd_check` passes `exit_zero=True`, `verify_check` passes `False` (its
  fixture test fails by design).
- `full` in `tdd-direct.toml` and `tdd-change.toml` becomes
  `python3 -m unittest discover -s tests -t .`; in `verify.toml` it stays
  `make test`. These are the commands in the fixtures' contracts. The
  transcript check of `tdd_check` uses the same string.

### Tests

Each scenario of the delta spec becomes a unit test in the test file of its
checker, red on the current code and green after the fix.
`review-protected`, `tdd-direct`, `tdd-change` and `verify` then run on both
agents (`verify` because `verify_check` now passes `exit_zero=False`).

## Risks / Trade-offs

- [A blocking untraced line names the check only in a later sentence and cites
  no line, such as "Blocking untraced finding. The `free < 0` check at lines
  13-14 serves no requirement."] → The old line check failed it, the new check
  passes it. Accepted: `warrant-review` asks for an untraced finding "with file
  and line", which the range check reads, and a miss shows in the transcript.

- [`eval-trials-kinds-judge` conflicts on `review_check`] → Its judge leaves
  `untraced_absent` alone; the conflict is textual and resolved when it
  rebases.

- [An agent cites the protected lines in a way the range parser misses, such
  as "lines 13 to 14"] → The sentence-scoped term check still catches a
  finding that names the check; a miss shows in the transcript.
- [The exact command check fails a run with an extra harmless flag such as
  `-v`] → Accepted: the contract asks for the command exactly as written.
