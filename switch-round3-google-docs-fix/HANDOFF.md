# Switch — Round 3 Fix Handoff

## Scope

This round makes **only the requested fixes** on top of the Round 2 snapshot:

1. Fix access to `drive_notes` / `drive_questions` Google Drive/Google Docs resources by deriving a usable Google preview URL from supported Google URL forms.
2. Replace the generic Viewer placeholder for Google Docs/Drive note/question resources with an **inline Google viewer**.
3. Avoid the stray `</div>` UX artifact associated with the old placeholder HTML.

No redesign, new authentication flow, new dependency, upload flow, ads/feed work, or unrelated cleanup was added.

## Source basis

The supplied Round 2 handoff says that `drive_notes` and `drive_questions` are mapped to `note` and `doc` resource types, while `pages/6_Viewer.py` previously sent every non-video resource into the generic inline-preview placeholder. It also explicitly states that non-YouTube documents were still placeholders at that point.

The Round 2 snapshot also records the existing resource mapping:

- `drive_notes` -> `note`
- `drive_questions` -> `doc`

and preserves the original `url` field on each resource.

## Files changed

### `tree_store.py`

Added `google_doc_embed_url()`.

Supported inputs:

- `https://docs.google.com/document/d/<DOCUMENT_ID>/...`
- `https://drive.google.com/file/d/<FILE_ID>/...`
- `https://drive.google.com/open?id=<FILE_ID>`

For `drive_notes` and `drive_questions`, the resource shape now carries:

`google_doc_embed_url`

The original `url` is not overwritten.

If a URL is not a recognized Google Docs/Drive URL, the helper returns `None` rather than inventing an ID or URL.

### `pages/6_Viewer.py`

Viewer behavior is now:

- YouTube -> existing inline YouTube iframe.
- Google Docs/Drive note/question -> inline Google preview using Streamlit's iframe component.
- Other resources -> existing placeholder behavior remains unchanged.

The old placeholder HTML is therefore no longer used for supported Google Docs/Drive note/question links.

## Important limitation

The Round 2 handoff supplied to this task contains the application source snapshot, but it does **not** contain the actual `repo_5.xlsx` bytes or the generated `data/tree.json`. This repo does not invent document IDs or fabricate course data.

The real `repo_5.xlsx` must be supplied and imported with the existing importer before the app has its real course/link dataset.

## Verification

- All reconstructed Python source files compile successfully.
- The new URL helper is deliberately conservative: it only creates preview URLs when a Google Docs/Drive document ID can be extracted.
- No new pip dependency was introduced.
- The existing `requirements.txt` remains unchanged.

## Expected UX

Opening a real `drive_notes` or `drive_questions` resource that contains a supported Google Docs/Drive URL should now show the document **inside the Switch Viewer**, rather than the old placeholder.

The original URL remains available in the resource data for normal external access.

If the underlying Google document is private or the signed-in browser account lacks access, Google's own viewer may still require permission. This code fix does not bypass Google access controls.

## Deploy

Upload the repository contents to the Git repository used by Streamlit.

The app entry point remains:

`app.py`

The existing Round 2 deployment structure and dependency set are retained.
