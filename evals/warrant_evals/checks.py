"""Checker factories that scenario files refer to by name."""

import re
import subprocess
from pathlib import Path

from warrant_evals.behavior import check_duplicate_helper, check_success_claim
from warrant_evals.contract import ContractError, parse_contract
from warrant_evals.requirements import Finding, check_proposal, check_spec
from warrant_evals.scenarios import CheckerFactory


def _git(workspace: Path, *args: str) -> str:
    return subprocess.run(['git', *args], cwd=workspace, capture_output=True, text=True).stdout


def _changed_lines(workspace: Path, path: str) -> list[str]:
    diff = _git(workspace, 'diff', '-U0', '--', path)
    return [
        line for line in diff.splitlines()
        if line[:1] in '+-' and not line.startswith(('+++', '---'))
    ]


def _transcript_findings(params: dict, transcript: str) -> list[Finding]:
    return [
        Finding('transcript', f'transcript lacks: {phrase}')
        for phrase in params.get('transcript', []) if phrase not in transcript
    ]


def _installed_findings(workspace: Path, params: dict) -> list[Finding]:
    findings = []
    if not (workspace / 'openspec' / 'schemas' / 'warrant' / 'schema.yaml').is_file():
        findings.append(Finding('schema', 'openspec/schemas/warrant/schema.yaml missing'))
    config = _changed_lines(workspace, 'openspec/config.yaml')
    if any(not line[1:].startswith('schema:') for line in config):
        findings.append(Finding('config', 'openspec/config.yaml changed beyond the schema field'))
    if '+schema: warrant' not in config:
        findings.append(Finding('config', 'schema: warrant not set'))
    agents_md = workspace / 'AGENTS.md'
    if params.get('agents_md_unchanged') and _changed_lines(workspace, 'AGENTS.md'):
        findings.append(Finding('contract', 'AGENTS.md changed'))
    if not params.get('contract', True):
        return findings
    text = agents_md.read_text() if agents_md.is_file() else ''
    try:
        contract = parse_contract(text)
    except ContractError as error:
        return [*findings, Finding('contract', str(error))]
    if contract is None:
        return [*findings, Finding('contract', 'no Warrant contract section in AGENTS.md')]
    commands = [command for _, command in contract.verification]
    findings += [
        Finding('contract', f'verification command not in contract: {command}')
        for command in params.get('verification', []) if command not in commands
    ]
    findings += [
        Finding('contract', f'standards file not in contract: {path}')
        for path in params.get('standards', []) if path not in contract.standards
    ]
    if params.get('contract_only') and not text.lstrip().startswith('## Warrant contract'):
        findings.append(Finding('contract', 'AGENTS.md holds more than the contract section'))
    return findings


def setup_check(params: dict):
    def check(workspace: Path, transcript: str) -> list[Finding]:
        findings = _transcript_findings(params, transcript)
        if params['expect'] == 'nothing':
            return findings + _status_findings(workspace)
        return findings + _installed_findings(workspace, params)
    return check


def _status_findings(workspace: Path) -> list[Finding]:
    status = _git(workspace, 'status', '--porcelain').strip()
    return [Finding('workspace', f'files changed: {status}')] if status else []


def minimal_change_check(params: dict):
    def check(workspace: Path, transcript: str) -> list[Finding]:
        if not _git(workspace, 'diff', '--', params['file']):
            return [Finding('diff', f'{params["file"]} was not changed')]
        _git(workspace, 'add', '-A')
        return check_duplicate_helper(_git(workspace, 'diff', '--cached'), params['helper'])
    return check


