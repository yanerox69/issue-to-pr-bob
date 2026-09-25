# Issue → PR with IBM Bob 2.0

**From a bug report to a review-ready pull request, with one command and guardrails Bob enforces itself.**

Built solo for the IBM Bob 2.0 Hackathon (lablab.ai, Sep 25–27 2026).

## The problem
Fixing a reported bug is mostly glue work: decode the report, reproduce it, hunt for the cause, patch,
re-run everything, write the PR. AI assistants speed that up, but they also cut corners: they patch
symptoms, or "fix" a failing test by editing the test.

## The solution
Five Bob 2.0 custom modes ([`sample-app/.bob/custom_modes.yaml`](sample-app/.bob/custom_modes.yaml)):

```
                 /Issue → PR  Fix @issues/ISSUE-004.md
                               │
                     🎯 Orchestrator (no edit rights)
          creates fix/issue-XXX, runs each stage as a Bob subtask
                               │
   ┌───────────────┬───────────┴────────────┬──────────────────┐
   ▼               ▼                        ▼                  ▼
🧪 Reproducer   🔍 Diagnoser              🔧 Fixer           📝 PR Writer
failing test    root cause file:line     minimal fix,       commit +
                + same bug elsewhere     full suite green   prs/ISSUE-XXX.md
edit: tests/    edit: none               edit: shopcart/    edit: prs/
                (explore subagent)       (NOT tests/)
```

The edit restrictions are `fileRegex` tool-group rules, **enforced by Bob**, so the Fixer cannot
make a test pass by changing the test.

## How we measured it
- `sample-app/`: a small Python order-management library with **10 seeded, realistic bugs**, each
  written up as a user-style report in `sample-app/issues/`.
- `eval/hidden_tests/`: one acceptance test per bug, **kept outside the repo Bob works in**.
- `eval/score.py --branches`: checks out every `fix/*` branch in a temporary worktree; a bug counts as
  fixed only if its hidden test passes **and** the existing suite is still green.

See [RESULTS.md](RESULTS.md) for the numbers, and `fixes/` for every patch and PR description Bob produced
(in batch B the PR Writer committed ISSUE-008/009/010 but skipped writing the `prs/` file, so those three
have a commit message only).

## Repo layout
| Path | What |
|---|---|
| `sample-app/` | The project Bob works on (open only this folder in Bob) |
| `sample-app/.bob/custom_modes.yaml` | The five modes: the actual deliverable |
| `sample-app/issues/` | The 10 bug reports |
| `fixes/` | Bob's output per issue: `.patch` + PR description |
| `eval/` | Hidden tests, scorer, answer key, run logs |

## Reproduce it
```bash
cd sample-app
python -m pip install -e ".[dev]"
python -m pytest -q                          # 20 passed: the bugs are invisible to the existing suite
python ../eval/score.py                      # 0/10 on main
# In Bob: open sample-app/, then  /Issue → PR  Fix @issues/ISSUE-00X.md
python ../eval/score.py --branches --label my-run
```
