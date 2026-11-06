## ADDED Requirements

### Requirement: Repeated runs

The eval runner SHALL run each selected scenario N times per agent, each run in
its own workspace, where N is the value of `--runs` or 1 when the option is
absent.

#### Scenario: Three runs
- **WHEN** the user runs `verify` on `claude` with `--runs 3`
- **THEN** the agent runs three times in three separate workspaces and the report has one `verify` entry for `claude` that reads `k/3`

#### Scenario: Default
- **WHEN** the user runs the evals without `--runs`
- **THEN** each scenario runs once per agent

### Requirement: Invalid run count

IF `--runs` is less than 1, THEN the eval runner SHALL stop with a usage error
before any agent runs.

#### Scenario: Zero runs
- **WHEN** the user passes `--runs 0`
- **THEN** the command exits with a usage error and no agent runs

### Requirement: Entry status from runs

WHEN all runs of a scenario on an agent end, the eval runner SHALL give the
entry the first status in the order fail, not run, pass that any of its runs
has.

#### Scenario: One of three fails
- **WHEN** two runs pass and one run fails
- **THEN** the entry reads fail, `2/3`, and lists the failed run's checker messages

#### Scenario: Agent not installed
- **WHEN** `codex` is not on PATH and `--runs 3` is given
- **THEN** the Codex entry reads not run with the reason

#### Scenario: Not run and pass
- **WHEN** one run passes and one run is not run
- **THEN** the entry reads not run

### Requirement: Scenario suite

The eval runner SHALL read a scenario's suite from its optional `suite` field,
with the value `regression` or `capability` and the default `regression`.

#### Scenario: No suite field
- **WHEN** a scenario file has no `suite` field
- **THEN** the scenario is in the regression suite

### Requirement: Unknown scenario suite

IF a scenario file sets `suite` to a value other than `regression` or
`capability`, THEN the scenario loader SHALL stop with an error that names the
file and the value.

#### Scenario: Misspelled suite
- **WHEN** a scenario file sets `suite = "regresion"`
- **THEN** loading fails with an error that names the file and `regresion`

### Requirement: Exit code by suite

IF a regression entry reads fail, THEN the eval runner SHALL exit with code 1.

#### Scenario: Failed regression scenario
- **WHEN** a regression entry reads fail
- **THEN** the eval runner exits with code 1

### Requirement: Capability entries and the exit code

The eval runner SHALL ignore capability entries when it sets the exit code.

#### Scenario: Failed capability scenario
- **WHEN** only a capability entry reads fail
- **THEN** the eval runner exits with code 0

### Requirement: Judged review findings

WHERE an expected finding of a review scenario has a description, IF no term of
the finding appears in the text of its axis section, THEN the review checker
SHALL count the finding as present only when the judge answers `yes` for that
text.

#### Scenario: Synonym the terms miss
- **WHEN** the Spec section names the unrequested option only as "machine-readable output flag" and the judge answers `yes`
- **THEN** the checker reports no missing finding for it

#### Scenario: Term found
- **WHEN** a term of the finding appears in its axis section
- **THEN** the checker does not call the judge for that finding

#### Scenario: Finding without description
- **WHEN** no term of a finding without a description appears in its axis section
- **THEN** the checker reports the finding as missing without calling the judge

#### Scenario: Unknown verdict
- **WHEN** the judge answers `unknown`
- **THEN** the checker reports the finding as missing and the message says the judge answered unknown

### Requirement: Judge call

WHEN the judge decides a finding, the judge SHALL run the `claude` CLI headless
with the judge model, no tools and a prompt that holds the finding's
description and the report text, and return `yes`, `no` or `unknown`.

#### Scenario: Judge command
- **WHEN** the judge decides a finding
- **THEN** the command runs `claude -p` with `--model sonnet` and `--tools ""`, with the prompt on stdin

### Requirement: Judge failure

IF the judge command is missing, exits with a non-zero code, exceeds its time
limit or returns no verdict, THEN the judge SHALL return `unknown` with the
reason.

#### Scenario: No claude CLI
- **WHEN** `claude` is not on PATH
- **THEN** the judge returns `unknown` with the reason `claude not installed`

### Requirement: Judge calibration

WHEN the user runs `python -m warrant_evals.judge`, the judge SHALL decide
each case of the calibration set and print the number of cases whose verdict
equals the case's label, the number of cases, and each case whose verdict
differs with its verdict and reason.

#### Scenario: One disagreement
- **WHEN** the calibration set has three cases and the judge answers `yes` on a case labeled `no`
- **THEN** the output reads `agreement: 2/3` and names that case with the verdict `yes` and the judge's reason

#### Scenario: Unknown verdict
- **WHEN** the judge answers `unknown` on a case labeled `yes`
- **THEN** the case counts as a disagreement

### Requirement: Calibration file failure

IF the calibration file is missing or is not valid TOML, THEN the judge SHALL
stop with an error that names the file.

#### Scenario: Missing file
- **WHEN** the user runs `python -m warrant_evals.judge` and `evals/judge/calibration.toml` does not exist
- **THEN** the command exits with a non-zero code and an error that names `evals/judge/calibration.toml`

## MODIFIED Requirements

### Requirement: Result report

WHEN a run finishes, the eval runner SHALL write a report with one entry per
scenario and agent that shows the scenario's suite, pass, fail or not run, the
number of passed runs out of all runs, checker messages and the path to each
run's transcript, followed by the number of passed entries out of all entries
for each suite.

#### Scenario: Mixed results
- **WHEN** one scenario passes and one fails
- **THEN** the report lists both, and the failing entry names each failed check

#### Scenario: Totals per suite
- **WHEN** two regression entries pass, one regression entry fails and one capability entry passes
- **THEN** the report ends with `regression: 2/3` and `capability: 1/1`

### Requirement: Checker tests

The artifact checker SHALL have unit tests that run without any agent CLI and
without a call to the judge.

#### Scenario: Offline test run
- **WHEN** `uv run pytest` runs on a machine without agent CLIs
- **THEN** the checker tests run and pass
