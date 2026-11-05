## ADDED Requirements

### Requirement: Recorded command runs

WHERE a scenario lists tools to record, the eval runner SHALL log each run of
those tools during the agent run with its order, tool name, arguments, working
directory, exit code and a hash of the workspace files at its start.

#### Scenario: Piped failing test
- **WHEN** the agent runs `python3 -m unittest tests.test_quota 2>&1 | tail -1` and the test fails
- **THEN** the log has a `python3` run with a non-zero exit code

#### Scenario: Nested run
- **WHEN** the agent runs `make test` and `make` starts `python3`
- **THEN** the log has a `make` run and a `python3` run

#### Scenario: Tool behavior unchanged
- **WHEN** a recorded tool runs
- **THEN** it gets the same arguments, input and environment apart from PATH and the recorder's own variables, and its output and exit code reach the agent unchanged

### Requirement: Recorder failure

IF the recorder cannot write its log, THEN the recorder SHALL still run the real
tool and pass its output and exit code through unchanged.

#### Scenario: Read-only log directory
- **WHEN** the log file cannot be opened for writing
- **THEN** the tool runs, its exit code reaches the agent, and the recorder writes one warning line to stderr

### Requirement: Recorded red and green

WHERE a TDD scenario records its test tool, the TDD checker SHALL fail a
`red_green` scenario that has no recorded run covering its test with a non-zero
exit code, followed by a recorded run covering its test with exit code 0 on
different workspace files.

#### Scenario: Red claimed but not run
- **WHEN** the report shows a failing and a passing line for "Not enough free" but the log has only passing runs covering its test
- **THEN** the checker fails and names "Not enough free"

#### Scenario: Red and green on the same files
- **WHEN** the failing and the passing run have the same workspace hash
- **THEN** the checker fails and names the scenario

#### Scenario: Test named by a comment, run by module
- **WHEN** the scenario's test is `test_short_verdict` under `# Shortfall verdict: Not enough free`, and the red and green runs are `python3 -m unittest tests.test_quota`
- **THEN** the runs cover the test and the check passes

### Requirement: Recorded full verification

WHERE a TDD or verify scenario records its test tool, the checker SHALL fail
when the last recorded run of the contract's full command did not start on the
final workspace files.

#### Scenario: Edit after the full run
- **WHEN** the agent runs the full tests command and then edits a file
- **THEN** the checker fails with "full verification not run on the final files"

#### Scenario: Full run never made
- **WHEN** the log has no run of the full command
- **THEN** the checker fails with the same message
