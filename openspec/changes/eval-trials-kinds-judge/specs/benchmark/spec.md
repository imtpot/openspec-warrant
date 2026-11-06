## ADDED Requirements

### Requirement: Judged review problems

WHERE a planted problem of a review task has a description, IF no term of the
problem appears in the agent's report, THEN the benchmark SHALL count the
problem as named only when the judge answers `yes` for the report.

#### Scenario: Problem named in other words
- **WHEN** no term of a described problem appears in the report and the judge answers `yes`
- **THEN** the problem counts as named in the review task score

#### Scenario: Judge unsure
- **WHEN** no term of a described problem appears in the report and the judge answers `unknown`
- **THEN** the problem counts as missed and the run list marks it unknown
