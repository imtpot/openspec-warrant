"""Mechanical checks of the warrant-kit principles (openspec/specs/warrant-kit)."""

import re
import tomllib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SKILLS = sorted(p.parent.name for p in (REPO / 'skills').glob('*/SKILL.md'))
AGENT_WORDS = [
    'Claude', 'Codex', 'Copilot', 'Cursor', 'Gemini', 'agy',
    'Skill tool', 'Task tool', 'TodoWrite',
]
# Every supported agent starts sub-agents; skills ask for one without a fallback.
FALLBACK = 'If you cannot start a separate context'


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


def _section(text: str, start: str, end: str | None = None) -> str:
    tail = text[text.index(start):]
    return tail[:tail.index(end)] if end else tail


def test_apply_guidance_implements_each_group_in_a_sub_agent():
    apply = _section(RULES_FILE.read_text(), '  apply:', '  archive:')

    assert 'fresh context (a sub-agent)' in apply
    assert 'task group' in apply
    assert apply.index('warrant-verify') < apply.lower().index('check off')


def test_apply_guidance_routes_settled_groups_to_a_smaller_model():
    apply = _section(RULES_FILE.read_text(), '  apply:', '  archive:')

    assert 'smaller, faster model' in apply
    assert "session's model" in apply


def test_apply_guidance_gives_a_path_after_revise():
    apply = _section(RULES_FILE.read_text(), '  apply:', '  archive:')

    assert 'Artifact review: REVISE' in apply
    assert 'review again' in apply
    assert 'ask the requester and stop before the first task' in apply


# warrant-rules: Test task per requirement
def test_tasks_rules_ask_for_a_test_task_per_requirement():
    tasks = _section(RULES_FILE.read_text(), '  tasks:', 'operations:')

    assert 'add a task that names the requirement and writes its tests' in tasks
    assert tasks.index('writes its tests') < tasks.index('End the task list')


# warrant-rules: Option ladder in the design
def test_design_rule_lists_the_option_ladder_in_order():
    design = _section(RULES_FILE.read_text(), '  design:', '  tasks:')
    rungs = ['no change', 'existing project code', 'the standard library or platform',
             'an installed dependency', 'new code']
    positions = [design.index(rung) for rung in rungs]

    assert positions == sorted(positions)
    assert 'warrant-minimal-change' not in design


def test_tasks_are_checked_off_only_after_passing_verification():
    apply = _section(RULES_FILE.read_text(), '  apply:', '  archive:')

    assert 'only when every verification command exited with 0' in apply


def test_archive_guidance_replaces_the_placeholder_purpose():
    archive = RULES_FILE.read_text().split('  archive:')[1]

    assert 'placeholder Purpose' in archive


def test_no_rule_joins_instructions_with_a_semicolon():
    assert [line for line in _rule_lines() if ';' in line] == []


def test_tasks_rules_ask_for_independent_groups():
    tasks = _section(RULES_FILE.read_text(), '  tasks:', 'operations:')

    assert "without another group's unfinished work" in tasks


def test_verification_results_have_a_parsable_format():
    text = RULES_FILE.read_text()
    tasks = text[text.index('  tasks:'):text.index('operations:')]

    assert "'Result: exit <code>, <result line>'" in tasks
    assert "'Result: not run, <reason>'" in tasks
    assert "'Result: exit 0'" in text[text.index('  archive:'):]


@pytest.mark.parametrize('name', SKILLS)
def test_fresh_context_has_no_fallback(name):
    assert FALLBACK not in _skill(name), f'{name} still describes an agent without sub-agents'


def _prose(name: str, start: str, end: str) -> str:
    return ' '.join(_section(_skill(name), start, end).split())


# verification-evidence: Development runs allowed; Only contract commands are evidence
def test_verify_allows_narrowed_runs_that_are_not_evidence():
    step = _prose('warrant-verify', '## 3.', '## 4.')

    assert 'narrowed or diagnostic run' in step
    assert 'while you work' in step
    assert 'Only the Verification commands' in step
    assert 'are evidence' in step


