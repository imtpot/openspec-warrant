## MODIFIED Requirements

### Requirement: Untraced line

WHILE the review is tied to an OpenSpec change, the review skill SHALL report
each added line that serves no requirement of that change, no item of the
Protected code list and no rule of a declared Standards file as a blocking Spec
finding with its file and line.

#### Scenario: Unrequested option
- **WHEN** the diff adds a command-line option that no requirement names
- **THEN** the Spec section lists the option's file and line as untraced

#### Scenario: Protected input check
- **WHEN** the diff adds a check that rejects negative command-line input and no requirement names it
- **THEN** the Spec section does not list that check as untraced
