# Data

The supplied Round 2 handoff contains the application source but does not include
the generated `tree.json` or the original `repo_5.xlsx` bytes. This repo therefore
does not invent replacement course/link data.

To populate the runtime data, place the real `repo_5.xlsx` beside the repository
(or provide its path) and run:

```bash
python tools/import_content.py path/to/repo_5.xlsx
```

That creates `data/tree.json`.

The new Google Docs/Drive fix operates on the real `url` values imported from
`repo_5.xlsx`; it does not manufacture document IDs or replace source links.
