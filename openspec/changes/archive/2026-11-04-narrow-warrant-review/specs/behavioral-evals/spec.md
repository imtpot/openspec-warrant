# Spec Delta

## ADDED Requirements

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
