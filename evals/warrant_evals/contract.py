"""Parse the `## Warrant contract` section of a project's AGENTS.md."""

import re
from dataclasses import dataclass

SECTION = 'Warrant contract'
SUBSECTIONS = ['Verification', 'Destructive actions', 'Glossary', 'Decision records']
VERIFICATION_BULLET = re.compile(r'^- ([^:]+): `([^`]+)`$')
COMMAND_BULLET = re.compile(r'^- `([^`]+)`$')


class ContractError(ValueError):
    pass


@dataclass
class Contract:
    verification: list[tuple[str, str]]
    destructive: list[str]
    glossary: str | None
    decision_records: str | None


def _section_body(text: str) -> str | None:
    match = re.search(rf'^## {SECTION}\s*$(.*?)(?=^## |\Z)', text, re.M | re.S)
    return match.group(1) if match else None


def _subsections(body: str) -> dict[str, list[str]]:
    parts = re.split(r'^### (.+?)\s*$', body, flags=re.M)
    names = [name.strip() for name in parts[1::2]]
    for name in SUBSECTIONS:
        if name not in names:
            raise ContractError(f'missing subsection: {name}')
    if [name for name in names if name in SUBSECTIONS] != SUBSECTIONS:
        raise ContractError(f'subsections out of order: {names}')
    return {
        name: [line.strip() for line in content.splitlines() if line.strip()]
        for name, content in zip(names, parts[2::2], strict=True)
    }


def _verification(lines: list[str]) -> list[tuple[str, str]]:
    entries = []
    for line in lines:
        match = VERIFICATION_BULLET.match(line)
        if not match:
            raise ContractError(f'verification entry needs `- name: `command``: {line}')
        entries.append((match.group(1).strip(), match.group(2)))
    return entries


def _location(lines: list[str]) -> str | None:
    value = lines[0] if lines else 'none'
    return None if value == 'none' else value


def parse_contract(text: str) -> Contract | None:
    """Return the contract, or None when AGENTS.md has no contract section."""
    body = _section_body(text)
    if body is None:
        return None
    parts = _subsections(body)
    return Contract(
        verification=_verification(parts['Verification']),
        destructive=[
            m.group(1) for line in parts['Destructive actions']
            if (m := COMMAND_BULLET.match(line))
        ],
        glossary=_location(parts['Glossary']),
        decision_records=_location(parts['Decision records']),
    )
