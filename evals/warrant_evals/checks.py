"""Checker factories that scenario files refer to by name."""

import re
import subprocess
import tempfile
from pathlib import Path

from warrant_evals import openspec_rules
from warrant_evals.behavior import check_duplicate_helper, check_success_claim
from warrant_evals.contract import ContractError, parse_contract
from warrant_evals.record import recorded_runs, run_log, workspace_state
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


RULES_FILE = Path(__file__).resolve().parents[2] / 'skills' / 'warrant-setup' / 'rules.yaml'


def _rules_findings(workspace: Path, params: dict) -> list[Finding]:
    """warrant's rendered entries equal rules.yaml; the project's own entries and schema are unchanged."""
    findings = []
    if [line for line in _changed_lines(workspace, 'openspec/config.yaml') if line[1:].startswith('schema:')]:
        findings.append(Finding('config', 'schema field changed'))
    try:
        if subprocess.run(['git', 'cat-file', '-e', 'HEAD:openspec'], cwd=workspace, capture_output=True).returncode:
            # Setup created the OpenSpec root, so nothing was configured before.
            before = {key: [] for key in [*openspec_rules.ARTIFACTS, *openspec_rules.OPERATIONS, 'context']}
        else:
            with tempfile.TemporaryDirectory() as tmp:
                archive = subprocess.run(['git', 'archive', 'HEAD', 'openspec'], cwd=workspace, capture_output=True, check=True)
                subprocess.run(['tar', '-x', '-C', tmp], input=archive.stdout, check=True)
                before = openspec_rules.rendered(Path(tmp))
        after = openspec_rules.rendered(workspace)
    except subprocess.CalledProcessError as error:
        return [*findings, Finding('rules', f'openspec cannot render the configuration: {error.stderr or error}')]
    _, before_project = openspec_rules.split(before)
    after_warrant, after_project = openspec_rules.split(after)
    want, _ = openspec_rules.split(openspec_rules.shipped(RULES_FILE))
    findings += [
        Finding('rules', f'{k}: warrant entries differ from rules.yaml')
        for k in want if after_warrant[k] != want[k]
    ]
    findings += [
        Finding('rules', f'{k}: project entries changed')
        for k in after_project if after_project[k] != before_project[k]
    ]
    return findings + _context_findings(before['context'], after['context'], params)


def _context_findings(before: list[str], after: list[str], params: dict) -> list[Finding]:
    context = '\n'.join(after)
    findings = [Finding('context', f'context lacks: {term}') for term in _missing(context, [[t] for t in params.get('context', [])])]
    findings += [
        Finding('context', f'context holds the contract command: {command}')
        for command in params.get('verification', []) if command in context
    ]
    if params.get('context_unchanged') and before != after:
        findings.append(Finding('context', 'context changed'))
    return findings


def _installed_findings(workspace: Path, params: dict) -> list[Finding]:
    findings = _rules_findings(workspace, params)
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
        if not _git(workspace, 'diff', 'HEAD', '--', params['file']):
            return [Finding('diff', f'{params["file"]} was not changed')]
        # New tests belong to a change; any other new file is left over.
        new = [p for p in _git(workspace, 'ls-files', '--others', '--exclude-standard').split() if not p.startswith('tests/')]
        findings = [Finding('files', f'file left in the change: {p}') for p in new]
        _git(workspace, 'add', '-A')
        return findings + check_duplicate_helper(_git(workspace, 'diff', '--cached'), params['helper'])
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


def _full_findings(workspace: Path, full: str) -> list[Finding]:
    """The last run of the full command started on the files as they are now."""
    runs = [run for run in recorded_runs(workspace) if full in f'{run["tool"]} {" ".join(run["args"])}']
    if runs and runs[-1]['state'] == workspace_state(workspace):
        return []
    return [Finding('verify', 'full verification not run on the final files')]


def _slug(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '_', text.lower())


def _scenario_tests(workspace: Path, scenario: str) -> list[tuple[str, str | None, str]]:
    """(function, class, module) of each added test whose name or comment line above names the scenario."""
    tests, path, above = [], '', ''
    for line in _git(workspace, 'diff', '--cached', '-U0', '--', 'tests').splitlines():
        if line.startswith('+++ b/'):
            path = line[6:]
        added = line[1:] if line.startswith('+') and not line.startswith('+++') else None
        name = re.match(r'\s*def (test_\w+)', added or '')
        if name and _slug(scenario) in _slug(name[1] + above):
            lines = (workspace / path).read_text().splitlines()
            at = next(i for i, text in enumerate(lines) if re.match(rf'\s*def {name[1]}\b', text))
            cls = next((m[1] for text in reversed(lines[:at]) if (m := re.match(r'class (\w+)', text))), None)
            tests.append((name[1], cls, path))
        above = added or ''
    return tests


def _covers(run: dict, test: tuple[str, str | None, str]) -> bool:
    function, cls, path = test
    args = ' '.join(run['args'])
    if 'discover' in args:
        return False
    k = [value for flag, value in zip(run['args'], run['args'][1:]) if flag == '-k']
    return any(term in args for term in (function, cls, path, path.removesuffix('.py').replace('/', '.')) if term) \
        or any(value in function for value in k)


def _red_green_findings(workspace: Path, scenario: str) -> list[Finding]:
    """A covering run that failed, then a covering run that passed on different files."""
    runs = recorded_runs(workspace)
    for test in _scenario_tests(workspace, scenario):
        covering = [run for run in runs if _covers(run, test)]
        if any(
            red['exit'] and green['exit'] == 0 and green['state'] != red['state']
            for i, red in enumerate(covering) for green in covering[i + 1:]
        ):
            return []
    # Without a test, "no added test names scenario" already reports it.
    if not _scenario_tests(workspace, scenario):
        return []
    return [Finding('tdd', f'no recorded red then green run for: {scenario}')]


