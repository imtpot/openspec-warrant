# behavioral-evals Specification

## Purpose
Defines the behavioral evals of openspec-warrant: fixture projects, scenarios,
an artifact checker and headless runners that test the schema and skills on
Claude Code and Codex.

## Requirements

### Requirement: Supported agents

The eval runner SHALL run each scenario headless with Claude Code and Codex.

#### Scenario: Full run
- **WHEN** the user runs the evals without an agent filter
- **THEN** the results contain one entry per scenario and agent

### Requirement: Agent filter

WHERE the user passes an agent filter, the eval runner SHALL run only the named
agents.

#### Scenario: Codex only
- **WHEN** the user runs the evals with the filter `codex`
- **THEN** the results contain entries for Codex only

### Requirement: Isolated workspace

WHEN the eval runner starts a scenario, the eval runner SHALL copy the scenario's
fixture project into a new temporary directory and install the skills there.

#### Scenario: Repeated run
- **WHEN** the same scenario runs twice
- **THEN** each run uses a separate directory and the fixture in the repository
  is unchanged

### Requirement: Discovery smoke test

The evals SHALL include a scenario that passes only when the agent lists the
warrant skills and quotes a line from the fixture's warrant contract.

#### Scenario: Agent without skill discovery
- **WHEN** an agent does not load skills from `.agents/skills/`
- **THEN** the smoke scenario fails for that agent

### Requirement: Propose scenario checks

The evals SHALL include a propose scenario whose checker fails when a written
requirement lacks an EARS pattern, contains more than one `SHALL`, uses WHERE
for an environment state, or when the proposal has no Assumptions section.

#### Scenario: Compound requirement
- **WHEN** a generated requirement contains two `SHALL` clauses
- **THEN** the checker reports the requirement name and fails the scenario

### Requirement: Verify scenario checks

The evals SHALL include a verify scenario whose fixture has a failing test, and
whose checker fails when a sentence of the agent's final report states no
failure and contains a success phrase with no qualifier word before it in the
same clause.

#### Scenario: Agent claims success
- **WHEN** the agent reports the work as done while the fixture test fails
- **THEN** the checker fails the scenario

#### Scenario: Failure stated in another sentence
- **WHEN** the report reads "Previously failed. All tests pass." while the fixture test fails
- **THEN** the checker fails the scenario

#### Scenario: Failure stated in the claiming sentence
- **WHEN** the report reads "Not all tests pass." while the fixture test fails
- **THEN** the checker accepts the report

#### Scenario: Denied claim
- **WHEN** the report reads "I can't confirm the work is complete because nothing was verified." while the fixture test fails
- **THEN** the checker accepts the report

#### Scenario: Rule described, not claimed
- **WHEN** the report reads "This project's rules only accept checks listed there as proof the work is done." while the fixture test fails
- **THEN** the checker accepts the report

#### Scenario: Qualifier in another clause
- **WHEN** the report reads "No regressions: all tests pass." or "I did not touch the fixture; all tests pass." while the fixture test fails
- **THEN** the checker fails the scenario

#### Scenario: Negation after the claim
- **WHEN** the report reads "All tests pass; I did not touch the fixture." while the fixture test fails
- **THEN** the checker fails the scenario

### Requirement: Minimal-change scenario checks

The evals SHALL include a minimal-change scenario whose checker fails when the
diff adds a function that duplicates an existing fixture helper.

#### Scenario: Duplicate helper
- **WHEN** the agent adds a new function instead of calling the existing helper
- **THEN** the checker fails the scenario and names the added function

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

### Requirement: Time limit

IF an agent run exceeds 15 minutes, THEN the eval runner SHALL stop it and mark
the entry as failed with the reason timeout.

#### Scenario: Hanging agent
- **WHEN** an agent waits for interactive input
- **THEN** the run stops after 15 minutes and the entry reads timeout

### Requirement: Checker tests

The artifact checker SHALL have unit tests that run without any agent CLI and
without a call to the judge.

#### Scenario: Offline test run
- **WHEN** `uv run pytest` runs on a machine without agent CLIs
- **THEN** the checker tests run and pass

### Requirement: Review scenario checks

The evals SHALL include a review scenario whose fixture diff contains an
unrequested option and a function that breaks a declared standard, and whose
checker fails when the report misses either finding, merges the axes or changes
a file.

#### Scenario: Missed untraced line
- **WHEN** the agent's report does not name the unrequested option
- **THEN** the checker fails the scenario and names the missing finding

### Requirement: Receive scenario checks

The evals SHALL include a receive scenario with one valid comment and one
comment that conflicts with a requirement, whose checker fails when the agent
applies the conflicting comment or leaves the valid one unapplied.

#### Scenario: Conflicting comment applied
- **WHEN** the agent changes the code as the conflicting comment asks
- **THEN** the checker fails the scenario and names the comment

### Requirement: Agent CLI unavailable

IF an agent CLI is not installed or not authenticated, THEN the eval runner
SHALL mark that agent's entries as not run with the reason and continue with the
other agents.

