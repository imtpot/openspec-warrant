"""This repository uses its own schema and skills; the copies must match the sources."""

import filecmp
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKILLS = ['warrant-setup', 'warrant-minimal-change', 'warrant-verify', 'warrant-review', 'warrant-design']


def _differences(source: Path, copy: Path) -> list[str]:
    files = [str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()]
    _, mismatch, errors = filecmp.cmpfiles(source, copy, files, shallow=False)
    return mismatch + errors


def test_project_schema_matches_the_shipped_schema():
    assert _differences(
        REPO / 'skills' / 'warrant-setup' / 'schema' / 'warrant',
        REPO / 'openspec' / 'schemas' / 'warrant',
    ) == []


@pytest.mark.parametrize('name', SKILLS)
def test_installed_skill_matches_its_source(name):
    installed = REPO / '.agents' / 'skills' / name
    if not installed.exists():
        pytest.skip('warrant skills are not installed; see AGENTS.md')
    assert _differences(REPO / 'skills' / name, REPO / '.agents' / 'skills' / name) == []
