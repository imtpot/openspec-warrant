## Why

`record-command-runs` keeps the run log and the shims under the workspace's
`.git` directory. Codex runs with `codex exec -s workspace-write`, whose sandbox
keeps `.git` read-only, so no run is logged and the TDD and verify fact checks
fail every Codex run. A probe on Codex 0.166 confirmed it: a write to `.git`
exits 1, while writes to the workspace and to `$TMPDIR` succeed.

Separately, the scenarios of `warrant-verify`, `warrant-tdd`,
`warrant-minimal-change` and `warrant-review` have not run on Codex since
`clarify-evidence-and-trace` changed their wording, which AGENTS.md asks for.

## Why code is needed

The log location is set in `evals/warrant_evals/record.py`; nothing configures
it.

## What Changes

- The shims and the log move out of the workspace to a directory next to it,
  `<workspace>.warrant/` (`bin/` and `runs.jsonl`). The eval workspaces are
  created under the system temporary directory, which both agents may write.
- The shim learns the workspace from a new variable `WARRANT_WORKSPACE`
  instead of deriving it from the log path.
- The scenarios that load one of the four skills, and the three recording
  scenarios, run on Codex.

## Out of scope

This change moves the log and runs the Codex scenarios; it does not change any
skill or checker rule.

- Fixing Codex failures that the runs reveal; they are reported, and each
  becomes its own change.
- The benchmark and mutation checks.

## Assumptions

- Codex's `workspace-write` sandbox keeps the system temporary directory
  writable, as it did in the probe. If a Codex configuration excludes it, the
  recorder warns and the fact checks fail, as today. Owner: requester.
- A directory next to the workspace does not show when the agent lists or
  searches the workspace. The agent can still reach it with `ls ..` or an
  absolute path; the eval does not guard against that. Owner: requester.
- `--keep` keeps the `.warrant` directory next to each kept workspace.
  Owner: requester.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `behavioral-evals`: the run log lives outside the workspace.

## Impact

- `evals/warrant_evals/record.py` and its users in `checks.py`; tests in
  `evals/tests/test_record.py`, `test_runner.py`, `test_tdd_check.py`,
  `test_verify_propose_checks.py`.
- `docs/benchmark.md` (the sentence that Codex runs are not logged).
