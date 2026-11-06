## MODIFIED Requirements

### Requirement: No OpenSpec root

IF the project has no OpenSpec root, THEN the setup skill SHALL stop without
writing files and name `openspec init --tools agents` without a `--profile`
option.

#### Scenario: Plain repository
- **WHEN** setup runs in a repository without `openspec/`
- **THEN** no file is created and the output names `openspec init --tools agents`

#### Scenario: Root of an enclosing repository
- **WHEN** setup runs in a project without `openspec/` inside a directory tree
  whose parent has an OpenSpec root
- **THEN** setup treats the project as having no root and creates no file

#### Scenario: Global custom profile kept
- **WHEN** setup names the init command
- **THEN** the command has no `--profile` option that would override the user's global profile

### Requirement: Install the rules

WHEN the user runs `warrant-setup` in a project with an OpenSpec root, the setup
skill SHALL add warrant's rules and guidance to `openspec/config.yaml`, taking
`rules.yaml` first from the directory of the loaded `SKILL.md`.

#### Scenario: Fresh project
- **WHEN** setup runs in a project created with `openspec init`
- **THEN** `openspec/config.yaml` contains `[warrant] ` rules for proposal, specs, design and tasks and `[warrant] ` apply guidance

#### Scenario: Agent-specific install
- **WHEN** the skill is installed only under `.claude/skills/warrant-setup/`
- **THEN** setup reads the `rules.yaml` next to that `SKILL.md` and does not stop
