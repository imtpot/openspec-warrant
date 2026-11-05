## Context

See proposal.md - Why. `record.py` has `run_log(workspace)` returning
`<workspace>/.git/warrant/runs.jsonl`; `install_shims` writes `bin/` next to it;
`main()` takes the workspace as `log.parents[2]`. The checkers call
`run_log(workspace).is_file()`.

## Goals / Non-Goals

**Goals:** recorded runs are logged on Codex as on Claude; the scenarios of the
four skills have run on Codex.

**Non-Goals:** see proposal.md - Out of scope.

## Decisions

### Log next to the workspace

This replaces the `record-command-runs` decision "The log lives under `.git` so
that it never shows in `git status`, diffs or the agent's file listing", because
Codex's sandbox cannot write there.

Option ladder: (1) no change: Codex runs are never logged. (2) Existing code:
`run_log` is the one place that names the location. Change it to
`workspace.parent / f'{workspace.name}.warrant' / 'runs.jsonl'`; `bin/` stays
next to the log. A directory inside the workspace, hidden through
`.git/info/exclude`, was rejected: the agent would still see it in a listing.

`install_shims` adds `WARRANT_WORKSPACE` to the returned environment, and
`main()` reads it instead of `log.parents[2]`.

The tests that write a log by hand use `run_log(...)` instead of the literal
`.git/warrant` path, so the location is named once.

### Codex runs

Run on Codex, with `--keep`, the scenarios listed in tasks.md. A failure is
judged from the transcript and, for recording scenarios, the run log, and is
reported, not fixed here.

## Risks / Trade-offs

- [A user runs evals with workspaces in a directory Codex may not write] → The
  runner always creates them with `tempfile.mkdtemp`, under the system
  temporary directory.
- [Codex's shell resets PATH so the shims are not first] → The fact checks then
  fail; the Codex run of `tdd-change` shows it, and the transcript shows why.
