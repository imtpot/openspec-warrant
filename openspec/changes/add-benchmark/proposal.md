# Proposal

## Why

The evals show that agents follow warrant's skills; they do not show that
warrant helps. Principle 7 asks for evidence, and Ponytail shows the form: the
same tasks with and without the skill, several runs each, and measured
results. Without such a comparison, nobody knows whether warrant catches more
bugs or only spends more tokens than plain OpenSpec.

## What Changes

- A benchmark command runs each benchmark task on each agent in two arms:
  `openspec` (OpenSpec skills, verification commands as plain `AGENTS.md`
  text) and `warrant` (the same plus warrant's skills, rules and contract).
- An implement task measures hidden acceptance tests passed, the share of
  prepared faulty implementations that the agent's own tests reject, and the
  non-test lines added.
- A review task measures the share of planted problems the review names.
- Every run records the tokens the agent reports.
- The benchmark writes a table with the mean per task, agent and arm.

## Capabilities

### New Capabilities
- `benchmark`: compare plain OpenSpec with OpenSpec plus warrant.

### Modified Capabilities
None.

## Impact

New `evals/warrant_evals/benchmark.py`, `evals/benchmark/` (tasks, fixture,
hidden tests and faulty implementations), tests, `README.md`,
`docs/design.md`. The review task reuses the `review-branch` fixture.

## Why code is needed

No existing tool runs agent CLIs in two configurations and scores the results
against hidden tests.

## Out of scope

The benchmark measures two tasks; it is not a general agent leaderboard and
does not run in CI.

Features and options deliberately left out:

- Cost in money: agents report tokens in different units and only Claude
  reports cost.
- Statistical tests; the table shows means and the number of runs.
- A third arm with another kit.

## Assumptions

Confirmed by the requester: build the comparison with a baseline (item 1) and
the detection rate of planted review problems (item 2).

- The baseline is OpenSpec with its skills, not an agent without any kit.
  Owner: requester (decided while the requester was away).
- Faulty implementations replace the agent's module, so the task fixes the
  module path and function signature in its design. Owner: requester (decided
  while the requester was away).
- Three runs per task, agent and arm by default. Owner: requester (decided
  while the requester was away).
- Token counts compare arms within one agent, never across agents. Owner:
  requester (decided while the requester was away).
