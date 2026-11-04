# Spec Delta

## ADDED Requirements

### Requirement: Artifact review before apply

The warrant apply guidance SHALL ask for a `warrant-review` artifact review
before the first task and for implementation only after `Artifact review: PASS`.

#### Scenario: Rendered apply guidance
- **WHEN** `openspec instructions apply --json` runs for a change after setup
- **THEN** its `operationGuidance` asks for the artifact review before the first task
