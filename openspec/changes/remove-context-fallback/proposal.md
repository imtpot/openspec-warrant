# Proposal

## Why

Every agent warrant supports starts sub-agents with a fresh context, and every
skill that asks for one adds a sentence on what to do without it. The
sentences cost tokens on every load, describe a case that does not occur, and
let an agent take the weaker path when it could start a sub-agent.

## What Changes

- `warrant-review` runs the Spec and Standards axes and the artifact review in
  separate, fresh contexts, without a fallback sentence.
- The kit no longer requires a fallback sentence where a skill asks for a
  fresh context.
- `docs/design.md` principle 6 states that skills may require a sub-agent.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `code-review`: fresh contexts without a fallback.
- `warrant-kit`: no fallback rule.

## Impact

`skills/warrant-review/SKILL.md`, `evals/tests/test_kit.py`, `docs/design.md`.

## Why code is needed

The skill text and a kit test change; no code beyond the test.

## Out of scope

This change removes the fallback; it does not move more work into sub-agents.

Features and options deliberately left out:

- A check that an agent actually started a sub-agent; evals see only the final
  report.

## Assumptions

Confirmed by the requester: remove the fallback sentence everywhere, because
all supported agents have sub-agents. No other decision is open.
