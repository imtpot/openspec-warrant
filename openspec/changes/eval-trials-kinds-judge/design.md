## Context

See proposal.md - Why. `run_evals` (`runner.py`) calls `_run_one` once per
scenario and agent and returns one `Result` each; `write_report` writes one row
per `Result`; `__main__.main` exits 1 when any `Result` reads fail. The
benchmark reuses `_run_one` and `checks._missing`. `_missing(text, groups)`
returns the first term of each term group that has no term in the text; the
review checker calls it per axis section, and `benchmark.review_score` calls it
on the whole report. Tests in `test_cli.py` load the real review scenarios and
check exact messages such as `Spec section lacks: --json`.

## Goals / Non-Goals

**Goals:** the three behaviors in the delta specs, with no new Python
dependency and with `uv run pytest` still offline.

**Non-Goals:** see proposal.md - Out of scope. The benchmark keeps its own
`--runs`.

## Decisions

### 1. Repeated runs

Option ladder: (1) no change: there is no repeat option. (2) Existing code:
the benchmark repeats `_run_one` in a loop over `range(1, runs + 1)`; the same
loop fits `run_evals`. Taken.

- `run_evals` gets `runs: int = 1` and calls `_run_one` N times per scenario
  and agent. `_run_one` gets `number: int | None = None`; with a number it
  names the transcript `<scenario>-<agent>-<number>.log`, without one it keeps
  `<scenario>-<agent>.log`. `run_evals` passes a number only when `runs > 1`,
  so single runs and the benchmark (which calls `_run_one` without a number
  and already puts the run number in the scenario name) keep their names. Each
  call already creates its own workspace.
- A new `combine(results)` turns the N `Result`s of one scenario and agent into
  one `Result`: status per the "Entry status from runs" requirement, new fields
  `passed` (count of pass) and `runs` (N), messages of each failed or not-run
  run prefixed `run <n>: ` when N > 1 (unprefixed when N = 1), the union of
  `tools`, and new list fields `transcripts` and `workspaces` that skip `None`
  (a not-run result has no transcript). The single-run fields `transcript` and
  `workspace` stay for `_run_one` and the benchmark. `write_report` reads only
  the combined fields.
- `__main__` adds `--runs` with a type function that rejects values below 1 via
  `argparse.ArgumentTypeError`, so argparse exits with a usage error before
  any agent runs.

Rejected: one report row per run. It hides k/N and makes the reader count.

### 2. Scenario suite and exit code

Option ladder: (1) no change: no field exists. (2) Existing code: the loader
already reads optional fields with `data.get`. Taken.

- `Scenario.suite = 'regression'`; `load_scenarios` reads `suite` and raises
  `ValueError(f'{path.name}: unknown suite {value}')` for other values, like
  the unknown-checker error. The name is `suite`, not `kind`: benchmark task
  files already use `kind` for `review` and `implement`.
- `Result.suite` is copied from the scenario. `write_report` adds a Suite
  column and a Runs column (`k/N`), then one line per suite present:
  `regression: <passed entries>/<entries>`.
- `main` returns 1 when any entry has `suite == 'regression'` and
  `status == 'fail'`.

### 3. Judge

