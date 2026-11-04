# Spec Delta

## ADDED Requirements

### Requirement: Purpose after archive

The warrant archive guidance SHALL direct the agent to replace the placeholder
Purpose of every main spec that the archive creates with what the capability
is for.

#### Scenario: New capability archived
- **WHEN** archiving a change creates `openspec/specs/benchmark/spec.md` with a placeholder Purpose
- **THEN** the guidance asks the agent to write the capability's purpose there
