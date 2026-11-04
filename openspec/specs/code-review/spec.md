# code-review Specification

## Purpose
Defines the `warrant-review` skill: reviewing a diff along separate Spec,
Standards and Evidence axes without changing files, and addressing review
comments by checking each one before acting on it.

## Requirements

### Requirement: Three axes in order

WHEN the user asks for a review, the review skill SHALL report its findings in
three sections, Spec, Standards and Evidence, in that order, without moving a
finding from one section to another.

#### Scenario: Review report
- **WHEN** the user asks to review the current branch
- **THEN** the report has the sections Spec, Standards and Evidence in that order

### Requirement: Review changes no file

WHILE the review skill runs in review mode, the review skill SHALL leave every
file in the repository unchanged.

#### Scenario: Findings without fixes
- **WHEN** the review finds an untraced line
- **THEN** `git status` shows the same state before and after the review

### Requirement: Default review range

WHEN the user names no base, the review skill SHALL review the commits since
the merge-base with the default branch of `origin` together with uncommitted
changes.

#### Scenario: Feature branch
- **WHEN** a feature branch has two commits and one uncommitted file
- **THEN** the review covers both commits and the uncommitted file

### Requirement: Named base

WHERE the user names a base commit or branch, the review skill SHALL review the
changes between that base and the working tree.

#### Scenario: Review since a tag
- **WHEN** the user asks to review since `v0.1.0`
- **THEN** the review covers the changes between `v0.1.0` and the working tree

### Requirement: Nothing to review

IF the review range contains no changes, THEN the review skill SHALL report
"nothing to review" and no findings.

#### Scenario: Clean branch
- **WHEN** the branch has no commits and no changes beyond its base
- **THEN** the report reads "nothing to review"

### Requirement: Untraced line

WHILE the review is tied to an OpenSpec change, the review skill SHALL report
each added line that serves no requirement of that change as a blocking Spec
finding with its file and line.

#### Scenario: Unrequested option
- **WHEN** the diff adds a command-line option that no requirement names
- **THEN** the Spec section lists the option's file and line as untraced

### Requirement: Change selection

The review skill SHALL tie the review to the OpenSpec change the user names,
or to the only active change when the user names none.

#### Scenario: One active change
- **WHEN** `openspec list` shows exactly one active change and the user names none
- **THEN** the Spec axis reviews against that change

### Requirement: Several active changes

IF more than one OpenSpec change is active and the user names none, THEN the
review skill SHALL ask the user which change the diff belongs to before the
Spec axis.

#### Scenario: Two active changes
- **WHEN** two changes are active and the user asks for a review
- **THEN** the skill asks which change to review against

### Requirement: No OpenSpec change

IF no OpenSpec change is active and the user names none, THEN the review skill
SHALL state "no OpenSpec change" in the Spec section and report no Spec findings.

#### Scenario: Direct change
- **WHEN** the project has no active change
- **THEN** the Spec section reads "no OpenSpec change"

### Requirement: Declared standards

The review skill SHALL report each part of the diff that violates a rule in a
file listed under the contract's Standards subsection as a blocking Standards
finding that quotes the rule and its file.

#### Scenario: Naming rule
- **WHEN** `docs/standards.md` requires snake_case functions and the diff adds `makeSlug`
- **THEN** the Standards section quotes the rule, its file and the line with `makeSlug`

### Requirement: Minimal-change smells

The review skill SHALL report speculative generality, unused options and new
dependencies without a stated reason as non-blocking Standards findings.

#### Scenario: Unused parameter
- **WHEN** the diff adds a parameter that no caller passes
- **THEN** the Standards section lists it as non-blocking

### Requirement: Removed protection

The review skill SHALL report removed validation at trust boundaries, removed
error handling that prevents data loss and removed security checks as blocking
Standards findings.

#### Scenario: Dropped input check
- **WHEN** the diff deletes a check of user input
- **THEN** the Standards section lists the deletion as blocking

### Requirement: No declared standards

WHILE the contract declares no standards, the review skill SHALL state "no
standards declared" in the Standards section and check the minimal-change
rules only.

#### Scenario: Standards none
- **WHEN** the Standards subsection reads `none` or is missing
- **THEN** the Standards section starts with "no standards declared"

### Requirement: Evidence by running verification

The review skill SHALL run each verification command of the contract following
the warrant-verify skill and report its command, exit code and result line in
the Evidence section.

#### Scenario: Passing tests
- **WHEN** the contract lists `make test` and it exits with code 0
- **THEN** the Evidence section shows `make test`, exit code 0 and the result line

### Requirement: Failed or missing evidence

