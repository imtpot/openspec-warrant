import shutil
import subprocess

import pytest

from warrant_evals.workspace import prepare_workspace

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
