# Proposal

## Why

warrant requires a test task per requirement and `warrant-review` reports
untested requirements, but nothing makes the tests come first or tie them to
the requirement they cover. Tests written after the code tend to confirm what
the code does instead of what the requirement asks, and a reviewer has to guess
which test covers which scenario.

## What Changes

- Add the `warrant-tdd` skill: red → green, one requirement scenario at a time.
  - At least one test per scenario of the requirement being implemented, named
    or commented with the requirement and scenario.
  - Each new test runs and fails for the expected reason before any code for it
    is written; then the least code makes it pass.
  - Single tests run with the contract's tests command narrowed by that tool's
    own selection; the full verification runs at the end through `warrant-verify`.
  - The report shows, per scenario, the failing and the passing result.
- Add TDD eval scenarios.

## Capabilities

### New Capabilities
- `test-first`: the behavior of the `warrant-tdd` skill.

### Modified Capabilities
- `behavioral-evals`: TDD scenarios join the eval set.

## Impact

New `skills/warrant-tdd/SKILL.md`; checkers, fixtures and scenarios in
`evals/`; `README.md`, the `AGENTS.md` setup command and the dogfood skill list.
No change to the schema or the contract format.

## Why code is needed

No configuration or tool makes an agent run a new test and see it fail before
writing code, or ties tests to OpenSpec scenarios.

## Out of scope

This change adds the TDD skill; it does not add a refactoring step, measure
coverage or change how `warrant-verify` runs the full suite.

Features and options deliberately left out:

- A refactoring step inside the loop; structure changes go through `warrant-review`.
- Selecting or checking off tasks in `tasks.md`; that is `openspec-apply-change`'s job.
- Coverage thresholds.
- A contract entry for a single-test command.
- Generating tests for code that already exists without a requirement.

## Assumptions

Confirmed by the requester: `warrant-tdd` is the next v2 skill; red and green
runs use the contract's tests command narrowed to one test with the tool's own
selection; each test names its requirement and scenario in its name or a
one-line comment; without an active OpenSpec change the skill states the
scenarios it derives from the request before writing tests; a new test that
passes before any code is written means the behavior exists and no code is
written for it; a contract without a tests entry stops the skill with a pointer
to `warrant-setup`; the skill does not select or check off tasks, which the
OpenSpec apply workflow does.

None.
