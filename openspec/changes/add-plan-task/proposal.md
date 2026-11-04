# Proposal

## Why

warrant's main claim is about planning: EARS requirements and an Assumptions
section make an agent surface what a request leaves open instead of deciding
it silently. No benchmark task tests that; every task so far hands the agent a
finished change. The requester also wants planning and implementation measured
together, as a real change runs.

## What Changes

- A `plan-implement` task kind: the agent gets a short request with three
  hidden ambiguities, plans it as an OpenSpec change and implements it in the
  same run.
- Scores: the share of ambiguities the agent marks as open or assumed, hidden
  acceptance tests on the unambiguous behavior, fault detection and added
  lines.
- Fault detection counts a fault as caught when a test that passes on the
  reference implementation fails on it, so tests that settle an ambiguity
  differently from the reference no longer void the score.
- A task `plan-implement-allocation` for `allocate(total_cents, percents)`.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `benchmark`: plan-implement tasks; fault detection per test.

## Impact

`evals/warrant_evals/benchmark.py`, its tests, a new task under
`evals/benchmark/`, `README.md`.

## Why code is needed

The benchmark scores runs in code.

## Out of scope

The task measures whether ambiguities are surfaced, not which decision the
agent takes for them.

Features and options deliberately left out:

- Acceptance tests for ambiguous behavior; the agent cannot know the
  requester's choice.
- Asking the agent questions interactively.

## Assumptions

Confirmed by the requester: one task that measures planning and
implementation together; ambiguous cases count only for being surfaced.

- An ambiguity counts as marked when one of its terms appears in the
  proposal's Assumptions section, or in a sentence of the report or artifacts
  that also says assume, question, confirm, unclear, ambiguous, decided or
  chose. Owner: requester (decided while the requester was away).
- The three ambiguities are percentages that do not add up to 100, where the
  leftover cents go, and an empty list or a zero percentage. Owner: requester
  (decided while the requester was away).
