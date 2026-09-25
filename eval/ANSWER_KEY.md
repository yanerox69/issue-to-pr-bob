# Answer key (PRIVATE — never put this inside sample-app/)

| Bug | Issue | File | Root cause | Reference fix |
|---|---|---|---|---|
| 01 | ISSUE-001 | pricing.py | `ROUND_HALF_EVEN` (banker's rounding) | `ROUND_HALF_UP` |
| 02 | ISSUE-002 | discounts.py | `today < expires` excludes last day | `<=` |
| 03 | ISSUE-003 | discounts.py | 50% cap applied per coupon, not to the sum | sum valid percents, then cap |
| 04 | ISSUE-004 | inventory.py | `reserve` checks physical stock, ignores reservations | compare against `self.available(sku)` |
| 05 | ISSUE-005 | orders.py | `copy.copy` / `list()` shallow-copy; LineItems shared between cart and order | build new `LineItem`s in `place` and `reorder` |
| 06 | ISSUE-006 | csv_import.py | hand-rolled `split(",")` ignores quoting | `csv.DictReader` |
| 07 | ISSUE-007 | csv_import.py | `encoding="utf-8"` keeps the BOM → header `﻿sku` | `encoding="utf-8-sig"` |
| 08 | ISSUE-008 | dates.py | `weekday() > 5` treats Saturday as a business day | `>= 5` |
| 09 | ISSUE-009 | tax.py | exact-match `dict.get(..., 0)` → silent 0% | normalise `strip().upper()`, raise on unknown |
| 10 | ISSUE-010 | orders.py | id = `len(orders)+1` reuses ids after cancel | monotonic counter |

Difficulty mix: one-character fixes (01, 02, 08), logic (03, 04, 09, 10), subtle aliasing (05),
two bugs in one function (06 + 07 — a good fix resolves both).

Verified 2026-09-23: reference fixes score 10/10 with the repo suite green.
