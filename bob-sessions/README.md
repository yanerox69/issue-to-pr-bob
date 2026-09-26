# IBM Bob task session summaries

Solo team: all sessions were run by the single team member in IBM Bob 2.0 (IDE v2.1.0).

| Screenshot | Session | Bobcoins |
|---|---|---|
| `batch-A-summary-issues-001-004.png` | Batch A: `/Issue → PR` "Fix these issues one after another: ISSUE-002, 001, 003, 004". All 16 todo steps completed; each issue on its own branch. | 8.36 |
| `issue-002-reproducer-subtask.png` | One stage of batch A: the Reproducer subtask writing a failing regression test for ISSUE-002. | 0.58 |
| `issue-005-retry-summary-bob-says-fixed.png` | Second independent run on ISSUE-005. Bob reports "Fixed" and 21/21 visible tests pass, **but the hidden acceptance test still fails**: the fix covers `reorder()` and misses the same aliasing in `place()`. This is the miss documented in RESULTS.md. | 1.95 |

Batch B (ISSUE-005, 008, 009, 010) and batch C (ISSUE-006, 007) ran the same way. Their cost (~9.6
Bobcoins together) comes from the budget meter; see `eval/runs.csv`.