# test-first: Narrowed runs are not evidence
def test_tdd_narrowed_runs_are_not_evidence():
    red = _prose('warrant-tdd', '### Red', '### Green')

    assert 'not evidence that the work is complete' in red


# minimal-change: Every line traces to a requirement; Named trace basis
def test_minimal_change_traces_every_line_to_a_named_basis():
    trace = _prose('warrant-minimal-change', '## Trace every line', '## Mark')

    for label in ('requirement: <name>', 'protected: <item>', 'standard: <file>'):
        assert label in trace
    assert '### Standards' in trace
    assert 'Anything the requester asked for' in trace


# code-review: Untraced line
def test_review_untraced_line_has_none_of_the_bases():
    spec = _prose('warrant-review', '### 3. Spec axis', '### 4.')

    assert '"Trace every line"' in spec
    assert 'none of these bases' in spec
    assert 'Protected code' in spec
    assert '### Standards' in spec


# code-review: Missing tasks
def test_review_artifact_blocks_requirement_no_task_names():
    artifact = _prose('warrant-review', '## Artifact mode', '## Receive mode')

    assert 'a requirement that no task names' in artifact


# code-review: Change selection
def test_review_receive_chooses_change_as_in_review_mode():
    receive = _prose('warrant-review', '## Receive mode', '2. List')

    assert 'Choose the OpenSpec change as in Review mode step 2.' in receive


# test-first: Fail for the expected reason
def test_tdd_missing_code_under_test_is_red():
    red = _prose('warrant-tdd', '3. Read the result', '### Green')

    assert 'function, module or attribute under test, does not exist yet: go to Green' in red
    assert 'because of an error in the test (import, syntax, wrong fixture)' in red


# test-first: Mutation check
def test_tdd_mutation_check_applies_runs_and_reverts():
    finish = _prose('warrant-tdd', '## 3. Finish', '## Report')

    assert 'apply it, run the tests, and revert it' in finish
    assert 'run it on the mutated code (red), revert, and run it again (green)' in finish
    assert 'Leave no mutation in the code' in finish


# verification-evidence: Destructive verification
def test_tdd_narrowed_run_follows_destructive_actions():
    red = _prose('warrant-tdd', '2. Run only this test', '3. Read the result')

    assert 'Destructive actions' in red
    assert '`warrant-verify` step 2' in red


# verification-evidence: Fresh evidence only
def test_verify_fresh_evidence_counts_files_the_commands_read():
    step = _prose('warrant-verify', '## 3.', '## 4.')

    assert 'a file the commands read' in step
    assert 'Recording results in OpenSpec artifacts' in step
    assert 'files under verification' not in step


# verification-evidence: Destructive verification
def test_verify_destructive_check_covers_every_command():
    step = _prose('warrant-verify', '## 2.', '## 3.')

    assert 'every command you run in this project' in step
    assert 'narrowed and diagnostic runs' in step


# verification-evidence: Development runs allowed; project-contract: No guessed commands
def test_verify_runs_no_command_without_a_contract():
    step = _prose('warrant-verify', '## 1.', '## 2.')

    assert 'Run no test, lint, type-check or build command' in step
    assert 'not even a narrowed or diagnostic one' in step


# setup: No OpenSpec root
def test_setup_names_init_without_a_profile():
    step = _prose('warrant-setup', '## 2.', '## 3.')

    assert '`openspec init --tools agents`' in step
    assert '--profile' not in _skill('warrant-setup')


# setup: Install the rules
def test_setup_looks_for_rules_next_to_its_own_skill_first():
    step = _prose('warrant-setup', '## 4.', '## 5.')

    assert '`rules.yaml` in the directory of this `SKILL.md`' in step
    assert step.index('directory of this `SKILL.md`') < step.index('`.agents/skills/warrant-setup/rules.yaml`')
    assert 'If none exists, stop' in step


# minimal-change: Debt ledger
def test_ledger_command_skips_installed_skills_of_every_agent():
    step = _prose('warrant-minimal-change', '## Shortcut ledger', '2. Print one line')

    assert "-- ':(exclude,glob).*/skills/**'`" in step
    assert 'skips installed skills' in step
