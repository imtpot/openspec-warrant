"""Read warrant's shipped rules and the rules OpenSpec renders for a project."""

import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ARTIFACTS = ['proposal', 'specs', 'design', 'tasks']
OPERATIONS = ['apply', 'archive']
MARK = '[warrant] '
ENTRY = re.compile(r'^\s*- "(.*)"\s*$')


def shipped(rules_file: Path) -> dict[str, list[str]]:
    """Entries per artifact and operation, read line by line from rules.yaml."""
    result: dict[str, list[str]] = {}
    key = None
    for line in rules_file.read_text().splitlines():
        if heading := re.match(r'^ {2}(\w+):$', line):
            key = heading.group(1)
        elif (entry := ENTRY.match(line)) and key:
            result.setdefault(key, []).append(entry.group(1))
    return result


def _openspec(args: list[str], cwd: Path) -> dict:
    done = subprocess.run(['openspec', *args, '--json'], cwd=cwd, capture_output=True, text=True, check=True)
    return json.loads(done.stdout)


def rendered(project: Path) -> dict[str, list[str]]:
    """Rules, operation guidance and context as OpenSpec renders them for `project`."""
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / 'project'
        shutil.copytree(project / 'openspec', copy / 'openspec')
        subprocess.run(['openspec', 'new', 'change', 'probe'], cwd=copy, capture_output=True, check=True)
        (copy / 'openspec' / 'changes' / 'probe' / 'tasks.md').write_text('- [ ] 1.1 probe\n')
        result = {a: _openspec(['instructions', a, '--change', 'probe'], copy).get('rules') or [] for a in ARTIFACTS}
        for op in OPERATIONS:
            result[op] = _openspec(['instructions', op, '--change', 'probe'], copy).get('operationGuidance') or []
        context = _openspec(['instructions', 'proposal', '--change', 'probe'], copy).get('context')
        result['context'] = [context] if context else []
        return result


def split(rules: dict[str, list[str]]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """(warrant entries, project entries) per key."""
    keys = ARTIFACTS + OPERATIONS
    return (
        {k: sorted(e for e in rules.get(k, []) if e.startswith(MARK)) for k in keys},
        {k: sorted(e for e in rules.get(k, []) if not e.startswith(MARK)) for k in keys},
    )
