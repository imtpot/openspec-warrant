# Proposal

## Why

On Claude Opus, plain OpenSpec nearly matches warrant: every arm writes
correct code, and fault detection differs by one fault per run. Weaker models
may need the kit's discipline more. The benchmark cannot test that, because it
runs each agent's default model only.

## What Changes

- The benchmark takes `--model <agent>=<model>` and passes the model to that
  agent's command (`--model` for Claude, `-m` for Codex).
- Tables name such runs `<agent>:<model>`.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `benchmark`: model selection.

## Impact

`evals/warrant_evals/benchmark.py`, its tests, `README.md`.

## Why code is needed

The benchmark builds the agent commands in code.

## Out of scope

This change selects one model per agent and run; it does not run a model
matrix in one call.

Features and options deliberately left out:

- Reasoning effort options.

## Assumptions

Confirmed by the requester: run the implement task on weaker Claude models
first.

- One model per agent per call; several models need several calls. Owner:
  requester (decided while the requester was away).
