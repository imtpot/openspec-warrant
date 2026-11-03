from warrant_evals.requirements import check_proposal, check_spec

VALID = """# Spec Delta

## ADDED Requirements

### Requirement: Ubiquitous

The quota check SHALL print one line per cloud.

#### Scenario: One cloud
- **WHEN** one cloud is configured
- **THEN** one line is printed

### Requirement: Event

WHEN the quota check runs with `--json`, the quota check SHALL write one JSON object.

#### Scenario: JSON
- **WHEN** `--json` is passed
- **THEN** stdout parses as JSON

### Requirement: State

WHILE the project RAM limit is unlimited, the quota check SHALL report `null` for free RAM.

#### Scenario: Unlimited
- **WHEN** the limit is -1
- **THEN** free RAM is null

### Requirement: Unwanted

IF the flavor does not exist, THEN the quota check SHALL exit with code 2.

#### Scenario: Unknown flavor
- **WHEN** the flavor is missing
- **THEN** the exit code is 2

### Requirement: Option

WHERE the `--verbose` option is set, the quota check SHALL print the limits it read.

#### Scenario: Verbose
- **WHEN** `--verbose` is passed
- **THEN** the limits are printed
"""

# Recorded from a trial run of spec-driven on a real project.
COMPOUND = """## ADDED Requirements

### Requirement: Exit code reports the verdict

The quota check SHALL exit with code 0 when one more VM of the flavor fits the
free cores and RAM, code 1 when it does not fit, and code 2 when the verdict is
unknown. The exit code SHALL be the same with and without `--json`.

#### Scenario: Flavor fits
- **WHEN** the flavor fits
- **THEN** the quota check exits with code 0
"""

WHERE_STATE = """## ADDED Requirements

### Requirement: JSON report of an unlimited quota

WHERE the cloud's project has no limit for cores or RAM, the quota check SHALL
report `null` for that value in `free` when it runs with `--json`.

#### Scenario: Unlimited RAM
- **WHEN** the project's RAM limit is -1
- **THEN** `free` is `{"cores": 18, "ram_mb": null}`
"""

NO_KEYWORD = """## ADDED Requirements

### Requirement: Text output stays unchanged

Without `--json` the output SHALL stay the same.

#### Scenario: Text
- **WHEN** no flag is given
- **THEN** the output is unchanged
"""

IF_WITHOUT_THEN = """## ADDED Requirements

### Requirement: Failed check

IF the check cannot authenticate the quota check SHALL exit with code 2.

#### Scenario: Auth failure
- **WHEN** authentication fails
- **THEN** the exit code is 2
"""


def test_valid_patterns_have_no_findings():
    assert check_spec(VALID) == []


def test_two_shall_clauses_are_reported():
    findings = check_spec(COMPOUND)

    assert [f.requirement for f in findings] == ['Exit code reports the verdict']
    assert 'SHALL' in findings[0].message


def test_where_before_environment_state_is_reported():
    findings = check_spec(WHERE_STATE)

    assert [f.requirement for f in findings] == ['JSON report of an unlimited quota']
    assert 'WHILE' in findings[0].message


def test_missing_ears_keyword_is_reported():
    findings = check_spec(NO_KEYWORD)

    assert [f.requirement for f in findings] == ['Text output stays unchanged']
    assert 'EARS' in findings[0].message


def test_if_without_then_is_reported():
    findings = check_spec(IF_WITHOUT_THEN)

    assert [f.requirement for f in findings] == ['Failed check']
    assert 'THEN' in findings[0].message


def test_shall_inside_backticks_is_not_counted():
    text = VALID.replace(
        'The quota check SHALL print one line per cloud.',
        'The checker SHALL fail a requirement that contains more than one `SHALL`.',
    )

    assert check_spec(text) == []


def test_proposal_with_assumptions_section_passes():
    assert check_proposal('# Proposal\n\n## Why\n\nx\n\n## Assumptions\n\n- a\n') == []


def test_proposal_without_assumptions_section_is_reported():
    findings = check_proposal('# Proposal\n\n## Why\n\nx\n\n## Open questions\n\nNone.\n')

    assert len(findings) == 1
    assert 'Assumptions' in findings[0].message
