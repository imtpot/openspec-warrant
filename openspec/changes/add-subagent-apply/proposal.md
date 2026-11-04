# Proposal

## Why

The agent that runs the OpenSpec apply workflow implements every task in its
own context. Code, test output and read files pile up, and every later step
sends them again: in a Claude benchmark run, the warrant arm took 57 turns and
1.2 million tokens, 95% of them re-read context, against 27 turns for plain
OpenSpec. A long context also drifts from the requirements. Implementing each
task group in a fresh sub-agent keeps the orchestrating context small and
gives each group a clean start, as the requester and Matt Pocock recommend.

## What Changes

- Apply guidance: implement each task group in a separate, fresh context (a
  sub-agent) that gets the group's tasks, their requirement names and the
  paths of the change's artifacts, follows `warrant-tdd` and
  `warrant-minimal-change`, and reports scenarios, red and green results and
  changed files.
- Apply guidance: after each sub-agent's report, the orchestrating agent runs
  `warrant-verify` and then checks off the group's tasks.
- Tasks rule: each implementation group can be implemented from the
  artifacts and the code alone, without another group's unfinished work.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `warrant-rules`: sub-agent per task group; independent task groups.

## Impact

`skills/warrant-setup/rules.yaml` and its copies, kit tests, `README.md`,
`docs/design.md`.

## Why code is needed

Only rules change; a kit test keeps them in the shipped rules.

## Out of scope

This change moves implementation into sub-agents; it does not change how
`warrant-tdd` chooses its tests.

Features and options deliberately left out:

- A sub-agent per task instead of per group; a group shares setup and files.
- Parallel sub-agents; groups run one after another.

## Assumptions

Confirmed by the requester: implement in sub-agents with a fresh context; no
fallback for agents without sub-agents.

- One sub-agent per task group, not per task. Owner: requester (decided while
  the requester was away).
- Groups run one after another. Owner: requester (decided while the requester
  was away).