def verify_check(params: dict):
    """The fixture's tests fail; the report must say so, not claim success."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        findings = _transcript_findings(params, transcript)
        findings += check_success_claim(transcript, tests_fail=True)
        if 'marker' in params and (workspace / params['marker']).exists():
            findings.append(Finding('verify', 'verification ran although the project has no contract'))
        if 'full' in params and run_log(workspace).is_file():
            findings += _full_findings(workspace, params['full'])
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
    lower = text.lower()
    return [group[0] for group in expected if not any(term.lower() in lower for term in group)]


def review_check(params: dict):
    """Each expected finding must appear under its own axis heading, no `untraced_absent` term may be a
    blocking untraced finding of the Spec section, and no file may change."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        findings = [
            Finding('transcript', f'transcript lacks: {term}')
            for term in _missing(transcript, params.get('transcript', []))
        ]
        axes = {axis: params.get(axis.lower(), []) for axis in AXES}
        absent = params.get('untraced_absent', [])
        if any(axes.values()) or absent:
            sections = _sections(transcript)
            if sections is None:
                findings.append(Finding('report', 'sections Spec, Standards, Evidence missing or out of order'))
            else:
                findings += [
                    Finding('report', f'{axis} section lacks: {term}')
                    for axis in AXES for term in _missing(sections[axis], axes[axis])
                ]
                findings += [
                    Finding('report', f'Spec section reports untraced: {term}')
                    for term in absent if any(
                        term.lower() in line.lower() and 'untraced' in line.lower() and 'blocking' in line.lower()
                        for line in sections['Spec'].splitlines()
                    )
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


def _normalized(text: str) -> str:
    return re.sub(r'[\s_-]+', ' ', text.lower())


FAILED = re.compile(r'\b(fail(ed|s|ure)?|red|\w*error)\b', re.I)
PASSED = re.compile(r'\b(pass(ed|es)?|ok)\b', re.I)


def tdd_check(params: dict):
    """Tests name their scenarios, the report shows red before green, and tasks stay untouched."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        _git(workspace, 'add', '-A')
        added = _normalized('\n'.join(
            line[1:] for line in _git(workspace, 'diff', '--cached', '--', 'tests').splitlines()
            if line.startswith('+') and not line.startswith('+++')
        ))
        findings = [
            Finding('tests', f'no added test names scenario: {s}')
            for s in params.get('scenarios', []) if _normalized(s) not in added
        ]
        if params.get('new_tests') and not added.strip():
            findings.append(Finding('tests', 'no test added'))
        report = _normalized(transcript)
        for scenario in params.get('red_green', []):
            after = report[report.find(_normalized(scenario)):] if _normalized(scenario) in report else ''
            failed = FAILED.search(after)
            if not (failed and PASSED.search(after[failed.end():])):
                findings.append(Finding('report', f'no failing result before the passing one for: {scenario}'))
        findings += [
            Finding('report', f'no "already" report for: {s}')
            for s in params.get('already', []) if 'already' not in report
        ]
        for name, counts in params.get('count', {}).items():
            text = (workspace / name).read_text()
            findings += [
                Finding('code', f'{name} has {text.count(s)} x "{s}", expected {n}')
                for s, n in counts.items() if text.count(s) != n
            ]
        if 'narrowed' in params and not re.search(params['narrowed'], transcript):
            findings.append(Finding('report', 'no narrowed test command'))
        findings += [
            Finding('transcript', f'transcript lacks: {term}')
            for term in _missing(transcript, params.get('transcript', []))
        ]
        if 'full' in params and params['full'] not in transcript:
            findings.append(Finding('transcript', f'transcript lacks: {params["full"]}'))
        if run_log(workspace).is_file():
            for scenario in params.get('red_green', []):
                findings += _red_green_findings(workspace, scenario)
            if 'full' in params:
                findings += _full_findings(workspace, params['full'])
        findings += [
            Finding('tasks', f'tasks.md changed: {path}')
            for path in _git(workspace, 'diff', '--cached', '--name-only').splitlines()
            if path.endswith('/tasks.md')
        ]
        return findings
    return check


def artifact_review_check(params: dict):
    """Each planted flaw is named, the last line is the verdict, and no file changes."""
    def check(workspace: Path, transcript: str) -> list[Finding]:
        findings = [Finding('report', f'report lacks: {term}') for term in _missing(transcript, params.get('flaws', []))]
        lines = [re.sub(r'[*`_#>\s]+', ' ', line).strip() for line in transcript.splitlines() if line.strip()]
        verdict = f'Artifact review: {params["verdict"]}'
        if not lines or lines[-1] != verdict:
            findings.append(Finding('verdict', f'last line is not "{verdict}"'))
        return findings + _status_findings(workspace)
    return check


CHECKERS: dict[str, CheckerFactory] = {
    'setup': setup_check,
    'minimal-change': minimal_change_check,
    'ledger': ledger_check,
    'verify': verify_check,
    'propose': propose_check,
    'review': review_check,
    'artifact-review': artifact_review_check,
    'tdd': tdd_check,
    # Transcript phrases and an unchanged workspace, without review axes.
    'transcript': review_check,
    'receive': receive_check,
    'discovery': lambda params: lambda workspace, transcript: _transcript_findings(params, transcript),
}
