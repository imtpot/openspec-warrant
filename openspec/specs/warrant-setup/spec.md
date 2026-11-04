# warrant-setup Specification

## Purpose
Defines how the `warrant-setup` skill installs the warrant schema and the
project contract into a target project that already uses OpenSpec 1.16.

## Requirements

### Requirement: Create the contract skeleton

WHEN the root `AGENTS.md` has no warrant contract, the setup skill SHALL append
the contract section with all four subsections.

#### Scenario: AGENTS.md without contract
- **WHEN** `AGENTS.md` exists without `## Warrant contract`
- **THEN** setup appends the section and leaves the existing content unchanged

#### Scenario: Standards found
- **WHEN** the project has a `CONTRIBUTING.md` with coding rules
- **THEN** setup proposes it under `### Standards` and writes it after the user confirms

### Requirement: Create AGENTS.md

IF the project has no root `AGENTS.md`, THEN the setup skill SHALL create it
with only the contract section.

#### Scenario: No AGENTS.md
- **WHEN** setup runs in a project without `AGENTS.md`
- **THEN** `AGENTS.md` exists and contains only the warrant contract section

### Requirement: Propose verification commands

WHEN the setup skill creates the contract, the setup skill SHALL propose
verification commands found in the project's own configuration and write them
only after the user confirms them.

#### Scenario: Project with a test task
- **WHEN** the project defines a test command in its build configuration
- **THEN** setup proposes that command and asks the user to confirm it

### Requirement: Keep an existing contract

WHILE the root `AGENTS.md` already contains a warrant contract, the setup skill
SHALL leave the contract unchanged.

#### Scenario: Second run
- **WHEN** setup runs twice in the same project
- **THEN** the second run does not change `AGENTS.md`

### Requirement: Report the OpenSpec skills command

WHEN setup completes, the setup skill SHALL print the `skills add` command that
installs the Fission-AI/OpenSpec workflow skills at the release tag matching the
installed OpenSpec version.

#### Scenario: Completion message
- **WHEN** setup completes with OpenSpec 1.16.0 installed
- **THEN** the output contains a `skills add` command with the `v1.16.0` tag

### Requirement: No OpenSpec root

IF the project has no OpenSpec root, THEN the setup skill SHALL stop without
writing files and tell the user to run `openspec init`.

#### Scenario: Plain repository
- **WHEN** setup runs in a repository without `openspec/`
- **THEN** no file is created and the output names `openspec init`

#### Scenario: Root of an enclosing repository
- **WHEN** setup runs in a project without `openspec/` inside a directory tree
  whose parent has an OpenSpec root
- **THEN** setup treats the project as having no root and creates no file

### Requirement: Unsupported OpenSpec version

IF the installed OpenSpec CLI is older than 1.16, THEN the setup skill SHALL
stop without writing files and report the installed and supported versions.

#### Scenario: Older CLI
- **WHEN** `openspec --version` prints `1.15.0`
- **THEN** setup reports `1.15.0` and `1.16` and writes nothing

### Requirement: Install the rules

WHEN the user runs `warrant-setup` in a project with an OpenSpec root, the setup
skill SHALL add warrant's rules and guidance to `openspec/config.yaml`.

#### Scenario: Fresh project
- **WHEN** setup runs in a project created with `openspec init`
- **THEN** `openspec/config.yaml` contains `[warrant] ` rules for proposal, specs, design and tasks and `[warrant] ` apply guidance

### Requirement: Keep the project's configuration

The setup skill SHALL leave every configuration entry that does not start with
`[warrant] `, and the `schema` field, unchanged.

#### Scenario: Project with own rules
- **WHEN** `openspec/config.yaml` has its own `context`, rules and `schema: spec-driven`
- **THEN** after setup they are unchanged and warrant's entries come after the project's own

### Requirement: Replace warrant entries on upgrade

WHILE `openspec/config.yaml` already holds `[warrant] ` entries, the setup skill
SHALL replace exactly those entries with the shipped ones.

#### Scenario: Second run
- **WHEN** setup runs twice in the same project
- **THEN** the second run leaves `openspec/config.yaml` unchanged

### Requirement: Draft the OpenSpec context

WHILE `context` in `openspec/config.yaml` is missing or empty, the setup skill
SHALL propose a context of at most 10 lines with only those constraints from
the project's own documents that an agent cannot infer from the code.

#### Scenario: Constraint in the README
- **WHEN** the README states that all user-facing text is German
- **THEN** setup proposes a context line with that constraint

#### Scenario: Discoverable facts
- **WHEN** the project has a `Makefile` with a `test` target
- **THEN** the proposed context names neither the test command nor the build tool

### Requirement: Write only confirmed context

WHEN the user confirms lines of the proposed context, the setup skill SHALL
write only those lines as `context` and keep every other key and comment.

#### Scenario: User confirms none
- **WHEN** the user confirms no line
- **THEN** `openspec/config.yaml` has no `context` value

### Requirement: Keep existing context

WHILE `context` in `openspec/config.yaml` is not empty, the setup skill SHALL
leave it unchanged.

#### Scenario: Context written by the team
- **WHEN** `context` already holds the team's text
- **THEN** after setup OpenSpec renders the same context

### Requirement: No confirmed destructive actions

IF the user confirms no destructive action, THEN the setup skill SHALL leave
the Destructive actions subsection empty.

#### Scenario: Nothing confirmed
- **WHEN** setup proposes `make deploy` and the user confirms none
- **THEN** `### Destructive actions` has no entry
