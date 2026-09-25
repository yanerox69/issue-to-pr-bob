# ISSUE-009: Some California orders are charged no sales tax

**Reporter:** tax compliance · **Severity:** critical · **Labels:** bug, tax, compliance

Audit found orders shipped to California with $0.00 tax. All of them came from the new
mobile checkout, which sends the region as `"ca"` (lowercase) or with trailing spaces
(`"CA "`). The web checkout sends `"CA"` and is fine.

Region codes should be treated case-insensitively and trimmed. We'd also rather fail
loudly than silently charge 0% for a region we don't recognise — but Oregon (`OR`)
legitimately has 0% sales tax.
