# fix: strip UTF-8 BOM from Excel-saved CSV files (ISSUE-007)

Fixes ISSUE-007

## Summary

`load_products()` raised `KeyError: 'sku'` on any CSV saved from Excel via
"Save As → CSV UTF-8" because Excel prepends a UTF-8 BOM (U+FEFF) to the
file and the `open()` call used `encoding="utf-8"`, which does not strip it.

## Root Cause

`shopcart/csv_import.py` line 9:

```python
with open(path, encoding="utf-8") as f:
```

`utf-8` passes the BOM byte-sequence through as the literal character `\ufeff`.
`str.strip()` does not remove it (it is not ASCII whitespace), so the first
header token read was `'\ufeffsku'` instead of `'sku'`. Every subsequent
`row["sku"]` lookup then raised `KeyError`.

## Fix

One-word change — `utf-8` → `utf-8-sig`:

```python
with open(path, encoding="utf-8-sig") as f:
```

`utf-8-sig` silently strips the BOM when present and behaves identically to
`utf-8` when the BOM is absent, so both Excel-saved and Google Sheets exports
continue to work without any branching logic.

## Testing

- **New test:** `tests/test_csv_import.py::test_issue_007_bom_utf8_csv`
  — writes a BOM-prefixed CSV as raw bytes and asserts `products[0].sku == "A1"`.
- **Suite result:** 21/21 tests pass (`python -m pytest -q`).

## Risk / What to Review

- `utf-8-sig` is stdlib — no new dependency.
- Only the `open()` encoding argument changes; all parsing logic is untouched.
- Low risk: the codec is a strict superset of `utf-8` for BOM-free files.

---

```
git push origin fix/issue-007
```
