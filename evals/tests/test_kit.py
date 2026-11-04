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



RULES_FILE = REPO / 'skills' / 'warrant-setup' / 'rules.yaml'


def _rule_lines() -> list[str]:
    return [line.strip() for line in RULES_FILE.read_text().splitlines() if line.strip().startswith('- ')]


def test_rules_cover_every_artifact_and_operation():
    keys = re.findall(r'^ {2}(\w+):$', RULES_FILE.read_text(), re.M)

    assert sorted(keys) == ['apply', 'archive', 'design', 'proposal', 'specs', 'tasks']


def test_every_rule_entry_is_one_marked_line():
    assert [line for line in _rule_lines() if not line.startswith('- "[warrant] ')] == []


def test_rules_leave_openspec_spec_guidance_to_openspec():
    duplicated = [line for line in _rule_lines() if re.search(r'one SHALL|observable response', line)]

    assert duplicated == []
