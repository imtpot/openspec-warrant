## ADDED Requirements

### Requirement: Archive after passing verification

The warrant archive guidance SHALL allow archiving only when every verification
task records `Result: exit 0`.

#### Scenario: Verification not run
- **WHEN** a verification task records `Result: not run, needs approval`
- **THEN** the guidance does not allow the archive

#### Scenario: Verification failed
- **WHEN** a verification task records `Result: exit 1, 1 failed`
- **THEN** the guidance does not allow the archive

#### Scenario: Rendered archive guidance
- **WHEN** `openspec instructions archive --json` runs for a change after setup
- **THEN** its `operationGuidance` requires `Result: exit 0` on every verification task
