# Spec Delta

## MODIFIED Requirements

### Requirement: No OpenSpec root

IF the project has no OpenSpec root and the user does not confirm
`openspec init --tools agents --profile core`, THEN the setup skill SHALL stop
without writing files and name that command.

#### Scenario: Plain repository
- **WHEN** setup runs in a repository without `openspec/` and nobody confirms
- **THEN** no file is created and the output names `openspec init --tools agents`

#### Scenario: Root of an enclosing repository
- **WHEN** setup runs in a project without `openspec/` inside a directory tree
  whose parent has an OpenSpec root
- **THEN** setup treats the project as having no root and creates no file

### Requirement: Unsupported OpenSpec version

IF the OpenSpec CLI is missing or older than 1.16 and the user does not confirm
an install command, THEN the setup skill SHALL stop without writing files and
report the installed version, the supported version and the install command.

#### Scenario: Older CLI
- **WHEN** `openspec --version` prints `1.15.0` and nobody confirms
- **THEN** setup reports `1.15.0`, `1.16` and an install command, and writes nothing

## REMOVED Requirements

### Requirement: Report the OpenSpec skills command

**Reason**: `openspec init --tools agents` installs the OpenSpec workflow
skills for the installed CLI version.
**Migration**: Setup runs or names `openspec init --tools agents --profile core`.

## ADDED Requirements

### Requirement: Confirmed install and init

WHEN the user confirms the install command or the init command, the setup
skill SHALL run it and continue the setup.

#### Scenario: Init confirmed
- **WHEN** a repository has no `openspec/` and the user confirms the init command
- **THEN** setup runs it, merges the rules and creates the contract

### Requirement: OpenSpec skills for every agent directory

WHEN `.agents/skills/` holds `openspec-*` skills, the setup skill SHALL link
each one into every existing `.<agent>/skills/` directory that lacks it.

#### Scenario: Agent directory without OpenSpec skills
- **WHEN** `.claude/skills/` exists and holds no `openspec-propose`
- **THEN** setup creates `.claude/skills/openspec-propose` as a link to `../../.agents/skills/openspec-propose`

### Requirement: Missing verify skill

IF `.agents/skills/openspec-verify-change` does not exist after setup, THEN the
setup skill SHALL report that the Spec axis of `warrant-review` needs it and
name `openspec config profile`.

#### Scenario: Core profile
- **WHEN** init installed the core workflows only
- **THEN** the report names the missing verify skill and `openspec config profile`
