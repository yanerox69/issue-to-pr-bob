"""Score shopcart against the hidden per-bug acceptance tests.

    python eval/score.py                          # scores ../sample-app working tree
    python eval/score.py --repo path --label x    # scores another checkout
    python eval/score.py --branches --label run1  # scores every fix/* branch of sample-app

A bug counts as fixed only if its hidden test file passes AND the repo's own test suite
still passes (no regressions). With --branches, each fix/issue-XXX branch is checked out
in a temporary git worktree and scored on its own; the run's score is the union of bugs
fixed across branches. Results are appended to eval/results.jsonl.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
HIDDEN = HERE / "hidden_tests"
SAMPLE_APP = HERE.parent / "sample-app"


def run_pytest(target: Path, repo: Path, cwd: Path) -> bool:
    env = {**os.environ, "SHOPCART_REPO": str(repo)}
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(target)],
            cwd=cwd, env=env, capture_output=True, text=True, timeout=60,
            stdin=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        print(f"    timeout: {target.name} ({repo.name})", flush=True)
        return False
    return result.returncode == 0


def score_repo(repo: Path) -> tuple[bool, dict[str, bool]]:
    suite_ok = run_pytest(repo / "tests", repo, repo)
    bugs = {}
    for test_file in sorted(HIDDEN.glob("test_bug*.py")):
        bug = test_file.stem.split("_")[1]  # "bug01"
        bugs[bug] = suite_ok and run_pytest(test_file, repo, HERE)
    return suite_ok, bugs


def git(*args: str, cwd: Path = SAMPLE_APP) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def score_branches() -> dict[str, tuple[bool, dict[str, bool]]]:
    branches = [b.strip().lstrip("* ") for b in git("branch", "--list", "fix/*").splitlines() if b.strip()]
    results = {}
    tmp_root = Path(tempfile.mkdtemp(prefix="shopcart-score-"))
    try:
        for branch in branches:
            print(f"  scoring {branch} ...", flush=True)
            tree = tmp_root / branch.replace("/", "_")
            git("worktree", "add", "--detach", str(tree), branch)
            try:
                results[branch] = score_repo(tree)
            finally:
                git("worktree", "remove", "--force", str(tree))
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=str(SAMPLE_APP))
    parser.add_argument("--branches", action="store_true", help="score every fix/* branch")
    parser.add_argument("--label", default="manual")
    args = parser.parse_args()

    record = {"time": datetime.now().isoformat(timespec="seconds"), "label": args.label}
    if args.branches:
        per_branch = score_branches()
        union: dict[str, bool] = {}
        print(f"{'branch':<20} {'suite':<6} bugs fixed")
        for branch, (suite_ok, bugs) in per_branch.items():
            fixed = [b for b, ok in bugs.items() if ok]
            print(f"{branch:<20} {'PASS' if suite_ok else 'FAIL':<6} {', '.join(fixed) or '-'}")
            for b, ok in bugs.items():
                union[b] = union.get(b, False) or ok
        score = sum(union.values())
        print(f"score (union): {score}/{len(union)}")
        record.update({
            "mode": "branches",
            "branches": {br: {"suite_ok": s, "bugs": b} for br, (s, b) in per_branch.items()},
            "bugs": union, "score": score,
        })
    else:
        repo = Path(args.repo).resolve()
        suite_ok, bugs = score_repo(repo)
        score = sum(bugs.values())
        print(f"repo:        {repo}")
        print(f"repo suite:  {'PASS' if suite_ok else 'FAIL (regressions -> fixes not counted)'}")
        for bug, ok in bugs.items():
            print(f"  {bug}: {'fixed' if ok else 'open'}")
        print(f"score:       {score}/{len(bugs)}")
        record.update({"mode": "repo", "repo": str(repo), "suite_ok": suite_ok, "bugs": bugs, "score": score})

    with open(HERE / "results.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