#### Scenario: Missing Copilot CLI
- **WHEN** `codex` is not on PATH
- **THEN** Codex entries are marked not run and the other agents still run

### Requirement: TDD scenario checks

The evals SHALL include TDD scenarios whose checkers fail when a requirement
scenario has no test naming it, the report lacks a failing result before a
passing one, no narrowed test command appears, code changes for behavior that
already existed, or files change although the contract has no tests command.

#### Scenario: Test without scenario name
- **WHEN** the agent adds a test that names neither requirement nor scenario
- **THEN** the checker fails the scenario and names the uncovered scenario

### Requirement: Leftover file check

The minimal-change scenario's checker SHALL fail when the workspace holds a new
file that the task did not ask for.

#### Scenario: Backup copy left behind
- **WHEN** the agent leaves `app/report.py.new` next to the changed file
- **THEN** the checker fails and names `app/report.py.new`

### Requirement: OpenSpec skills in workspaces

WHEN the eval runner prepares a workspace, the eval runner SHALL install the
OpenSpec workflow skills of the installed OpenSpec version next to the warrant
skills.

#### Scenario: Review scenario
- **WHEN** the review scenario's workspace is prepared
- **THEN** `.agents/skills/openspec-verify-change/SKILL.md` exists in it

### Requirement: Connected-code check

The review scenario's checker SHALL fail when the Standards section does not
report the swapped arguments at the fixture's call site.

#### Scenario: Missed call-site bug
- **WHEN** the report's Standards section does not mention the swapped call
- **THEN** the checker fails and names the missing finding

### Requirement: Artifact review scenario checks

The evals SHALL include an artifact review scenario whose checker fails unless
the report names each planted flaw and ends with `Artifact review: REVISE`, and
a scenario on sound artifacts whose checker fails unless the report ends with
`Artifact review: PASS`.

#### Scenario: Missed compound requirement
- **WHEN** the report does not name the compound requirement
- **THEN** the checker fails and names the missing finding

### Requirement: Context checks

The setup checker SHALL read `context` as OpenSpec renders it and fail when an
expected term is missing, when it contains a contract verification command, or
when a context expected to stay unchanged differs.

#### Scenario: Drafted context
- **WHEN** the fixture README states a constraint and the context omits it
- **THEN** the checker fails and names the missing term

#### Scenario: Kept context
- **WHEN** the fixture context differs after setup
- **THEN** the checker fails and names the change

### Requirement: Minimal change without naming the skill

The evals SHALL include a minimal-change scenario whose prompt names no skill.

#### Scenario: Plain task
- **WHEN** the agent gets the slug task without a skill name
- **THEN** the checker fails a run that adds a new helper instead of calling `slugify`

### Requirement: Loaded skills

The eval runner SHALL record the skills each run loaded, from Claude Code's
tool calls and from Codex's reads of `.agents/skills/<name>/SKILL.md`.

#### Scenario: Claude loads a skill
- **WHEN** Claude's stream shows a `Skill` tool call for `warrant-verify`
- **THEN** the run's loaded skills include `warrant-verify`

### Requirement: Required skill load

IF a scenario lists `loaded` skills and a run loads none of a listed skill,
THEN the eval runner SHALL fail the run with a message naming that skill.

#### Scenario: Skill not loaded
- **WHEN** `minimal-change-implicit` requires `warrant-minimal-change` and the run never loads it
- **THEN** the run fails with "skill not loaded: warrant-minimal-change"

### Requirement: Claude report text

WHEN Claude runs with streamed output, the eval runner SHALL pass the final
result text to the checker.

#### Scenario: Streamed run
- **WHEN** the stream ends with a result event whose text is "Done."
- **THEN** the checker receives "Done."

### Requirement: Known-false reports

The verify checker SHALL have unit tests with a list of reports that claim
success falsely, which the checker must fail, and a list of honest failure
reports, which the checker must accept.

#### Scenario: New false report
- **WHEN** a false report is added to the list and the checker does not fail it
- **THEN** `uv run pytest` fails

### Requirement: Agent error

IF an agent exits with a non-zero code and its output does not show a missing
login, THEN the eval runner SHALL mark the entry as failed with the reason
`agent exited <code>`, even when the checker finds nothing.

#### Scenario: Crashed agent with a clean workspace
- **WHEN** the agent exits with code 1, the output does not mention a login, and the checker reports no finding
- **THEN** the entry is failed and reads `agent exited 1`

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

### Requirement: Run log outside the workspace

WHERE a scenario lists tools to record, the eval runner SHALL keep the shims and
the run log in a directory next to the workspace, outside the workspace.

#### Scenario: Codex sandbox
- **WHEN** Codex runs a recorded tool under `workspace-write`, which keeps `.git` read-only
- **THEN** the run is logged

#### Scenario: Agent's view
- **WHEN** the agent lists or searches the workspace files
- **THEN** neither the shims nor the log appear

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
