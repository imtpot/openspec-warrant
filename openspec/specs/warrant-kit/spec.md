# warrant-kit Specification

## Purpose
Defines the rules every warrant skill follows, in the form that tests can
check: agent-neutral text, size, "when to use" descriptions, license, eval
coverage and a place in the design map.

## Requirements

### Requirement: Agent-neutral skills

The warrant skills SHALL name no agent product and no agent-specific tool.

#### Scenario: Tool name in a skill
- **WHEN** a skill file contains "Skill tool" or "Codex"
- **THEN** the kit test fails and names the file and the word

### Requirement: Skill size

The warrant skills SHALL each stay at or under 150 lines.

#### Scenario: Long skill
- **WHEN** a `SKILL.md` has 151 lines
- **THEN** the kit test fails and names the skill

### Requirement: Description says when to use

The description of each warrant skill SHALL start with "Use when" or "Use before".

#### Scenario: Workflow summary as description
- **WHEN** a description starts with "Implement a requirement test first"
- **THEN** the kit test fails and names the skill

### Requirement: Skill license

The frontmatter of each warrant skill SHALL declare `license: MIT`.

#### Scenario: Missing license
- **WHEN** a skill's frontmatter has no license line
- **THEN** the kit test fails and names the skill

### Requirement: Eval coverage

The evals SHALL contain at least one scenario that lists each warrant skill in
its `skills` field.

#### Scenario: Skill without scenario
- **WHEN** a new skill is added and no scenario lists it in `skills`
- **THEN** the kit test fails and names the skill

### Requirement: Place in the design map

The design document `docs/design.md` SHALL name each warrant skill.

#### Scenario: Skill missing from the design
- **WHEN** a skill is not mentioned in `docs/design.md`
- **THEN** the kit test fails and names the skill
