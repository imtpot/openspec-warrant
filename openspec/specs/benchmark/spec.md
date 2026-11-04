# benchmark Specification

## Purpose
Defines the benchmark that runs the same tasks with no kit, with plain OpenSpec
and with OpenSpec plus warrant, and scores hidden acceptance tests, faults the
agent's tests reject, planted review problems and tokens.

## Requirements

### Requirement: Three arms

WHEN the benchmark runs a task on an agent, the benchmark SHALL run it in the
`bare`, `openspec` and `warrant` arms with the same fixture and prompt.

#### Scenario: One task, one agent
- **WHEN** the benchmark runs the implement task on `claude` with one run
- **THEN** it reports one `bare`, one `openspec` and one `warrant` result

### Requirement: Baseline arms

WHERE the arm is `bare` or `openspec`, the benchmark SHALL replace the Warrant
contract in `AGENTS.md` with plain text that names the same verification
commands and standards files, and install no warrant skill or rule.

#### Scenario: No skills in bare
- **WHEN** the `bare` arm workspace is prepared
- **THEN** it has no installed skill

#### Scenario: Contract becomes text
- **WHEN** the fixture contract lists `make test` and `docs/standards.md`
- **THEN** the baseline `AGENTS.md` names both and has no `## Warrant contract`

### Requirement: Warrant arm

WHERE the arm is `warrant`, the benchmark SHALL install the warrant skills and
merge the shipped rules into `openspec/config.yaml`.

#### Scenario: Rules present
- **WHEN** the warrant arm workspace is prepared
- **THEN** OpenSpec renders every shipped `[warrant]` entry

### Requirement: Implement task scores

WHEN an implement run ends, the benchmark SHALL record the number of hidden
acceptance tests passed, the share of faulty implementations that the agent's
tests reject, and the non-test lines the agent added.

#### Scenario: Tests catch two of three faults
- **WHEN** the agent's tests pass on the reference implementation and fail on two of three faulty implementations
- **THEN** the run records a fault detection share of 2/3

### Requirement: Invalid agent tests

IF the agent's tests fail on the reference implementation, THEN the benchmark
SHALL record the fault detection share as not measured.

#### Scenario: Wrong expectation in a test
- **WHEN** an agent's test expects a value the requirements do not give
- **THEN** the run shows fault detection as not measured

### Requirement: Review task score

WHEN a review run ends, the benchmark SHALL record the share of planted
problems that the agent's report names.

#### Scenario: Two of three problems named
- **WHEN** the report names two of three planted problems
- **THEN** the run records 2/3

### Requirement: No user settings for Claude

WHEN the benchmark runs Claude, the benchmark SHALL load only project and
local settings.

#### Scenario: User plugin installed
- **WHEN** the user has a plugin enabled in user settings
- **THEN** the benchmark's Claude command passes `--setting-sources project,local`

### Requirement: Token usage

WHEN a run ends, the benchmark SHALL record the tokens that the agent reports.

#### Scenario: Codex usage line
- **WHEN** the Codex output ends with `tokens used` and `21,806`
- **THEN** the run records 21806 tokens

### Requirement: Missing usage

IF an agent reports no token usage, THEN the benchmark SHALL record the tokens
as not measured.

#### Scenario: No usage line
- **WHEN** the Codex output has no `tokens used` line
- **THEN** the run shows tokens as not measured

### Requirement: Summary table

WHEN all runs end, the benchmark SHALL write a table with the mean of each
score per task, agent and arm, and the number of runs behind each mean.

#### Scenario: Three runs
- **WHEN** three warrant runs record fault detection 1, 2/3 and 1
- **THEN** the table shows 0.89 with 3 runs

### Requirement: Run list

WHEN all runs end, the benchmark SHALL write one row per run with the faults
its tests let through or the planted problems its report missed.

#### Scenario: One fault let through
- **WHEN** a run's tests accept the faulty implementation `bankers_rounding.py`
- **THEN** its row lists `bankers_rounding.py`

### Requirement: Kept workspaces

WHERE `--keep` is given, the benchmark SHALL keep each run's workspace and
list its path in the run's row.

#### Scenario: Inspect an agent's tests
- **WHEN** the benchmark runs with `--keep`
- **THEN** each row names a workspace directory that still exists
