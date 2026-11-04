# Spec Delta

## ADDED Requirements

### Requirement: Spec axis from openspec-verify-change

WHILE the review is tied to an OpenSpec change, the review skill SHALL report in
the Spec section the findings of the `openspec-verify-change` workflow for that
change, with their own severities.

#### Scenario: Unimplemented requirement
- **WHEN** verify-change reports a requirement as not found
- **THEN** the Spec section lists it with verify-change's severity

### Requirement: Verify-change not installed

IF the `openspec-verify-change` skill is not installed, THEN the review skill
SHALL report the Spec axis as not run and name the command that installs the
OpenSpec workflow skills.

#### Scenario: Missing OpenSpec skills
- **WHEN** `.agents/skills/openspec-verify-change/` and `~/.agents/skills/openspec-verify-change/` do not exist
- **THEN** the Spec section reads not run and names the `skills add` command

### Requirement: Connected code

The review skill SHALL report a bug or a security problem in code that calls or
is called by a changed function as a blocking Standards finding.

#### Scenario: Swapped arguments at a call site
- **WHEN** the diff adds a call that passes the arguments of `check(free, needed)` in the wrong order
- **THEN** the Standards section lists the call as blocking

### Requirement: Axes in separate contexts

The review skill SHALL run the Spec axis and the Standards axis each in a
separate, fresh context, or one after another without reusing conclusions
when no separate context is available.

#### Scenario: Agent without separate contexts
- **WHEN** the agent cannot start a separate context
- **THEN** the skill runs the axes one after another and reports each axis's findings on their own

## REMOVED Requirements

### Requirement: Missing requirement
**Reason**: `openspec-verify-change` reports requirements that are not implemented.
**Migration**: "Spec axis from openspec-verify-change".

### Requirement: Untested requirement
**Reason**: `openspec-verify-change` reports scenarios that no test covers.
**Migration**: "Spec axis from openspec-verify-change".
