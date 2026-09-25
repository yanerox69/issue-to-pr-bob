"""Build submission/RESULTS.md from the scoring log and the run log.

    python eval/report.py --label bob-run-1

Reads eval/results.jsonl (the latest record with that label), eval/runs.csv (Bobcoins and
minutes per issue, filled in by hand from Bob's task panel) and eval/baseline_manual.csv.
"""

import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "submission" / "RESULTS.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    args = parser.parse_args()

    records = [json.loads(line) for line in open(HERE / "results.jsonl", encoding="utf-8") if line.strip()]
    matching = [r for r in records if r["label"] == args.label]
    if not matching:
        raise SystemExit(f"no results with label {args.label!r}; run eval/score.py --branches --label {args.label}")
    record = matching[-1]

    # Main-run rows only: "ISSUE-005-retry", "ISSUE-002-smoke" etc. are side runs.
    runs = [r for r in read_csv(HERE / "runs.csv") if r["issue"].count("-") == 1]
    baseline = read_csv(HERE / "baseline_manual.csv")

    bugs = record["bugs"]
    fixed = sum(bugs.values())
    coins = [c for c in (num(r["bobcoins"]) for r in runs) if c is not None]
    minutes = [m for m in (num(r["minutes"]) for r in runs) if m is not None]
    manual = [m for m in (num(r["minutes_to_fix_by_hand"]) for r in baseline) if m is not None]

    lines = [
        "# Results",
        "",
        f"Run `{args.label}` scored at {record['time']}.",
        "",
        "Every fix is checked by **hidden acceptance tests the agent never saw**, and only counts",
        "if the repo's own test suite still passes on that branch (no regressions).",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Bugs fixed (hidden tests) | **{fixed} / {len(bugs)}** |",
    ]
    if coins:
        lines.append(f"| Bobcoins total | {sum(coins):.2f} |")
        lines.append(f"| Bobcoins per fixed bug | {sum(coins) / max(fixed, 1):.2f} |")
    if minutes:
        lines.append(f"| Avg. wall-clock minutes per issue (Bob) | {sum(minutes) / len(minutes):.1f} |")
    if manual:
        lines.append(f"| Avg. minutes per bug by hand (baseline, n={len(manual)}) | {sum(manual) / len(manual):.1f} |")
    lines += ["", "## Per bug", "", "| Bug | Hidden test | Bobcoins | Minutes | Notes |", "|---|---|---|---|---|"]

    by_issue = {f"bug{int(r['issue'].removeprefix('ISSUE-')):02d}": r for r in runs}
    for bug, ok in bugs.items():
        run = by_issue.get(bug, {})
        lines.append(
            f"| {bug} | {'✅ fixed' if ok else '❌ open'} | {run.get('bobcoins', '')} "
            f"| {run.get('minutes', '')} | {run.get('notes', '')} |"
        )

    if record.get("mode") == "branches":
        lines += ["", "## Branches", "", "| Branch | Own suite | Hidden tests passing |", "|---|---|---|"]
        for branch, res in record["branches"].items():
            passing = ", ".join(b for b, ok in res["bugs"].items() if ok) or "-"
            lines.append(f"| `{branch}` | {'pass' if res['suite_ok'] else 'FAIL'} | {passing} |")

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
