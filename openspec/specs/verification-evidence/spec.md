# verification-evidence Specification

## Purpose
Defines the `warrant-verify` skill: no claim that work is complete, fixed or
passing without running the project's declared verification commands and
reading their output in the same session.

## Requirements

### Requirement: Run before claiming

WHEN an agent is about to claim that work is complete, fixed or passing, the
verify skill SHALL direct the agent to run every verification command of the
project contract first.

#### Scenario: Task completion
- **WHEN** the agent finishes a task and the contract lists tests and lint
- **THEN** the agent runs both commands before it reports the task as done

### Requirement: Evidence in the report

WHEN the agent reports completion, the verify skill SHALL direct the agent to
include, per command, the command, its exit code and the line of output that
shows the result.

#### Scenario: Passing tests
- **WHEN** `uv run pytest` exits with code 0
- **THEN** the report shows the command, exit code 0 and the summary line, such
  as `42 passed`

### Requirement: Failing check blocks the claim

IF a verification command exits with a non-zero code, THEN the verify skill
SHALL direct the agent to report the failure with its output and not to claim
completion.

#### Scenario: One failing test
- **WHEN** the test command exits with code 1
- **THEN** the report states that verification failed and quotes the failing test

### Requirement: Check that cannot run

IF a verification command cannot run, THEN the verify skill SHALL direct the
agent to report it as not run with the reason, and not as passed.

#### Scenario: Missing tool
- **WHEN** a verification command fails because the tool is not installed
- **THEN** the report lists the command as not run and names the missing tool

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

### Requirement: Only contract commands are evidence

The verify skill SHALL count only the contract's verification commands, run
exactly as written after the last change, as evidence for a completion claim.

#### Scenario: Claim backed only by a narrowed run
- **WHEN** the only passing run after the last change is `uv run pytest tests/test_quota.py`
- **THEN** the agent runs `uv run pytest` as written before it claims completion
