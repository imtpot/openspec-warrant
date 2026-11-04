"""Mechanical checks of the warrant-kit principles (openspec/specs/warrant-kit)."""

import re
import tomllib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKILLS = sorted(p.parent.name for p in (REPO / 'skills').glob('*/SKILL.md'))
AGENT_WORDS = [
    'Claude', 'Codex', 'Copilot', 'Cursor', 'Gemini', 'agy',
    'Skill tool', 'Task tool', 'TodoWrite', 'subagent',
]


def _skill(name: str) -> str:
    return (REPO / 'skills' / name / 'SKILL.md').read_text()


def _frontmatter(name: str) -> dict[str, str]:
    block = _skill(name).split('---')[1]
    return dict(line.split(': ', 1) for line in block.strip().splitlines() if ': ' in line)


@pytest.mark.parametrize('name', SKILLS)
def test_skill_is_agent_neutral(name):
    text = _skill(name)
    found = [w for w in AGENT_WORDS if re.search(rf'\b{re.escape(w)}', text, re.I)]

    assert found == [], f'{name} names {found}'


@pytest.mark.parametrize('name', SKILLS)
def test_skill_size(name):
    lines = _skill(name).count('\n')

    assert lines <= 150, f'{name} has {lines} lines'


@pytest.mark.parametrize('name', SKILLS)
def test_description_says_when_to_use(name):
    description = _frontmatter(name)['description']

    assert description.startswith(('Use when', 'Use before')), f'{name}: {description[:60]}'


@pytest.mark.parametrize('name', SKILLS)
def test_skill_license(name):
    assert _frontmatter(name).get('license') == 'MIT', name


@pytest.mark.parametrize('name', SKILLS)
def test_skill_has_an_eval_scenario(name):
    listed = [tomllib.loads(p.read_text()).get('skills', []) for p in (REPO / 'evals' / 'scenarios').glob('*.toml')]

    assert any(name in skills for skills in listed), f'no scenario lists {name} in skills'


@pytest.mark.parametrize('name', SKILLS)
def test_skill_is_in_the_design(name):
    assert name in (REPO / 'docs' / 'design.md').read_text(), f'{name} missing from docs/design.md'
