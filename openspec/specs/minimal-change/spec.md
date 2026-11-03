# minimal-change Specification

## Purpose
Defines the `warrant-minimal-change` skill: the smallest complete change in
which every changed line is warranted by a requirement, and every deliberate
limitation is recorded so it cannot silently become permanent.

## Requirements

### Requirement: Option ladder before code

WHEN an agent applies the minimal-change skill to a task, the minimal-change
skill SHALL direct the agent to take the first option that fully works, in this
order: no change, existing project code, standard library or platform,
installed dependency, new code.

#### Scenario: Helper already exists
- **WHEN** the project already has a function that does what the task needs
- **THEN** the change calls that function and adds no new one

### Requirement: Name skipped features

WHEN the agent leaves out a feature or option the request did not ask for, the
minimal-change skill SHALL direct the agent to name it in one line of its report.

#### Scenario: Unrequested option
- **WHEN** a request asks for JSON output only
- **THEN** the report names any output format it did not add

### Requirement: Complete change

The minimal-change skill SHALL direct the agent to update every caller, test,
fixture and configuration that the change breaks.

#### Scenario: Signature change
- **WHEN** the change alters a function signature
- **THEN** every caller in the project is updated in the same change

### Requirement: Every line traces to a requirement

WHILE a change belongs to an OpenSpec change, the minimal-change skill SHALL
direct the agent to remove any added line that no requirement of that change
needs.

#### Scenario: Speculative parameter
- **WHEN** the diff adds a parameter that no requirement uses
- **THEN** the agent removes the parameter before completion

### Requirement: Protected code

The minimal-change skill SHALL direct the agent never to remove validation at
trust boundaries, error handling that prevents data loss, or security checks to
make a change smaller.

#### Scenario: Shorter without validation
- **WHEN** removing an input check would shorten the diff
- **THEN** the input check stays

### Requirement: Shortcut marker

WHEN the agent accepts a known limitation, the minimal-change skill SHALL direct
the agent to mark it with a comment of the form
`shortcut: <limit>, <when to upgrade>`.

#### Scenario: Fixed page size
- **WHEN** the change reads only the first page of an API result
- **THEN** the code has a comment such as
  `shortcut: first 100 items only, paginate when a project exceeds 100`

### Requirement: Debt ledger

WHEN the user asks for the shortcut ledger, the minimal-change skill SHALL list
every `shortcut:` comment in files tracked by git outside the installed skill
directories `.agents/` and `.claude/`, one line per comment with file, line,
limit and upgrade trigger.

#### Scenario: Two markers
- **WHEN** two tracked files contain one `shortcut:` comment each
- **THEN** the ledger has two lines and a total of 2

### Requirement: Marker without trigger

IF a `shortcut:` comment names no upgrade trigger, THEN the ledger SHALL tag
that line `no-trigger`.

#### Scenario: Bare marker
- **WHEN** a comment reads `shortcut: no retries`
- **THEN** its ledger line is tagged `no-trigger`

### Requirement: Ledger changes nothing

The minimal-change skill SHALL not modify any file while it builds the ledger.

#### Scenario: Ledger run
- **WHEN** the ledger is built
- **THEN** `git status` shows no new changes
