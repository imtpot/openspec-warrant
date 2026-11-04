# Spec Delta

## ADDED Requirements

### Requirement: Minimal change without naming the skill

The evals SHALL include a minimal-change scenario whose prompt names no skill.

#### Scenario: Plain task
- **WHEN** the agent gets the slug task without a skill name
- **THEN** the checker fails a run that adds a new helper instead of calling `slugify`
