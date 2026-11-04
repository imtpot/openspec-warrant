import shutil
import subprocess
from pathlib import Path

import pytest

from warrant_evals.checks import CHECKERS

RULES = (Path(__file__).resolve().parents[2] / 'skills' / 'warrant-setup' / 'rules.yaml').read_text()
pytestmark = pytest.mark.skipif(shutil.which('openspec') is None, reason='openspec CLI not on PATH')

CONFIG = 'schema: spec-driven\n\n# keep this comment\nrules:\n  tasks:\n  - Own project rule\n'
CONTRACT = """## Warrant contract

### Verification

- tests: `make test`

### Destructive actions

### Glossary

none

### Decision records

none
"""


def _git(workspace, *args):
    subprocess.run(['git', *args], cwd=workspace, check=True, capture_output=True)


@pytest.fixture
def workspace(tmp_path):
    (tmp_path / 'openspec').mkdir()
    (tmp_path / 'openspec' / 'config.yaml').write_text(CONFIG)
    (tmp_path / 'AGENTS.md').write_text('# Demo\n')
    _git(tmp_path, 'init', '-q')
    _git(tmp_path, 'add', '-A')
    _git(tmp_path, '-c', 'user.name=t', '-c', 'user.email=t@invalid', 'commit', '-q', '-m', 'fixture')
    return tmp_path


def _merged(rules=RULES):
    """The project config with warrant's entries merged into its own tasks list."""
    body = rules.split('rules:\n', 1)[1]
    return CONFIG.replace('  tasks:\n  - Own project rule\n', '') + body.replace(
        '  tasks:\n', '  tasks:\n  - Own project rule\n', 1
    )


def _install(workspace, agents_md='# Demo\n\n' + CONTRACT, config=None):
    (workspace / 'openspec' / 'config.yaml').write_text(config or _merged())
    (workspace / 'AGENTS.md').write_text(agents_md)


def _check(params, workspace, transcript=''):
    return [f.message for f in CHECKERS['setup'](params)(workspace, transcript)]


def test_installed_setup_passes(workspace):
    _install(workspace)

    assert _check({'expect': 'installed', 'verification': ['make test']}, workspace) == []


def test_outdated_warrant_rule_fails(workspace):
    _install(workspace, config=_merged(RULES.replace('[warrant] Use WHERE only', '[warrant] Use WHERE mostly')))

    assert _check({'expect': 'installed'}, workspace) == ['specs: warrant entries differ from rules.yaml']


def test_changed_project_rule_fails(workspace):
    _install(workspace, config=_merged().replace('Own project rule', 'Changed rule'))

    assert _check({'expect': 'installed'}, workspace) == ['tasks: project entries changed']


def test_changed_schema_fails(workspace):
    _install(workspace, config=_merged().replace('schema: spec-driven', 'schema: other'))

    assert 'schema field changed' in _check({'expect': 'installed'}, workspace)


def test_missing_verification_command_fails(workspace):
    _install(workspace, '# Demo\n\n' + CONTRACT.replace('- tests: `make test`\n', ''))

    assert _check({'expect': 'installed', 'verification': ['make test']}, workspace) == [
        'verification command not in contract: make test'
    ]


def test_contract_only_agents_md(workspace):
    _install(workspace, CONTRACT)

    assert _check({'expect': 'installed', 'contract_only': True}, workspace) == []
    _install_text = '# Demo\n\n' + CONTRACT
    (workspace / 'AGENTS.md').write_text(_install_text)
    assert _check({'expect': 'installed', 'contract_only': True}, workspace) == [
        'AGENTS.md holds more than the contract section'
    ]


def test_unchanged_agents_md(workspace):
    _install(workspace, '# Demo\n')

    assert _check({'expect': 'installed', 'agents_md_unchanged': True, 'contract': False}, workspace) == []


def test_nothing_written(workspace):
    assert _check({'expect': 'nothing', 'transcript': ['openspec init']}, workspace, 'Run openspec init first.') == []
    (workspace / 'new.txt').write_text('x')
    assert _check({'expect': 'nothing'}, workspace) == ['files changed: ?? new.txt']


def test_transcript_phrase_missing(workspace):
    assert _check({'expect': 'nothing', 'transcript': ['1.15.0']}, workspace, 'done') == [
        'transcript lacks: 1.15.0'
    ]


def test_expected_standards_path_present(workspace):
    _install(workspace, '# Demo\n\n' + CONTRACT + '\n### Standards\n\n- `CONTRIBUTING.md`\n')

    assert _check({'expect': 'installed', 'standards': ['CONTRIBUTING.md']}, workspace) == []


def test_expected_standards_path_missing(workspace):
    _install(workspace)

    assert _check({'expect': 'installed', 'standards': ['CONTRIBUTING.md']}, workspace) == [
        'standards file not in contract: CONTRIBUTING.md'
    ]