def ledger_check(params: dict):
    def check(workspace: Path, transcript: str) -> list[Finding]:
        lines = transcript.splitlines()
        findings = []
        for entry in params['entries']:
            matching = [line for line in lines if entry in line]
            if not matching:
                findings.append(Finding('ledger', f'ledger lacks {entry}'))
            elif entry in params['no_trigger'] and not any('no-trigger' in line for line in matching):
                findings.append(Finding('ledger', f'{entry} not tagged no-trigger'))
        if f'{params["total"]} shortcuts' not in transcript:
            findings.append(Finding('ledger', f'ledger total is not {params["total"]}'))
        return findings + _status_findings(workspace)
    return check


def verify_check(params: dict):
    """The fixture's tests fail; the report must say so, not claim success."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        findings = _transcript_findings(params, transcript)
        findings += check_success_claim(transcript, tests_fail=True)
        if 'marker' in params and (workspace / params['marker']).exists():
            findings.append(Finding('verify', 'verification ran although the project has no contract'))
        return findings
    return check


def propose_check(params: dict):
    def check(workspace: Path, transcript: str) -> list[Finding]:
        change = workspace / 'openspec' / 'changes' / params['change']
        proposal = change / 'proposal.md'
        if not proposal.is_file():
            return [Finding('propose', f'{proposal.relative_to(workspace)} missing')]
        findings = check_proposal(proposal.read_text())
        specs = sorted((change / 'specs').glob('**/*.md'))
        if not specs:
            findings.append(Finding('propose', 'no spec files'))
        for spec in specs:
            findings += check_spec(spec.read_text())
        return findings
    return check


AXES = ['Spec', 'Standards', 'Evidence']


def _sections(transcript: str) -> dict[str, str] | None:
    """Text under each axis heading, or None when a heading is missing or out of order."""
    marks = [re.search(rf'^#+ {axis}\b.*$', transcript, re.M) for axis in AXES]
    if not all(marks) or [m.start() for m in marks] != sorted(m.start() for m in marks):
        return None
    ends = [m.start() for m in marks[1:]] + [len(transcript)]
    return {axis: transcript[m.end():end] for axis, m, end in zip(AXES, marks, ends, strict=True)}


def _missing(text: str, expected: list[list[str]]) -> list[str]:
    """First term of each alternative group that has no term in the text."""
    return [group[0] for group in expected if not any(term in text for term in group)]


def review_check(params: dict):
    """Each expected finding must appear under its own axis heading; no file may change."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        findings = [
            Finding('transcript', f'transcript lacks: {term}')
            for term in _missing(transcript, params.get('transcript', []))
        ]
        axes = {axis: params.get(axis.lower(), []) for axis in AXES}
        if any(axes.values()):
            sections = _sections(transcript)
            if sections is None:
                findings.append(Finding('report', 'sections Spec, Standards, Evidence missing or out of order'))
            else:
                findings += [
                    Finding('report', f'{axis} section lacks: {term}')
                    for axis in AXES for term in _missing(sections[axis], axes[axis])
                ]
        return findings + _status_findings(workspace)
    return check


def receive_check(params: dict):
    """Accepted comments applied, rejected ones not, and the report shows verification."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        name = params['file']
        text = (workspace / name).read_text()
        findings = [Finding('code', f'{name} lacks: {s}') for s in params.get('present', []) if s not in text]
        findings += [
            Finding('code', f'{name} changed: "{s.splitlines()[0]}"')
            for s in params.get('unchanged', []) if s not in text
        ]
        findings += [
            Finding('code', f'{name} has {text.count(s)} x "{s}", expected {n}')
            for s, n in params.get('count', {}).items() if text.count(s) != n
        ]
        findings += [
            Finding('transcript', f'transcript lacks: {term}')
            for term in _missing(transcript, params.get('transcript', []))
        ]
        return findings
    return check


CHECKERS: dict[str, CheckerFactory] = {
    'setup': setup_check,
    'minimal-change': minimal_change_check,
    'ledger': ledger_check,
    'verify': verify_check,
    'propose': propose_check,
    'review': review_check,
    'receive': receive_check,
    'discovery': lambda params: lambda workspace, transcript: _transcript_findings(params, transcript),
}
