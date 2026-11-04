# Spec Delta

## ADDED Requirements

### Requirement: Fresh context with a fallback

WHERE a warrant skill asks for a separate, fresh context, the skill SHALL state
what to do when no separate context is available, in a sentence that starts with
"If you cannot start a separate context".

#### Scenario: Review in a fresh context
- **WHEN** a skill says to run a review in a separate, fresh context
- **THEN** the skill also contains "If you cannot start a separate context" followed by the fallback
