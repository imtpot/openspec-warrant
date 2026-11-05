## ADDED Requirements

### Requirement: Development runs allowed

WHILE the agent works on a change, the verify skill SHALL allow narrowed or
diagnostic runs of a test, lint, type-check or build tool.

#### Scenario: Single test while working
- **WHEN** the agent runs `uv run pytest tests/test_quota.py -k shortfall` during a red step
- **THEN** the run is allowed and the skill does not require the full suite for that step

### Requirement: Only contract commands are evidence

The verify skill SHALL count only the contract's verification commands, run
exactly as written after the last change, as evidence for a completion claim.

#### Scenario: Claim backed only by a narrowed run
- **WHEN** the only passing run after the last change is `uv run pytest tests/test_quota.py`
- **THEN** the agent runs `uv run pytest` as written before it claims completion
