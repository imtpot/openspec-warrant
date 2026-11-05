## Why

The TDD and verify evals take the agent's word for what it ran. The TDD checker
looks for a failing line before a passing line in the final report, and for the
narrowed and full commands as text; the verify checker looks for "make test" in
the report. An agent can write a correct-looking red/green report without the
runs behind it, and the eval passes.

The transcript cannot close the gap. Claude's stream shows each command and its
output, but agents pipe test runs (`python3 -m unittest ... 2>&1 | tail -1`), so
the recorded exit status is that of `tail`: a failing red run shows as
`is_error: false`. Codex prints its commands in its own format on stderr.

## Why code is needed

The eval harness is Python code; it has no way today to observe a command's
real exit code or the files it ran on. The `.tests-ran` marker in the
`no-contract` fixture's Makefile is a one-off form of the same idea and cannot
tell order, exit code or file state.

## What Changes

- A scenario can list tools to record (`record = ["python3", "make"]`). The
  runner puts a recording shim for each on PATH. The shim runs the real tool
  unchanged and appends one line per run to a log under the workspace's `.git`
  directory: order, argv, working directory, exit code, and a hash of the
  workspace files at the start of the run.
- The TDD checker checks, from the log, that each `red_green` scenario has a
  recorded failing run followed by a passing run that both cover the scenario's
  test (by function, class or module), with a file change between them, and that the full tests command ran
  on the final files.
- The verify checker checks, from the log, that the contract command ran after
  the agent's last change.
- `tdd-change`, `tdd-direct` and `verify` record their test tools. The existing
  report-based checks stay: the skill still has to report its evidence.

## Out of scope

This change records runs of named tools in eval scenarios; it does not change
any skill or the benchmark.

- Verified mutation coverage (applying a mutation and seeing a test fail).
- Comparing the exit codes in the agent's report with the log.
- Recording in the benchmark harness.
- Replacing the `.tests-ran` marker of `verify-no-contract`.
- Running the scenarios on Codex.

## Assumptions

- This replaces the archived `add-warrant-tdd` decision "Evidence in the
  report, not in the harness": the shim is one pass-through recorder for any
  tool, not a fake tool per language, which was the reason for the rejection.
  Owner: requester.
- The scenario's test is the added test function whose name, or the comment
  line right above it, contains the scenario name, as the archived
  `add-warrant-tdd` Decision 3 already matches tests. A run covers that test
  when its joined arguments contain the function name, its class name, its
  module (dotted or as a path), or a `-k` value that is part of the function
  name, and do not contain `discover`. A module run can fail for another
  test's reason; that is accepted. Owner: requester.
- The log starts empty when the shims are installed, so an agent that runs no
  recorded tool fails the fact checks. Owner: requester.
- An edit of any tracked file, or a new untracked and not ignored file, after
  the full run fails the full-verification check, including notes, scratch
  files or `tasks.md`. Owner: requester.
- If the real tool is not on PATH, the shim prints the shell's "not found"
  message and exits 127, as the shell would. Owner: requester.
- Runs started by a recorded tool are recorded too (`make test` records `make`
  and the `python3` it starts). Owner: requester.
- A tool called by absolute path (`/usr/bin/python3`) bypasses the shim and is
  not recorded; the fact checks then fail the scenario. Owner: requester.
- The scenarios run on Claude only. Codex's `workspace-write` sandbox keeps
  `.git` read-only, so the log cannot be written there; the recorder then
  passes the tool through and warns, and the fact checks fail. Owner:
  requester.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `behavioral-evals`: recorded command runs; TDD and verify checks on them.

## Impact

- `evals/warrant_evals/runner.py` (Scenario field, shims, PATH),
  `evals/warrant_evals/scenarios.py`, a new recorder module,
  `evals/warrant_evals/checks.py` (TDD and verify checkers).
- `evals/scenarios/tdd-change.toml`, `tdd-direct.toml`, `verify.toml`.
- Tests in `evals/tests/`.
- `docs/benchmark.md`, which says TDD evals "cannot prove that each run
  happened".
