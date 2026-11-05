## Context

See proposal.md - Why. `Scenario.path` already puts workspace directories first
on PATH (`setup-wrong-version` uses it for a fake CLI). The runner passes the
final report, not the raw transcript, to the checkers.

## Goals / Non-Goals

**Goals:** the TDD and verify evals check what ran, in which order, with which
exit code and on which files, for any language, on agents that let the run
write under `.git` (Claude Code; not Codex's sandbox, see proposal.md -
Assumptions).

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

### Recording shim

This replaces the archived `add-warrant-tdd` Decision 1 ("Evidence in the
report, not in the harness ... Rejected: wrapping test runners in the fixture to
log every run; it needs a fake tool per language"). The shim below is one
pass-through recorder for any tool name, so no fake tool per language is
needed.

Option ladder: (1) no change keeps trusting the report. (2) Existing code:
Claude's stream has commands and output but not exit codes behind pipes, and
Codex's stderr has neither in a fixed form. (3) Standard library: one Python
module, `warrant_evals/record.py`, run as the shim:

- For each tool in `record`, the runner writes `<workspace>/.git/warrant/bin/<tool>`,
  an executable whose shebang is the harness's own interpreter
  (`sys.executable`, so a `python3` shim does not call itself) and which runs
  `record.py`. It prepends that directory to PATH and sets `WARRANT_RUN_LOG`
  (`<workspace>/.git/warrant/runs.jsonl`) and `WARRANT_REAL_PATH` (PATH without
  the shim directory).
- `record.py` finds the real tool on `WARRANT_REAL_PATH`, takes the workspace
  hash, runs the tool with the same argv, stdin, stdout, stderr and
  environment (PATH unchanged, so nested runs are recorded), and appends one
  JSON line: `{"seq", "tool", "args", "cwd", "exit", "state"}`, where `args` is
  argv without the shim path. `seq` is the start time in nanoseconds. It exits
  with the tool's exit code. If the real tool is not on `WARRANT_REAL_PATH`, it
  prints the shell's message and exits 127. If the log cannot be written, it
  prints one warning line to stderr and still passes the run through.
- `install_shims` creates the log empty, so "no run" and "no recording" differ.
  The checkers run the fact checks when the log file exists.
- `state` is a SHA-256 over the path and content of every tracked and untracked,
  not ignored, file of the workspace, read with `git ls-files -c -o
  --exclude-standard -z`, skipping listed files that no longer exist, so the
  hash is the same before and after the checker's `git add -A`. It does not
  touch the index.
- The log lives under `.git` so that it never shows in `git status`, diffs or
  the agent's file listing.

### Fact checks

A helper `recorded_runs(workspace)` reads the log sorted by `seq`, and
`workspace_state(workspace)` computes the same hash after the run.

- TDD, per `red_green` scenario: find the scenario's test in the added lines
  of `tests/` (the checker already reads them): a `def test_...` whose name, or
  the comment line right above it, contains the normalized scenario name
  (lowercase, every non-alphanumeric run → `_`; the comment line is normalized
  the same way). The class is the nearest `class` line above the function in
  the test file, read from disk. A run covers the test when `" ".join(args)`
  contains, as a substring, the function name, the class name, the module as
  `tests.test_x` or `tests/test_x.py`, or follows a `-k` with a value that is a
  substring of the function name; and does not contain `discover`. Fail unless a covering run exits
  non-zero and a later covering run exits 0 with a different `state`. If no
  test is found, the existing "no added test names scenario" finding already
  reports it.

  This keeps the archived `add-warrant-tdd` Decision 3 ("`test_<scenario>` or
  a comment `# <Requirement>: <Scenario>` above the test"): both forms work,
  and so does a run by module.
- TDD and verify, with param `full` (the contract command as text): fail
  unless the last run whose `tool + " " + " ".join(args)` contains `full` as a
  substring started on a `state` equal to the final `workspace_state`. For
  `make test`, the `make` run counts; the nested `python3` run does not match.
- The checks run only when the scenario records tools; scenarios without
  `record` keep their current behavior.

### Scenario files

- `tdd-change.toml`, `tdd-direct.toml`: `record = ["python3"]`.
- `verify.toml`: `record = ["make", "python3"]`, `full = "make test"`.

## Risks / Trade-offs

- [The agent calls a tool by absolute path] → Not recorded; the fact checks
  fail, and the transcript shows why. Listed under Assumptions.
- [The harness interpreter differs from the agent's `python3`] → The shim only
  hosts `record.py`; the recorded tool is the real `python3` found on
  `WARRANT_REAL_PATH`.
- [Hashing a large workspace at every run is slow] → The fixtures have a few
  files; the benchmark does not record.
- [`tdd-direct` has no `red_green` param] → Only the full-verification check
  applies there; no new param is invented for it.
