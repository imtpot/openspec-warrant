"""This repository uses its own schema and skills; the copies must match the sources."""

import filecmp
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKILLS = ['warrant-setup', 'warrant-minimal-change', 'warrant-verify', 'warrant-review', 'warrant-tdd']


def _differences(source: Path, copy: Path) -> list[str]:
    files = [str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()]
    _, mismatch, errors = filecmp.cmpfiles(source, copy, files, shallow=False)
    return mismatch + errors


def _warrant_lines(path: Path) -> list[str]:
    lines = [line.strip() for line in path.read_text().splitlines()]
    return [line for line in lines if '[warrant] ' in line and not line.startswith('#')]


@pytest.mark.parametrize('config', [
    'openspec/config.yaml', 'evals/fixtures/warrant-project/openspec/config.yaml',
])
def test_config_carries_the_shipped_rules(config):
    shipped = _warrant_lines(REPO / 'skills' / 'warrant-setup' / 'rules.yaml')

    assert _warrant_lines(REPO / config) == shipped


@pytest.mark.parametrize('name', SKILLS)
def test_installed_skill_matches_its_source(name):
    installed = REPO / '.agents' / 'skills' / name
    if not installed.exists():
        pytest.skip('warrant skills are not installed; see AGENTS.md')
    assert _differences(REPO / 'skills' / name, REPO / '.agents' / 'skills' / name) == []
