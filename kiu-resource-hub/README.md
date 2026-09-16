# KIU Resource Hub

A Streamlit app for KIU students with three tabs — Hostels, Jobs Board, and
Scholarships. All the content lives in one Excel file, `data/listings.xlsx`.
There's no database and no separate admin app: to add or change a listing,
edit that spreadsheet and push it to GitHub.

## What's in this folder

```
kiu-resource-hub/
├── app.py                  the Streamlit app
├── requirements.txt        Python packages Streamlit Cloud installs
├── data/
│   └── listings.xlsx       the content - Instructions, Hostels, Jobs, Scholarships sheets
└── .streamlit/
    └── config.toml         color theme
```

Open `listings.xlsx` and read its **Instructions** sheet first - it explains
the five rules that keep the app working (don't rename tabs, one entry per
row, the Link column takes any URL, etc). Each of the three content sheets
has one shaded example row showing the expected format; replace it with a
real entry once you're ready.

## Put it on GitHub (no terminal needed)

1. Unzip the download. You should see `app.py`, `requirements.txt`,
   `README.md`, and the `data` and `.streamlit` folders sitting side by side —
   that's the repo root, not a folder to open first.
2. Go to **github.com** and sign in, then click **New repository**. Name it
   (e.g. `kiu-resource-hub`), leave it empty (no README/license), and create it.
3. On the empty repo's page, click **uploading an existing file**.
4. Select everything you unzipped — `app.py`, `requirements.txt`,
   the whole `data` folder, and the whole `.streamlit` folder — drag it all in,
   and commit. GitHub's drag-and-drop preserves the folder structure, so
   `data/listings.xlsx` and `.streamlit/config.toml` land in the right places.

## Deploy on Streamlit Community Cloud (also no terminal)

1. Go to **share.streamlit.io** and sign in with your GitHub account.
2. Click **New app** (or "Create app"), then **choose an existing repository**
   and pick the repo you just created.
3. Set **Main file path** to `app.py`, choose the branch (`main`), and click
   **Deploy**.
4. Streamlit Cloud installs `requirements.txt` and starts the app. First
   deploy takes a minute or two; you'll get a `*.streamlit.app` link to share.

## Updating listings later

Edit `data/listings.xlsx` directly in GitHub: open the file in your repo,
click the pencil (**Edit**) icon — GitHub will offer to let you replace it
by uploading a new version, which is the easiest way to edit a spreadsheet.
Commit the change. Streamlit Cloud watches the repo and redeploys
automatically within a minute or two; you can also open the app and press
its **Refresh data** button to see the change without waiting for a redeploy.

## Notes on this first version

- Search and a one-field filter (Area / Type / Provider) are built into
  each tab; there's no login or write-back to the sheet from the app itself.
- Listings are read fresh from the workbook (cached 5 minutes) rather than
  copied into a database, so editing the spreadsheet is the entire editing
  workflow.
