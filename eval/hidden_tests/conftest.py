"""Hidden acceptance tests: one file per seeded bug. Kept OUTSIDE the sample repo so the
agent under evaluation can't read them. Point SHOPCART_REPO at the repo to evaluate."""

import os
import sys
from pathlib import Path

REPO = Path(os.environ.get("SHOPCART_REPO", Path(__file__).parents[2] / "sample-app")).resolve()
sys.path.insert(0, str(REPO))