This replaces part of Decision 7 of the archived `add-warrant-core` design
("Checker rules, not model grading ... Rejected: a model grading the
artifacts, because results would vary between runs and cost more") and of
Decision 7 of the archived `add-warrant-review` design ("Deterministic
checkers"), for described review findings and planted review problems only.
Every term match, every other checker and the section-order checks stay
deterministic. Variance and cost still count, but they are bounded: the judge
runs only after every term misses, `unknown` counts as a miss, and
calibration (Decision 5) measures agreement. The cost they were weighed
against has grown: two commits widened review term lists after correct reports
failed (see proposal.md - Why).

Option ladder: (1) no change: the checks match terms only. (2) Existing code:
the runner already runs `claude -p` headless as a subprocess. Reused as the
transport. (3) Standard library: `subprocess`, `json`, `re`, `tempfile`.
(4) Installed dependency: none needed; the Anthropic SDK was rejected by the
requester. (5) New code: `warrant_evals/judge.py`, about 40 lines.

- `judge.ask(description: str, text: str) -> tuple[str, str]` returns
  `(verdict, reason)`. It runs, in a fresh temporary directory, with a 120 s
  timeout:
  `claude -p --model sonnet --tools "" --setting-sources project,local --no-session-persistence --output-format json`,
  with the prompt on stdin: a Codex report is the whole session output and can
  exceed the size of one command-line argument.
  It reads `result` from the JSON and takes the verdict from the first word of
  its first line (`yes`, `no` or `unknown`, any case). Every failure in the
  "Judge failure" requirement, and a command that cannot start (`OSError`),
  returns `('unknown', <reason>)`, so a judge failure never stops a run.
- Prompt (rubric): the description of one expected problem; the report text
  between `<report>` tags, marked as data and not instructions, with any
  `</report>` in it removed so it cannot close its own tag; the rule: answer
  `yes` only if the report identifies this problem as a defect or a finding;
  `no` if it does not, or only mentions the code or a related term; the
  problem is the defect, not only the change that causes it, so when the
  description names an effect (a wrong result, a broken caller, a broken
  rule), `yes` needs that effect stated, and flagging the change for another
  reason, such as untraced, is `no`; `unknown` if the text does not let you
  decide; first line one word, then one sentence of reason. The effect rule
  came from calibration (tasks.md 7.1).
- Item format: a term group stays a list of strings. A described item is an
  inline table in the same array: `{ terms = [...], description = "..." }`.
  TOML 1.0 allows mixed arrays, and `tomllib` reads them.
- `_missing(text, groups)` keeps its signature and return type. For a
  described item with no matching term it calls `judge.ask(description, text)`.
  On `yes` the item is present; on `no` it is missing with its first term; on
  `unknown` it is missing as `<first term> (judge: unknown, <reason>)`. The
  review checker passes the axis section's text, so the judge sees only that
  section, and the benchmark passes the whole report, as now. `transcript` and
  `untraced_absent` and `untraced_lines` use no descriptions and stay
  keyword-only, as do the other `_missing` callers (setup `context`,
  artifact-review `flaws`), which pass plain lists.
- `_missing` looks up `judge.ask` through the module at call time, so tests
  replace it. A new `evals/tests/conftest.py` has an autouse fixture that sets
  `judge.ask` to a fake that returns `('no', 'judge off in tests')`. Existing
  exact-message tests stay valid, and no test calls `claude`. `test_judge.py`
  binds the real function at import (`from warrant_evals.judge import ask`),
  which the fixture's later attribute swap does not affect, and replaces
  `subprocess.run` and `shutil.which` in `warrant_evals.judge`.
- The run list in the benchmark shows the `(judge: unknown, ...)` text in its
  Missed column without a change to `run_list`.

Model: `sonnet`, a constant `JUDGE_MODEL` in `judge.py`. Rejected: `haiku`.
The judge must tell a reported defect from a passing mention and match
domain synonyms ("banker's rounding" for "round half to even"); a false `yes`
silently loosens a regression check, and the judge runs only on keyword
misses, so the cheaper model saves little. Rejected: `opus`, Claude Code's
usual agent model; the judge should not share the agent's blind spots.

Rejected: `--json-schema` structured output. The first-word parse is enough
for three values and needs no knowledge of where the CLI puts structured
output.

### 4. Descriptions

Add descriptions to the Spec and Standards groups of `review-branch` and
`review-named-base`, to the Spec group of `review-protected` (all built on the
`review-branch` fixture), to the Standards group of `review-no-change`, and
to every planted problem of `evals/benchmark/review-refund.toml` and
`review-export.toml`. Each says what
is wrong, where, and why, in one or two sentences, taken from the fixture's
diff, spec or standards. Evidence groups (`make test`) and the
`review-no-change` Spec item ("no OpenSpec change") stay keyword-only: they
check that a command or a statement is named, not a defect.

### 5. Calibration

Option ladder: (1)-(4) nothing in the project or the standard library
measures a grader; (5) new code, about 25 lines in `judge.py`.

- `evals/judge/calibration.toml` holds `[[case]]` tables with `name`,
  `description`, `text` and `label` (`yes` or `no`). About 20 cases, roughly
  half each: report excerpts copied from eval transcripts of the review
  scenarios and benchmark review tasks, including the reports behind
  `fafafce` and `5300db3`; and written `no` cases that mention the
  planted code or term without reporting the defect, which is the false-pass
  risk.
- `judge.py` gets `calibrate(cases, ask) -> str`, which returns
  `agreement: k/N` and one line per disagreement
  (`<name>: label <label>, verdict <verdict>, <reason>`), and
  `main(path=CALIBRATION, ask=ask) -> int`, which loads the file, prints
  `calibrate`'s output and returns 0; the `__main__` block calls it. Tests pass
  a fake `ask` explicitly, so the conftest fixture does not affect them. An `unknown` verdict is
  a disagreement. A missing or malformed file makes `main` raise
  `SystemExit` with a message that names the file.
- No threshold and no pytest gate: calibration calls the real judge, so it
  runs manually, like the evals.

## Risks / Trade-offs

- [The judge says `yes` too easily and loosens a check] → It runs only after
  all terms miss, the rubric asks for the problem reported as a finding, and
  `unknown` counts as missing. The calibration set has `no` cases for passing
  mentions, and the transcript of each judged pass is read during the first
  full runs.
- [The calibration set is small and written by the same people as the
  rubric] → It measures gross errors, not a precise rate; add each judge error
  found in a transcript as a new case.
- [Judging a Codex report needs `claude`] → The verdict is `unknown` with the
  reason when `claude` is missing, so the entry fails visibly instead of
  passing.
- [N runs multiply quota use] → `--runs` defaults to 1.
- [With `--runs` above 1, transcript names gain `-<n>`] → Only the report
  links to them; single runs and the benchmark keep their names;
  `docs/benchmark.md` is updated.
