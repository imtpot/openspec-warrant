# Spec Delta

## ADDED Requirements

### Requirement: Leftover file check

The minimal-change scenario's checker SHALL fail when the workspace holds a new
file that the task did not ask for.

#### Scenario: Backup copy left behind
- **WHEN** the agent leaves `app/report.py.new` next to the changed file
- **THEN** the checker fails and names `app/report.py.new`

## REMOVED Requirements

### Requirement: Scenario not applicable to an agent
**Reason**: No scenario uses it since Codex runs in a non-login shell.
**Migration**: None.

### Requirement: Design scenario checks
**Reason**: `warrant-design` is removed.
**Migration**: None.
