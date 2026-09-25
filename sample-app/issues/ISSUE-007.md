# ISSUE-007: Import fails with KeyError 'sku' on files saved from Excel

**Reporter:** catalog team · **Severity:** medium · **Labels:** bug, import

When we open the catalog in Excel and "Save As → CSV UTF-8", the import fails:

```
KeyError: 'sku'
```

The file looks identical in a text editor, and the header is definitely `sku,name,price,category`.
The same file saved from Google Sheets imports fine.
