# Spec Delta

## MODIFIED Requirements

### Requirement: No OpenSpec root

IF the project has no OpenSpec root, THEN the setup skill SHALL stop without
writing files and name `openspec init --tools agents --profile core`.

#### Scenario: Plain repository
- **WHEN** setup runs in a repository without `openspec/`
- **THEN** no file is created and the output names `openspec init --tools agents`

#### Scenario: Root of an enclosing repository
- **WHEN** setup runs in a project without `openspec/` inside a directory tree
  whose parent has an OpenSpec root
- **THEN** setup treats the project as having no root and creates no file

### Requirement: Unsupported OpenSpec version

IF the OpenSpec CLI is missing or older than 1.16, THEN the setup skill SHALL
stop without writing files and report the installed version, the supported
version and an install command.

#### Scenario: Older CLI
- **WHEN** `openspec --version` prints `1.15.0`
- **THEN** setup reports `1.15.0`, `1.16` and an install command, and writes nothing

## REMOVED Requirements

### Requirement: Confirmed install and init

**Reason**: A global install and `openspec init` are left to the user, who
runs the commands that setup names and the README lists.
**Migration**: Run the named commands, then run `warrant-setup` again.
