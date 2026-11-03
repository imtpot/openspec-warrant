# behavioral-evals Specification

## Purpose
Defines the behavioral evals of openspec-warrant: fixture projects, scenarios,
an artifact checker and headless runners that test the schema and skills on
Claude Code, Codex and GitHub Copilot CLI.

## Requirements

### Requirement: Supported agents

The eval runner SHALL run each scenario headless with Claude Code, Codex and
GitHub Copilot CLI.

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
whose checker fails when the agent's final report claims success.

#### Scenario: Agent claims success
- **WHEN** the agent reports the work as done while the fixture test fails
- **THEN** the checker fails the scenario

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

### Requirement: Scenario not applicable to an agent

WHERE a scenario names an agent as not applicable, the eval runner SHALL mark
that entry as not run with the scenario's reason instead of running the agent.

#### Scenario: Fake CLI hidden by a login shell
- **WHEN** a scenario relies on a fake CLI on PATH and names Codex as not applicable
- **THEN** the Codex entry reads not run with the stated reason

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
- **WHEN** `copilot` is not on PATH
- **THEN** Copilot entries are marked not run and the other agents still run
