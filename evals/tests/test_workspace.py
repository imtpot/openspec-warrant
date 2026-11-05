import shutil
import subprocess
from pathlib import Path

import pytest

from warrant_evals.workspace import commit_fixture, prepare_workspace

pytestmark = pytest.mark.skipif(shutil.which('skills') is None, reason='skills CLI not on PATH')


def test_prepare_commits_the_fixture_and_installs_skills(tmp_path):
    source = tmp_path / 'source'
    (source / 'skills' / 'demo-skill').mkdir(parents=True)
    (source / 'skills' / 'demo-skill' / 'SKILL.md').write_text(
        '---\nname: demo-skill\ndescription: Demo skill for tests.\n---\nDemo.\n'
    )
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    (workspace / 'README.md').write_text('fixture\n')

    prepare_workspace(workspace, source)

    assert (workspace / '.agents' / 'skills' / 'demo-skill' / 'SKILL.md').is_file()
    assert (workspace / '.claude' / 'skills' / 'demo-skill').is_symlink()
    log = subprocess.run(['git', 'log', '--oneline'], cwd=workspace, capture_output=True, text=True)
    assert log.stdout.count('\n') == 1
    status = subprocess.run(['git', 'status', '--porcelain'], cwd=workspace, capture_output=True, text=True)
    assert status.stdout == ''


def test_prepare_installs_extra_skill_sources(tmp_path):
    sources = []
    for name in ('main-skill', 'extra-skill'):
        root = tmp_path / name
        (root / 'skills' / name).mkdir(parents=True)
        (root / 'skills' / name / 'SKILL.md').write_text(
            f'---\nname: {name}\ndescription: Use when testing {name}.\n---\nDemo.\n'
        )
        sources.append(root)
    workspace = tmp_path / 'workspace'
    workspace.mkdir()

    prepare_workspace(workspace, sources[0], extra=[sources[1] / 'skills'])

    assert (workspace / '.agents' / 'skills' / 'main-skill' / 'SKILL.md').is_file()
    assert (workspace / '.agents' / 'skills' / 'extra-skill' / 'SKILL.md').is_file()


@pytest.mark.parametrize(('setup', 'present'), [('setup-protected.sh', True), ('setup-feature.sh', False)])
def test_review_branch_protected_variant_adds_the_input_check(tmp_path, setup, present):
    fixture = tmp_path / 'review-branch'
    shutil.copytree(Path(__file__).parent.parent / 'fixtures' / 'review-branch', fixture)
    commit_fixture(fixture)

    subprocess.run(['sh', setup], cwd=fixture, check=True, capture_output=True)

    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=fixture, capture_output=True, text=True)
    cli = (fixture / 'app' / 'cli.py').read_text()
    assert branch.stdout.strip() == 'feature'
    assert ('if args.free < 0:' in cli) is present
