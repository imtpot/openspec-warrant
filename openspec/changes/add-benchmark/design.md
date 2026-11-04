# Design

## Decisions

### 1. Reuse the eval runner

The benchmark builds one `Scenario` per task, arm and run and passes it to the
runner's existing `_run_one`, so workspaces, `PATH`, setup scripts, timeouts
and transcripts behave as in the evals. The check function records scores
instead of findings. Option ladder: no configuration or existing tool runs
agents in two arms; the runner already does everything except scoring.

### 2. Agent commands with usage

The benchmark derives its agent commands from the eval agents:
Claude adds `--output-format json` and reads `usage` and `result`; Codex reads
the `tokens used` line; Copilot adds `--usage-output-file` in the workspace.
Claude also gets `--setting-sources project,local`. Tokens are all input
(including cache) plus output tokens as each agent reports them.

### 3. Hidden material outside the workspace

Acceptance tests, the reference implementation and faulty implementations
live in `evals/benchmark/<task>/hidden/`, which is never copied into the
workspace. Scoring copies them in after the agent has finished.

### 4. Baselines from the same fixture

The `bare` and `openspec` arms are derived from the fixture by turning the
contract into text, so all arms share one fixture and cannot drift apart.
`bare` installs no skill; `openspec` installs the OpenSpec skills; `warrant`
installs both and merges `rules.yaml`.

### 5. Implement task

The fixture holds a sound OpenSpec change `add-weighted-split` for
`split(total, weights)` in `app/split.py`. Faulty implementations each break
one requirement.
