# Spec Delta

## Purpose

Defines how the `warrant-setup` skill installs the warrant schema and the
project contract into a target project that already uses OpenSpec 1.16.

## ADDED Requirements

### Requirement: Install the schema

WHEN the user runs `warrant-setup` in a project with an OpenSpec root, the setup
skill SHALL copy the warrant schema files into `openspec/schemas/warrant/`.

#### Scenario: Fresh project
- **WHEN** `warrant-setup` runs in a project created with `openspec init`
- **THEN** `openspec/schemas/warrant/schema.yaml` exists
- **AND** `openspec schema which warrant` reports the project location

### Requirement: Select the schema

WHEN the setup skill installs the schema, the setup skill SHALL set
`schema: warrant` in `openspec/config.yaml` and keep every other field of that
file unchanged.

#### Scenario: Existing rules
- **WHEN** `openspec/config.yaml` already contains `context` and `rules`
- **THEN** after setup only the `schema` field differs

### Requirement: Create the contract skeleton

WHEN the root `AGENTS.md` has no warrant contract, the setup skill SHALL append
the contract section with all four subsections.

#### Scenario: AGENTS.md without contract
- **WHEN** `AGENTS.md` exists without `## Warrant contract`
- **THEN** setup appends the section and leaves the existing content unchanged

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

### Requirement: Replace an outdated schema

WHILE `openspec/schemas/warrant/` holds files that differ from the shipped
schema, the setup skill SHALL show the differences and replace the files only
after the user confirms.

#### Scenario: Upgrade
- **WHEN** a newer warrant release is installed and setup runs
- **THEN** setup lists the changed schema files and waits for confirmation

### Requirement: Report the OpenSpec skills command

WHEN setup completes, the setup skill SHALL print the `skills add` command that
installs the Fission-AI/OpenSpec workflow skills at the release tag matching the
supported OpenSpec version.

#### Scenario: Completion message
- **WHEN** setup completes
- **THEN** the output contains a `skills add` command with the `v1.16.0` tag

### Requirement: No OpenSpec root

IF the project has no OpenSpec root, THEN the setup skill SHALL stop without
writing files and tell the user to run `openspec init`.

#### Scenario: Plain repository
- **WHEN** setup runs in a repository without `openspec/`
- **THEN** no file is created and the output names `openspec init`

### Requirement: Unsupported OpenSpec version

IF the installed OpenSpec CLI is not version 1.16, THEN the setup skill SHALL
stop without writing files and report the installed and supported versions.

#### Scenario: Older CLI
- **WHEN** `openspec --version` prints `1.15.0`
- **THEN** setup reports `1.15.0` and `1.16` and writes nothing
