import subprocess

import pytest

from warrant_evals.checks import CHECKERS

CONFIG = 'schema: spec-driven\n\n# keep this comment\n'
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


def _install(workspace, agents_md='# Demo\n\n' + CONTRACT):
    (workspace / 'openspec' / 'schemas' / 'warrant').mkdir(parents=True)
    (workspace / 'openspec' / 'schemas' / 'warrant' / 'schema.yaml').write_text('name: warrant\n')
    (workspace / 'openspec' / 'config.yaml').write_text(CONFIG.replace('spec-driven', 'warrant'))
    (workspace / 'AGENTS.md').write_text(agents_md)


def _check(params, workspace, transcript=''):
    return [f.message for f in CHECKERS['setup'](params)(workspace, transcript)]


def test_installed_setup_passes(workspace):
    _install(workspace)

    assert _check({'expect': 'installed', 'verification': ['make test']}, workspace) == []


def test_config_change_beyond_schema_fails(workspace):
    _install(workspace)
    (workspace / 'openspec' / 'config.yaml').write_text('schema: warrant\n')

    assert _check({'expect': 'installed'}, workspace) == ['openspec/config.yaml changed beyond the schema field']


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
