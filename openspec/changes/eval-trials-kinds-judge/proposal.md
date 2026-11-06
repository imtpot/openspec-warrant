## Why

A comparison with Anthropic's eval guidance ("Demystifying evals for AI
agents", "Develop tests") showed three gaps in the behavioral evals:

- Each scenario runs once per agent. With a non-deterministic agent, one pass
  does not tell "the skill works" from "the run was lucky", and one failure
  does not tell a regression from noise. The guidance asks for several trials
  and, where consistency matters, pass^k (all k trials pass).
- All scenarios form one suite, and any failure sets exit code 1. Nothing
  records which scenarios must stay near 100% (regression) and which measure
  behavior that agents do not yet show reliably (capability).
- Review checks match keywords. The guidance calls such graders brittle, and
  the history confirms it: `fafafce` and `5300db3` each widened a review
  term list after a correct report failed.

### Replaced archived decision

The judge replaces part of Decision 7 of the archived `add-warrant-core`
design ("Checker rules, not model grading ... Rejected: a model grading the
artifacts, because results would vary between runs and cost more") and of
Decision 7 of the archived `add-warrant-review` design ("Deterministic
checkers"), for review findings only. Both reasons still hold but weigh less
than the current cost: the judge runs only when every term misses, so
deterministic matches stay deterministic and calls are few, and the variance
is measured by calibration and bounded by counting `unknown` as a miss. All
other checkers stay deterministic.

The requester confirmed this replacement after seeing the archived decision.

## Why code is needed

The runner runs each scenario once and computes the exit code from every
entry; the review checker and the benchmark review score match terms only. No
scenario parameter or existing tool repeats runs, splits totals by suite or
judges a report. Widening term lists again is the current workaround and
keeps failing on the next synonym.

## What Changes

- `python -m warrant_evals --runs N` runs each scenario N times per agent. The
  report has one entry per scenario and agent with `k/N` passed runs and the
  transcript of each run. An entry passes only when all N runs pass.
- A scenario file can set `suite = "capability"`; the default is
  `regression`. The report shows each entry's suite and separate totals per
  suite. Only failed
  regression entries set exit code 1.
- An expected finding in a review scenario and a planted problem in a
  benchmark review task can carry a description. When no term of such an item
  appears in the report text, an LLM judge decides with the answer `yes`, `no`
  or `unknown`. The judge runs through the `claude` CLI with a model other than
  the default agent model and with no tools.
- The review scenarios and the benchmark review tasks get descriptions for
  their expected findings and planted problems.
- A tracked calibration set of labeled report excerpts and
  `python -m warrant_evals.judge` measure how often the judge agrees with the
  labels, as the guidance asks for model-based graders.

## Out of scope

This change adds repeated runs, scenario suites and a judge for review
findings; it does not change what any scenario tests.

- A judge for checkers other than the review checker and the benchmark review
  score, and for `untraced_absent` and `untraced_lines`.
- A judge that also re-checks items that a term already matched (false-pass
  detection).
- A `--judge-model` option, a `--no-judge` option and a judge through the
  Anthropic SDK.
- Variance, confidence intervals or pass^k columns in the benchmark summary.
- Caching of judge verdicts.
- Concurrent runs.

## Assumptions

- `--runs` defaults to 1, so a run without the option costs what it costs
  now. Owner: requester.
- Every existing scenario stays `regression` until the requester marks one
  `capability`. Owner: requester.
- An entry is `fail` when any of its runs fails, `not run` when no run failed
  and at least one did not run, and `pass` otherwise. `not run` entries do
  not set exit code 1, as now. Owner: requester.
- The judge model is `sonnet`: the judge must tell a reported defect from a
  passing mention, and it runs only on keyword misses, so a stronger model
  costs little. It differs from Claude Code's default agent model, but not
  from a benchmark run with `--model claude=sonnet`. Owner: requester.
- Calibration reports agreement and lists disagreements; it sets no pass
  threshold. The result is recorded in tasks.md, and a low agreement means a
  change of model or rubric before the judge is relied on. Owner: requester.
- Calibration cases are excerpts copied from eval transcripts (which
  `evals/out/` does not track) plus written cases that mention the code
  without reporting the defect. Owner: requester.
- An `unknown` verdict counts as not found, and the checker message names it
  as `unknown`, so a person reads the transcript. Owner: requester.
- A judge call that fails (no `claude` CLI, non-zero exit, timeout, output
  without a verdict) gives `unknown` with the reason. Owner: requester.
- In review scenarios the judge reads only the text of the expected finding's
  axis section, so "under its own axis" stays checked. Owner: requester.
- Items without a description stay keyword-only. Owner: requester.
- Codex runs are judged through the `claude` CLI too, so judging a Codex
  report needs an authenticated `claude`. Owner: requester.
- `uv run pytest` never calls the real judge; tests inject a fake judge.
  Owner: requester.
- With `--runs` above 1, transcripts are named `<scenario>-<agent>-<n>.log`;
  with one run they keep the name `<scenario>-<agent>.log`, so the benchmark,
  which names its own runs, is unaffected. Owner: requester.
- A described item is written as `{ terms = [...], description = "..." }` in
  the same array as plain term lists. Owner: requester.
- In calibration, an `unknown` verdict counts as a disagreement, since the
  checker treats it as a miss. Owner: requester.
- The judge times out after 120 seconds; messages of a failed run in a
  multi-run entry start with `run <n>: `. Owner: requester.
- A missing or malformed calibration file stops the calibration command with
  an error that names the file. Owner: requester.
- About 20 calibration cases, roughly half `yes` and half `no`. Owner:
  requester.
- `evidence` groups (a command name) and the `review-no-change` statement "no
  OpenSpec change" get no description: they are not defects a judge can
  recognize. Owner: requester.
- The scenario field is `suite`, not `kind`, because benchmark task files
  already use `kind` for `review` and `implement`. Owner: requester.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `behavioral-evals`: repeated runs, scenario suites and the exit code, the
  result report, and the judge in the review scenario checks.
- `benchmark`: the judge decides described review problems that no term
  matches.

## Impact

- `evals/warrant_evals/runner.py`, `evals/warrant_evals/__main__.py`,
  `evals/warrant_evals/scenarios.py`, `evals/warrant_evals/checks.py`,
  `evals/warrant_evals/benchmark.py`, new `evals/warrant_evals/judge.py`.
- `evals/scenarios/review-*.toml`, `evals/benchmark/review-*.toml`, new
  `evals/judge/calibration.toml`.
- `evals/tests/test_runner.py`, `evals/tests/test_cli.py`,
  `evals/tests/test_review_check.py`, `evals/tests/test_benchmark.py`, new
  `evals/tests/test_judge.py` and `evals/tests/conftest.py`.
- `docs/benchmark.md`.
- No new Python dependency; the judge needs the `claude` CLI at eval time.
