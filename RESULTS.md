# Results

Run `bob-run-1-final` scored at 2026-09-25T15:49:38.

Every fix is checked by **hidden acceptance tests the agent never saw**, and only counts
if the repo's own test suite still passes on that branch (no regressions).

| Metric | Value |
|---|---|
| Bugs fixed (hidden tests) | **9 / 10** |
| Bobcoins total | 18.02 |
| Bobcoins per fixed bug | 2.00 |

## Per bug

| Bug | Hidden test | Bobcoins | Minutes | Notes |
|---|---|---|---|---|
| bug01 | ✅ fixed | 2.09 |  | batch A (8.36 total / 4 issues) |
| bug02 | ✅ fixed | 2.09 |  | batch A (8.36 total / 4 issues) |
| bug03 | ✅ fixed | 2.09 |  | batch A (8.36 total / 4 issues) |
| bug04 | ✅ fixed | 2.09 |  | batch A (8.36 total / 4 issues) |
| bug05 | ❌ open | 1.61 |  | batches B+C ~9.64 / 6 issues (from budget meter 95%->59%); fix incomplete (hidden test) |
| bug06 | ✅ fixed | 1.61 |  | batches B+C ~9.64 / 6 issues (from budget meter 95%->59%) |
| bug07 | ✅ fixed | 1.61 |  | batches B+C ~9.64 / 6 issues (from budget meter 95%->59%) |
| bug08 | ✅ fixed | 1.61 |  | batches B+C ~9.64 / 6 issues (from budget meter 95%->59%) |
| bug09 | ✅ fixed | 1.61 |  | batches B+C ~9.64 / 6 issues (from budget meter 95%->59%) |
| bug10 | ✅ fixed | 1.61 |  | batches B+C ~9.64 / 6 issues (from budget meter 95%->59%) |

## Branches

| Branch | Own suite | Hidden tests passing |
|---|---|---|
| `fix/issue-001` | pass | bug01 |
| `fix/issue-002` | pass | bug02 |
| `fix/issue-003` | pass | bug03 |
| `fix/issue-004` | pass | bug04 |
| `fix/issue-005` | pass | - |
| `fix/issue-006` | pass | bug06 |
| `fix/issue-007` | pass | bug07 |
| `fix/issue-008` | pass | bug08 |
| `fix/issue-009` | pass | bug09 |
| `fix/issue-010` | pass | bug10 |
