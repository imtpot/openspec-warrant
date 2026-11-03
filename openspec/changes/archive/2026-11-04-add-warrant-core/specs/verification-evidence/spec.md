# Spec Delta

## Purpose

Defines the `warrant-verify` skill: no claim that work is complete, fixed or
passing without running the project's declared verification commands and
reading their output in the same session.

## ADDED Requirements

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
last change to the files under verification.

#### Scenario: Edit after a test run
- **WHEN** the agent edits a file after the last test run
- **THEN** the agent runs the tests again before it claims completion

### Requirement: Destructive verification

IF a verification command matches an entry in the contract's Destructive
actions, THEN the verify skill SHALL direct the agent to ask the user before
running it.

#### Scenario: Deploy-based check
- **WHEN** a verification command starts with a listed destructive prefix
- **THEN** the agent asks for approval and does not run it without approval
