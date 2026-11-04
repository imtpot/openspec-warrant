# Proposal

## Why

In the benchmark's implement task on Claude, the tests that warrant's agent
wrote rejected 67% of the faulty implementations, against 92% for plain
OpenSpec and 75% with no kit. The kept workspaces show why: `warrant-tdd`
takes the scenarios from the spec, and the agent tested exactly those eight
examples. Plain OpenSpec also tested what the requirement text states but no
example shows: an exact half cent rounded up, a range after the period, a
period whose end equals its start. Those three cases are the faults warrant
missed. Catching faults is the kit's purpose; a TDD skill that narrows tests
to the examples works against it.

## What Changes

- `warrant-tdd` lists, besides the spec's scenarios, one case for each
  boundary or condition that a requirement's text states and none of its
  scenarios shows, and runs red and green for each.
- The report names these cases.
- Each expected value is a literal from the spec or a worked example, not a
  value the code under test computes (Pocock and superpowers agree).
- Only external systems, time and randomness are replaced with test doubles.
- Before finishing, the skill checks realistic mutations of the changed code
  and adds a test for each one no test catches (superpowers' mutation check).
- The benchmark takes `--arm` to run only some arms.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `test-first`: boundary cases from the requirement text.
- `benchmark`: arm filter.

## Impact

`skills/warrant-tdd/SKILL.md`, `evals/warrant_evals/benchmark.py`, their
tests, `README.md`.

## Why code is needed

The skill text carries the behavior; the arm filter is a small code change in
the benchmark.

## Out of scope

This change widens what `warrant-tdd` tests; it does not change how tests are
run or reported otherwise.

Features and options deliberately left out:

- Property-based or generated tests.
- Agreeing test seams with the user (Pocock): in a change, the spec and design
  already fix the interface.
- A refactor step in the loop.
- Rules that ask spec authors for more scenarios; the requirement text already
  states the cases.

## Assumptions

Confirmed by the requester: quality, not token economy, is the main goal; fix
`warrant-tdd` first; take the independent expected values, boundary-only mocks
and the mutation check from the Pocock and superpowers TDD skills; keep
vertical slices and leave refactoring out of the loop.

- A boundary case is a comparison (before, after, not after, at least), an
  exact rounding point, an empty or zero input, or a case on the other side of
  a stated condition. Owner: requester (decided while the requester was away).
- Success is fault detection in the warrant arm at least equal to plain
  OpenSpec's 0.92 over three Claude runs. Owner: requester (decided while the
  requester was away).
