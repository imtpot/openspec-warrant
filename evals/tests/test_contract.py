import pytest

from warrant_evals.contract import ContractError, parse_contract

CONTRACT = """# Project

Intro text.

## Warrant contract

### Verification

- tests: `uv run pytest`
- lint: `uv run ruff check .`

### Destructive actions

- `pulumi up`
- `kubectl delete`

### Glossary

docs/glossary.md

### Decision records

none

## Other section

- not: `part of the contract`
"""


def test_reads_verification_commands_in_order():
    contract = parse_contract(CONTRACT)

    assert contract.verification == [
        ('tests', 'uv run pytest'),
        ('lint', 'uv run ruff check .'),
    ]


def test_reads_destructive_actions():
    assert parse_contract(CONTRACT).destructive == ['pulumi up', 'kubectl delete']


def test_reads_locations_and_none():
    contract = parse_contract(CONTRACT)

    assert contract.glossary == 'docs/glossary.md'
    assert contract.decision_records is None


def test_missing_section_returns_none():
    assert parse_contract('# Project\n\n## Build\n\n- `make`\n') is None


def test_empty_verification_list():
    text = CONTRACT.replace(
        '- tests: `uv run pytest`\n- lint: `uv run ruff check .`\n', ''
    )

    assert parse_contract(text).verification == []


def test_subsections_out_of_order_are_rejected():
    text = CONTRACT.replace('### Glossary', '### Tmp').replace(
        '### Destructive actions', '### Glossary'
    ).replace('### Tmp', '### Destructive actions')

    with pytest.raises(ContractError, match='order'):
        parse_contract(text)


def test_missing_subsection_is_rejected():
    text = CONTRACT.replace('### Decision records\n\nnone\n', '')

    with pytest.raises(ContractError, match='Decision records'):
        parse_contract(text)


def test_verification_bullet_without_backticked_command_is_rejected():
    text = CONTRACT.replace('- tests: `uv run pytest`', '- tests: uv run pytest')

    with pytest.raises(ContractError, match='tests'):
        parse_contract(text)


STANDARDS = CONTRACT.replace(
    '### Decision records\n\nnone\n',
    '### Decision records\n\nnone\n\n### Standards\n\n- `docs/standards.md`\n- `CONTRIBUTING.md`\n',
)


def test_reads_standards_paths():
    assert parse_contract(STANDARDS).standards == ['docs/standards.md', 'CONTRIBUTING.md']


def test_standards_none_is_empty():
    text = STANDARDS.replace('- `docs/standards.md`\n- `CONTRIBUTING.md`\n', 'none\n')

    assert parse_contract(text).standards == []


def test_contract_without_standards_has_no_standards():
    assert parse_contract(CONTRACT).standards == []


def test_standards_before_decision_records_is_rejected():
    text = CONTRACT.replace('### Decision records', '### Standards\n\nnone\n\n### Decision records')

    with pytest.raises(ContractError, match='order'):
        parse_contract(text)
