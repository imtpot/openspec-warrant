# Spec Delta

## ADDED Requirements

### Requirement: No leftover files

The minimal-change skill SHALL direct the agent to delete every temporary,
backup or scratch file it created before it reports the change as complete.

#### Scenario: Edited copy
- **WHEN** the agent wrote `app/report.py.new` while editing `app/report.py`
- **THEN** `app/report.py.new` no longer exists when the change is reported
