import json
import subprocess
from pathlib import Path

import pytest

import warrant_evals.judge as judge
from warrant_evals.judge import ask, calibrate, main


def _fake_claude(monkeypatch, stdout='', returncode=0, raises=None):
    """Replace `claude` with a fake that records its call and answers `stdout`."""
    calls = []

    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        if raises:
            raise raises
        return subprocess.CompletedProcess(argv, returncode, stdout, '')

    monkeypatch.setattr(judge.shutil, 'which', lambda name: f'/bin/{name}')
    monkeypatch.setattr(judge.subprocess, 'run', run)
    return calls


def _answer(result):
    return json.dumps({'type': 'result', 'result': result})


# Judge call: Judge command
def test_judge_command(monkeypatch):
    calls = _fake_claude(monkeypatch, _answer('yes\nIt is named.'))

    ask('Refunds round half up instead of half to even.', 'The report text.')

    [(argv, kwargs)] = calls
    assert argv[:-1] == [
        'claude', '-p', '--model', 'sonnet', '--tools', '', '--setting-sources', 'project,local',
        '--no-session-persistence', '--output-format', 'json', '--',
    ]
    prompt = argv[-1]
    assert 'Refunds round half up instead of half to even.' in prompt
    assert '<report>\nThe report text.\n</report>' in prompt
    assert kwargs['timeout'] == 120
    assert kwargs['capture_output'] and kwargs['text']
    cwd = Path(kwargs['cwd'])
    assert cwd != Path.cwd()
    assert not cwd.exists()  # a fresh temporary directory, removed after the call


@pytest.mark.parametrize(('result', 'verdict'), [
    ('Yes\nThe report names it.', 'yes'),
    ('no\nThe report does not name it.', 'no'),
    ('UNKNOWN.\nThe report is cut off.', 'unknown'),
    ('No. The report only mentions the function.', 'no'),
])
def test_verdict_from_first_word(monkeypatch, result, verdict):
    _fake_claude(monkeypatch, _answer(result))

    got, reason = ask('a problem', 'a report')

    assert got == verdict
    assert reason


def test_reason_is_the_rest_of_the_text(monkeypatch):
    _fake_claude(monkeypatch, _answer('Yes\nThe report names it.\n'))

    assert ask('a problem', 'a report') == ('yes', 'The report names it.')


# Judge failure: No claude CLI
def test_no_claude_cli(monkeypatch):
    calls = _fake_claude(monkeypatch, _answer('yes\nnamed'))
    monkeypatch.setattr(judge.shutil, 'which', lambda name: None)

    assert ask('a problem', 'a report') == ('unknown', 'claude not installed')
    assert calls == []


@pytest.mark.parametrize('fake', [
    {'stdout': _answer('yes\nnamed'), 'returncode': 1},
    {'raises': subprocess.TimeoutExpired(['claude'], 120)},
    {'stdout': 'not json'},
    {'stdout': json.dumps({'type': 'result'})},
    {'stdout': _answer('Maybe\nI cannot tell.')},
    {'stdout': _answer('')},
], ids=['non-zero exit', 'timeout', 'not json', 'no result', 'no verdict', 'empty result'])
def test_judge_failure_gives_unknown_with_reason(monkeypatch, fake):
    _fake_claude(monkeypatch, **fake)

    verdict, reason = ask('a problem', 'a report')

    assert verdict == 'unknown'
    assert reason


def _case(name, label):
    return {'name': name, 'description': f'{name} problem', 'text': f'{name} report', 'label': label}


def _fake_ask(answers):
    """A judge that answers by description: `answers[description] == (verdict, reason)`."""
    return lambda description, text: answers[description]


CASES = [_case('a', 'yes'), _case('b', 'no'), _case('c', 'no')]
ANSWERS = {
    'a problem': ('yes', 'named'),
    'b problem': ('no', 'not named'),
    'c problem': ('yes', 'it names the rounding defect'),
}


# Judge calibration: One disagreement
def test_one_disagreement():
    output = calibrate(CASES, _fake_ask(ANSWERS))

    assert output.splitlines() == ['agreement: 2/3', 'c: label no, verdict yes, it names the rounding defect']


# Judge calibration: Unknown verdict
def test_unknown_verdict_is_a_disagreement():
    output = calibrate([_case('a', 'yes')], _fake_ask({'a problem': ('unknown', 'claude not installed')}))

    assert output.splitlines() == ['agreement: 0/1', 'a: label yes, verdict unknown, claude not installed']


def test_calibrate_passes_description_and_text():
    seen = []

    calibrate([_case('a', 'yes')], lambda description, text: seen.append((description, text)) or ('yes', ''))

    assert seen == [('a problem', 'a report')]


def test_main_prints_calibration(tmp_path, capsys):
    path = tmp_path / 'calibration.toml'
    path.write_text(''.join(
        f'[[case]]\nname = "{c["name"]}"\ndescription = "{c["description"]}"\n'
        f'text = "{c["text"]}"\nlabel = "{c["label"]}"\n\n'
        for c in CASES
    ))

    assert main(path, ask=_fake_ask(ANSWERS)) == 0

    assert capsys.readouterr().out.splitlines() == [
        'agreement: 2/3', 'c: label no, verdict yes, it names the rounding defect',
    ]


# Calibration file failure: Missing file
def test_missing_calibration_file(tmp_path):
    path = tmp_path / 'judge' / 'calibration.toml'

    with pytest.raises(SystemExit) as raised:
        main(path, ask=_fake_ask({}))

    assert str(path) in str(raised.value.code)


def test_calibration_file_not_toml(tmp_path):
    path = tmp_path / 'calibration.toml'
    path.write_text('[[case]\nname = \n')

    with pytest.raises(SystemExit) as raised:
        main(path, ask=_fake_ask({}))

    assert str(path) in str(raised.value.code)


def test_calibration_file_without_cases(tmp_path):
    path = tmp_path / 'calibration.toml'
    path.write_text('name = "a"\n')

    with pytest.raises(SystemExit) as raised:
        main(path, ask=_fake_ask({}))

    assert str(path) in str(raised.value.code)


def test_default_calibration_path():
    assert judge.CALIBRATION == Path(__file__).resolve().parents[2] / 'evals' / 'judge' / 'calibration.toml'
    assert main.__defaults__[0] == judge.CALIBRATION