IF a verification command fails or cannot run, THEN the review skill SHALL
report it as a blocking Evidence finding.

#### Scenario: Failing test
- **WHEN** `make test` exits with code 1
- **THEN** the Evidence section lists it as blocking with the failing test

### Requirement: Finding format

The review skill SHALL give each finding its level (blocking or non-blocking),
its location as file and line where one exists, and the quoted code,
requirement or rule it concerns.

#### Scenario: Untraced line finding
- **WHEN** the skill reports an untraced line
- **THEN** the finding reads blocking, names `file:line` and quotes the line

### Requirement: Classify comments first

WHEN the user asks to address review comments, the review skill SHALL classify
each comment as accepted or rejected, with a reason, before it changes any file.

#### Scenario: Three comments
- **WHEN** the user passes three review comments
- **THEN** the skill lists three classifications before the first edit

### Requirement: Reject comments that conflict with specs

IF a review comment asks for behavior that conflicts with a requirement of the
OpenSpec change, THEN the review skill SHALL reject the comment and quote the
requirement.

#### Scenario: Comment against a requirement
- **WHEN** a comment asks to exit with code 0 on failure and a requirement says code 2
- **THEN** the skill rejects the comment and quotes the code-2 requirement

### Requirement: Reject false claims

IF a review comment states a fact about the code that the code contradicts,
THEN the review skill SHALL reject the comment and show the code that
contradicts it.

#### Scenario: Claimed missing check
- **WHEN** a comment says a function lacks a null check and the check exists
- **THEN** the skill rejects the comment and quotes the existing check

### Requirement: Unclear comments

IF a review comment is unclear about what to change, THEN the review skill
SHALL ask the user and leave the related code unchanged.

#### Scenario: Vague comment
- **WHEN** a comment reads "this looks off"
- **THEN** the skill asks what to change and does not edit the code it refers to

### Requirement: Verify after addressing comments

WHEN the review skill has applied the accepted comments, the review skill SHALL
run the contract's verification following warrant-verify before it reports the
comments as addressed.

#### Scenario: Comments applied
- **WHEN** two accepted comments are applied
- **THEN** the report shows the verification commands with exit codes before
  stating that the comments are addressed

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

### Requirement: Artifact mode changes no file

WHILE the review skill reviews a change's artifacts, the review skill SHALL
leave every file unchanged.

#### Scenario: Flawed artifacts
- **WHEN** the artifact review finds flaws
- **THEN** `git status` is the same before and after

### Requirement: EARS findings

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report each requirement that does not use exactly one EARS pattern with one
`SHALL` as a blocking finding naming the requirement.

#### Scenario: Compound requirement
- **WHEN** a requirement reads "... SHALL raise an error and SHALL NOT print output"
- **THEN** the report names that requirement as blocking

### Requirement: Missing tasks

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a task list without a test task for a requirement, or without a
verification group, as a blocking finding.

#### Scenario: No verification group
- **WHEN** `tasks.md` has no verification tasks
- **THEN** the report names the missing verification group as blocking

### Requirement: Contradicted decision

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a design decision that contradicts a decision in `design.md` of an
archived change as a blocking finding quoting both.

#### Scenario: Output format already decided
- **WHEN** an archived change's design says machine output is JSON and the design chooses YAML
- **THEN** the report quotes both decisions and marks the conflict as blocking

### Requirement: Unlisted assumption

WHEN the review skill reviews a change's artifacts, the review skill SHALL
report a decision that the specs or design present as settled, and that the
proposal lists neither as confirmed nor under Assumptions, as a blocking finding.

#### Scenario: Unconfirmed output path
- **WHEN** the design fixes an output path that the proposal never mentions
- **THEN** the report names the decision as an unlisted assumption

### Requirement: Verdict line

WHEN the artifact review ends, the review skill SHALL end its report with the
line `Artifact review: REVISE` if any blocking finding exists and
`Artifact review: PASS` otherwise.

#### Scenario: Blocking finding
- **WHEN** the review reports one blocking finding
- **THEN** the last line of the report is `Artifact review: REVISE`

### Requirement: Axes in fresh contexts

The review skill SHALL run the Spec axis and the Standards axis each in a
separate, fresh context.

#### Scenario: Branch review
- **WHEN** a branch is reviewed
- **THEN** each axis runs in its own fresh context and the report keeps their findings apart

### Requirement: Artifact review in a sub-agent

The review skill SHALL review the artifacts in a separate, fresh context that
receives the artifact files and not the conversation that produced them.

#### Scenario: Artifacts written in this conversation
- **WHEN** the agent wrote the artifacts earlier in the conversation
- **THEN** a fresh context reviews them from the files on disk
