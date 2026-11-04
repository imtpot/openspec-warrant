# Proposal

## Why

warrant's principles (see `docs/design.md`) live in conversation and in one
design document. A comparison with the inspiration sources showed drift that
nothing caught: skill descriptions that summarize workflows, rules repeated in
several places, and skills that duplicate OpenSpec. Principles that a test can
check should be requirements with tests, so drift fails `uv run pytest`.

## What Changes

- Add the `warrant-kit` capability: the mechanically checkable principles of
  the kit as requirements.
- Add `evals/tests/test_kit.py` with one test per requirement.
- Rewrite the skill descriptions that summarize their workflow so that each
  says only when to use the skill.
- Add `docs/design.md`: the problem, the principles, the architecture and the
  map against OpenSpec's skills.

## Capabilities

### New Capabilities
- `warrant-kit`: rules every warrant skill follows: agent-neutral text, size,
  "when to use" descriptions, license, eval coverage and a place in the design
  map.

### Modified Capabilities
None.

## Impact

`evals/tests/test_kit.py`; the `description` line of every `skills/*/SKILL.md`;
`docs/design.md`.

## Why code is needed

Only a test makes a principle fail loudly; documentation alone did not prevent
the drift.

## Out of scope

This change makes existing principles checkable; it does not remove
`warrant-design`, narrow `warrant-review` or add apply guidance, which follow in
their own changes.

Features and options deliberately left out:

- Checks that need judgement (duplication with OpenSpec skills, contract-only
  facts); they stay in `docs/design.md` and in review.
- A brevity rule for replies; it comes with the economy change.

## Assumptions

Confirmed by the requester: the seven principles in `docs/design.md`; specs and
design are written as drafts for review.

- A description "says when to use the skill" when it starts with "Use when" or
  "Use before". Owner: requester.
- The agent names checked are Claude, Codex, Copilot, Cursor, Gemini and agy,
  and the tool words are "Skill tool", "Task tool", "TodoWrite" and "subagent".
  Owner: requester.
