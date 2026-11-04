# Proposal

## Why

The evals show that agents follow warrant's skills; they do not show that
warrant helps. Principle 7 asks for evidence, and Ponytail shows the form: the
same tasks with and without the skill, several runs each, and measured
results. Without such a comparison, nobody knows whether warrant catches more
bugs or only spends more tokens than plain OpenSpec.

## What Changes

- A benchmark command runs each benchmark task on each agent in three arms:
  `bare` (no skills; the project files and the same prompt), `openspec`
  (OpenSpec skills) and `warrant` (OpenSpec skills plus warrant's skills,
  rules and contract). In `bare` and `openspec`, `AGENTS.md` names the
  verification commands as plain text.
- Claude runs without user settings, so user-level plugins stay out of every
  arm.
- An implement task measures hidden acceptance tests passed, the share of
  prepared faulty implementations that the agent's own tests reject, and the
  non-test lines added. Some faults break only a requirement's text, not one
  of its example scenarios.
- A review task measures the share of planted problems the review names; the
  problems need reading the spec, the standards or code outside the diff.
- Every run records the tokens the agent reports.
- The benchmark writes a table with the mean per task, agent and arm.

## Capabilities

### New Capabilities
- `benchmark`: compare no kit, plain OpenSpec, and OpenSpec plus warrant.

### Modified Capabilities
None.

## Impact

New `evals/warrant_evals/benchmark.py`, `evals/benchmark/` (tasks, fixture,
hidden tests and faulty implementations), tests, `README.md`,
`docs/design.md`.

## Why code is needed

No existing tool runs agent CLIs in two configurations and scores the results
against hidden tests.

## Out of scope

The benchmark measures two tasks; it is not a general agent leaderboard and
does not run in CI.

Features and options deliberately left out:

- Cost in money: the agents report tokens differently and only Claude reports
  cost.
- Statistical tests; the table shows means and the number of runs.
- Arms with other kits (Ponytail, superpowers).

## Assumptions

Confirmed by the requester: build the comparison with a baseline (item 1), the
detection rate of planted review problems (item 2), and an arm without any
kit.

- The `bare` arm keeps the `openspec/` files, which carry the task's
  requirements, but installs no skill. Owner: requester (decided while the
  requester was away).
- User-level configuration of Codex loads in every arm; the requester removed
  Codex's user skills, so only built-in skills remain. Owner: requester.
- Faulty implementations replace the agent's module, so the task fixes the
  module path and function signature in its design. Owner: requester (decided
  while the requester was away).
- Three runs per task, agent and arm by default. Owner: requester (decided
  while the requester was away).
- Token counts compare arms within one agent, never across agents. Owner:
  requester (decided while the requester was away).
