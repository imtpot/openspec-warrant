## MODIFIED Requirements

### Requirement: Missing tasks

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a requirement that no task names, or a task list without a verification
group, as a blocking finding.

#### Scenario: No verification group
- **WHEN** `tasks.md` has no verification tasks
- **THEN** the report names the missing verification group as blocking

#### Scenario: Requirement without a task
- **WHEN** no task in `tasks.md` names the requirement "Quota check"
- **THEN** the report names "Quota check" as a requirement that no task names, blocking

### Requirement: Change selection

The review skill SHALL tie a review, and the classification of review
comments, to the OpenSpec change the user names, or to the only active change
when the user names none.

#### Scenario: One active change
- **WHEN** `openspec list` shows exactly one active change and the user names none
- **THEN** the Spec axis reviews against that change

#### Scenario: Comments with one active change
- **WHEN** the user gives review comments and `openspec list` shows exactly one active change
- **THEN** the skill checks the comments against that change's requirements
