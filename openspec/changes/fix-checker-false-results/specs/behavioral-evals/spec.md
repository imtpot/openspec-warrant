## MODIFIED Requirements

### Requirement: Protected line review scenario

The evals SHALL include a review scenario whose fixture diff adds an input check
that no requirement names, and whose checker fails when a blocking untraced
Spec finding names that check in the sentence that says "blocking" and
"untraced" or cites a line range that covers a line of that check.

#### Scenario: Protected check reported as untraced
- **WHEN** a finding of the Spec section names the input check in the sentence that says "blocking" and "untraced"
- **THEN** the checker fails the scenario and names the check

#### Scenario: Check excluded in a later sentence
- **WHEN** the finding cites `app/cli.py:1-12, 15-16` as untraced and a later sentence of the same line reads "The `free < 0` check at lines 13–14 counts as input validation, but it only exists to serve this untraced CLI."
- **THEN** the checker accepts the report

#### Scenario: Check covered by a cited range
- **WHEN** a blocking untraced finding cites `app/cli.py:1-16` and does not name the check
- **THEN** the checker fails the scenario

### Requirement: Recorded full verification

WHERE a TDD or verify scenario records its test tool, the checker SHALL fail
when the last recorded run whose tool and arguments equal the contract's full
command did not start on the final workspace files or, in a TDD scenario, did
not exit with code 0.

#### Scenario: Edit after the full run
- **WHEN** the agent runs the full tests command and then edits a file
- **THEN** the checker fails with "full verification not run on the final files"

#### Scenario: Full run never made
- **WHEN** the log has no run of the full command
- **THEN** the checker fails with the same message

#### Scenario: Narrowed run with the full command as a prefix
- **WHEN** the only run is `python3 -m unittest discover -s tests -t . -k foo` and the contract command is `python3 -m unittest discover -s tests -t .`
- **THEN** the checker fails with "full verification not run on the final files"

#### Scenario: Failing full run in a TDD scenario
- **WHEN** the last full run of a TDD scenario started on the final files and exited with code 1
- **THEN** the checker fails and names the exit code
