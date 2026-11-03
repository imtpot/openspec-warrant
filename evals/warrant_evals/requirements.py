"""Deterministic checks for requirements and proposals written under the warrant schema."""

import re
from dataclasses import dataclass

REQUIREMENT = re.compile(r'^### Requirement: (.+?)\s*$(.*?)(?=^#{2,4} |\Z)', re.M | re.S)
EARS_START = ('The ', 'WHEN ', 'WHILE ', 'IF ', 'WHERE ')
# shortcut: a fixed phrase list catches the common cases only, extend it when
# a missed environment state shows up in an eval report.
STATE_PHRASES = (
    ' has no ', ' have no ', ' is not ', ' are not ', ' is unavailable',
    ' is down', ' is empty', ' is full', ' exceeds ', ' is missing',
)


@dataclass
class Finding:
    requirement: str
    message: str


def _requirement_findings(name: str, text: str) -> list[Finding]:
    text = ' '.join(text.split())
    if not text.startswith(EARS_START):
        return [Finding(name, f'no EARS pattern at the start: {text[:60]!r}')]
    findings = []
    prose = re.sub(r'`[^`]*`', '', text)
    if (count := len(re.findall(r'\bSHALL\b', prose))) != 1:
        findings.append(Finding(name, f'{count} SHALL clauses; write one requirement per outcome'))
    if text.startswith('IF ') and ', THEN ' not in text:
        findings.append(Finding(name, 'IF clause without ", THEN"'))
    if text.startswith('WHERE '):
        clause = text.split(',', 1)[0]
        if any(phrase in f'{clause} ' for phrase in STATE_PHRASES):
            findings.append(Finding(name, f'WHERE used for an environment state, use WHILE: {clause!r}'))
    return findings


def _checked_text(text: str) -> str:
    """Drop REMOVED and RENAMED delta sections; their entries carry no requirement text."""
    return re.sub(r'^## (REMOVED|RENAMED) Requirements\s*$.*?(?=^## |\Z)', '', text, flags=re.M | re.S)


def check_spec(text: str) -> list[Finding]:
    findings = []
    for match in REQUIREMENT.finditer(_checked_text(text)):
        findings += _requirement_findings(match.group(1), match.group(2))
    return findings


def check_proposal(text: str) -> list[Finding]:
    if re.search(r'^#{2,3} Assumptions\b', text, re.M):
        return []
    return [Finding('proposal', 'no Assumptions section')]
