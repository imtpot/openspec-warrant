# Design

## Context

See proposal.md - Why. Requirements are in `specs/`.

- Headless runs return the agent's final message (Claude Code) or its final
  message plus a log (Codex); intermediate test runs are not reliably visible.
- `warrant-minimal-change` defines "least code", `warrant-verify` the final
  verification; `warrant-tdd` refers to both instead of repeating them.

## Goals / Non-Goals

**Goals:**
- A reviewer can find the test for every scenario by name, and can see from
  the report that each test failed before it passed.

**Non-Goals:**
- No observation of the agent's intermediate commands by the eval harness.

## Decisions

### 1. Evidence in the report, not in the harness

The order red → green cannot be observed from the final message alone, so the
skill must report, per scenario, the failing result line and the passing result
line (requirement "Red and green evidence"). The checker verifies that report.
Rejected: wrapping test runners in the fixture to log every run; it needs a
fake tool per language and would test the harness more than the skill.

### 2. Narrowing by the tool's own selection

The skill derives the single-test command from the contract's tests command by
adding the tool's selection syntax (a file path, a test id, `-k`, `--grep`,
`-run`). It names this as narrowing in the report. Option ladder: the contract
already holds the command; a new contract entry was rejected by the requester.

### 3. Traceability by name or comment

`test_<scenario_in_snake_case>` or a comment `# <Requirement>: <Scenario>`
above the test. The checker accepts either and matches names case-insensitively
with spaces, hyphens and underscores treated alike.

### 4. Eval fixtures

- `tdd-project`: an OpenSpec change with "Shortfall verdict" (scenario "Not
  enough free"; missing in code) and "Negative input" (scenario "Negative
  request"; the check already exists); contract tests command
  `python3 -m unittest discover -s tests -t .`.
- `tdd-no-tests`: the same code with an empty Verification list.
- `tdd-direct`: no OpenSpec change; the prompt asks for a small function.

## Risks / Trade-offs

- [An agent writes "failed" and "passed" in the report without running tests]
  → The checker also requires the narrowed command and the full command with
  an exit code; the eval cannot prove the runs happened, and the README says so.
- [Name matching misses a test named differently] → The comment form gives the
  agent an unambiguous option; the skill text prefers it.
