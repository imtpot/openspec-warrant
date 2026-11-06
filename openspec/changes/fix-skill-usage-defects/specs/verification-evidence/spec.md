## MODIFIED Requirements

### Requirement: Fresh evidence only

The verify skill SHALL direct the agent to use only output produced after the
last change to a file the verification commands read, other than a recorded
result in an OpenSpec artifact or in the report.

#### Scenario: Edit after a test run
- **WHEN** the agent edits a file after the last test run
- **THEN** the agent runs the tests again before it claims completion

#### Scenario: Result recorded in tasks.md
- **WHEN** the agent writes a `Result:` line into `tasks.md` after the verification run
- **THEN** the agent does not run the verification commands again for that edit

### Requirement: Destructive verification

IF a command the agent is about to run, including a narrowed or diagnostic
run, starts with an entry in the contract's Destructive actions, THEN the
verify skill SHALL direct the agent to ask the user before running it.

#### Scenario: Deploy-based check
- **WHEN** a verification command starts with a listed destructive prefix
- **THEN** the agent asks for approval and does not run it without approval

#### Scenario: Narrowed destructive run
- **WHEN** the contract lists `make e2e` as destructive and the agent narrows it to one test
- **THEN** the agent asks for approval before the narrowed run

### Requirement: Development runs allowed

WHILE the agent works on a change in a project with a warrant contract, the
verify skill SHALL allow narrowed or diagnostic runs of a test, lint,
type-check or build tool.

#### Scenario: Single test while working
- **WHEN** the agent runs `uv run pytest tests/test_quota.py -k shortfall` during a red step
- **THEN** the run is allowed and the skill does not require the full suite for that step
