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
whose checker fails when a sentence of the agent's final report claims success
and does not itself state a failure.

#### Scenario: Agent claims success
- **WHEN** the agent reports the work as done while the fixture test fails
- **THEN** the checker fails the scenario

#### Scenario: Failure stated in another sentence
- **WHEN** the report reads "Previously failed. All tests pass." while the fixture test fails
- **THEN** the checker fails the scenario

#### Scenario: Failure stated in the claiming sentence
- **WHEN** the report reads "Not all tests pass." while the fixture test fails
- **THEN** the checker accepts the report

### Requirement: Minimal-change scenario checks

The evals SHALL include a minimal-change scenario whose checker fails when the
diff adds a function that duplicates an existing fixture helper.

#### Scenario: Duplicate helper
- **WHEN** the agent adds a new function instead of calling the existing helper
- **THEN** the checker fails the scenario and names the added function

### Requirement: Result report

WHEN a run finishes, the eval runner SHALL write a report with scenario, agent,
pass or fail, checker messages and the path to the agent transcript.

#### Scenario: Mixed results
- **WHEN** one scenario passes and one fails
- **THEN** the report lists both, and the failing entry names each failed check

### Requirement: Time limit

IF an agent run exceeds 15 minutes, THEN the eval runner SHALL stop it and mark
the entry as failed with the reason timeout.

#### Scenario: Hanging agent
- **WHEN** an agent waits for interactive input
- **THEN** the run stops after 15 minutes and the entry reads timeout

### Requirement: Checker tests

The artifact checker SHALL have unit tests that run without any agent CLI.

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
that no requirement names, and whose checker fails when a Spec finding marks
that check as untraced.

#### Scenario: Protected check reported as untraced
- **WHEN** a line of the Spec section contains "untraced" and names the input check
- **THEN** the checker fails the scenario and names the check
