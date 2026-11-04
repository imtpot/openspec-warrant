# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Report the OpenSpec skills command

WHEN setup completes, the setup skill SHALL print the `skills add` command that
installs the Fission-AI/OpenSpec workflow skills at the release tag matching the
installed OpenSpec version.

#### Scenario: Completion message
- **WHEN** setup completes with OpenSpec 1.16.0 installed
- **THEN** the output contains a `skills add` command with the `v1.16.0` tag

### Requirement: Unsupported OpenSpec version

IF the installed OpenSpec CLI is older than 1.16, THEN the setup skill SHALL
stop without writing files and report the installed and supported versions.

#### Scenario: Older CLI
- **WHEN** `openspec --version` prints `1.15.0`
- **THEN** setup reports `1.15.0` and `1.16` and writes nothing

## REMOVED Requirements

### Requirement: Install the schema
**Reason**: The warrant schema is replaced by rules in the project configuration.
**Migration**: "Install the rules".

### Requirement: Select the schema
**Reason**: Projects stay on `spec-driven`; setup no longer changes the `schema` field.
**Migration**: None.

### Requirement: Replace an outdated schema
**Reason**: There is no schema to replace.
**Migration**: "Replace warrant entries on upgrade".
