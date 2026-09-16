"""
KIU Resource Hub
A Streamlit app that reads hostel, job and scholarship listings from a single
Excel workbook (data/listings.xlsx) and displays them as three browsable tabs.
Editing the workbook and pushing it to GitHub is the entire "content management"
system - there is no separate admin app or database.
"""

import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "listings.xlsx"

st.set_page_config(page_title="KIU Resource Hub", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 10px;
    }
    .khub-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 0.1rem; }
    .khub-subtitle { color: #5B6B66; font-size: 0.92rem; margin-bottom: 0.4rem; }
    .khub-field-label { color: #5B6B66; font-size: 0.78rem; margin-bottom: -0.3rem; }
    .khub-field-value { font-size: 0.95rem; }
    .khub-notes { color: #444; font-size: 0.88rem; font-style: italic; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=300, show_spinner="Loading listings...")
def load_workbook(path: str, mtime: float):
    return pd.read_excel(path, sheet_name=None, engine="openpyxl")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how="all").copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def fmt(val):
    """Render a cell for display; blank/NaN becomes None so callers can skip it."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return None
    if isinstance(val, pd.Timestamp):
        return val.strftime("%d %b %Y")
    text = str(val).strip()
    return text if text else None


def field(col, label, value):
    if value is None:
        return
    col.markdown(f'<div class="khub-field-label">{label}</div>', unsafe_allow_html=True)
    col.markdown(f'<div class="khub-field-value">{value}</div>', unsafe_allow_html=True)


def render_hostel(row):
    with st.container(border=True):
        st.markdown(f'<div class="khub-title">{fmt(row.get("Name")) or "Untitled listing"}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        field(c1, "Area", fmt(row.get("Area")))
        field(c2, "Price", fmt(row.get("Price (per semester)")))
        field(c3, "Room type", fmt(row.get("Room Type")))
        notes = fmt(row.get("Notes"))
        if notes:
            st.markdown(f'<div class="khub-notes">{notes}</div>', unsafe_allow_html=True)
        link = fmt(row.get("Link"))
        if link:
            st.link_button("View listing", link)


def render_job(row):
    with st.container(border=True):
        st.markdown(f'<div class="khub-title">{fmt(row.get("Job Title")) or "Untitled role"}</div>', unsafe_allow_html=True)
        org = fmt(row.get("Organization"))
        if org:
            st.markdown(f'<div class="khub-subtitle">{org}</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        field(c1, "Type", fmt(row.get("Type")))
        field(c2, "Location", fmt(row.get("Location")))
        field(c3, "Deadline", fmt(row.get("Deadline")))
        notes = fmt(row.get("Notes"))
        if notes:
            st.markdown(f'<div class="khub-notes">{notes}</div>', unsafe_allow_html=True)
        link = fmt(row.get("Link"))
        if link:
            st.link_button("Apply now", link)


def render_scholarship(row):
    with st.container(border=True):
        st.markdown(f'<div class="khub-title">{fmt(row.get("Scholarship Name")) or "Untitled scholarship"}</div>', unsafe_allow_html=True)
        provider = fmt(row.get("Provider"))
        if provider:
            st.markdown(f'<div class="khub-subtitle">{provider}</div>', unsafe_allow_html=True)
        eligibility = fmt(row.get("Eligibility"))
        if eligibility:
            st.markdown(f'<div class="khub-field-label">Eligibility</div>', unsafe_allow_html=True)
            st.markdown(eligibility)
        deadline = fmt(row.get("Deadline"))
        if deadline:
            st.markdown(f'<div class="khub-field-label">Deadline</div><div class="khub-field-value">{deadline}</div>', unsafe_allow_html=True)
        notes = fmt(row.get("Notes"))
        if notes:
            st.markdown(f'<div class="khub-notes">{notes}</div>', unsafe_allow_html=True)
        link = fmt(row.get("Link"))
        if link:
            st.link_button("Apply now", link)


TABS = {
    "🏠 Hostels": {
        "sheet": "Hostels",
        "filter_col": "Area",
        "renderer": render_hostel,
        "search_hint": "Search by name, area or room type",
        "empty_hint": "No hostels listed yet. Add rows to the Hostels sheet in listings.xlsx.",
    },
    "💼 Jobs Board": {
        "sheet": "Jobs",
        "filter_col": "Type",
        "renderer": render_job,
        "search_hint": "Search by title, organization or location",
        "empty_hint": "No jobs listed yet. Add rows to the Jobs sheet in listings.xlsx.",
    },
    "🎓 Scholarships": {
        "sheet": "Scholarships",
        "filter_col": "Provider",
        "renderer": render_scholarship,
        "search_hint": "Search by name, provider or eligibility",
        "empty_hint": "No scholarships listed yet. Add rows to the Scholarships sheet in listings.xlsx.",
    },
}

header_l, header_r = st.columns([5, 1])
with header_l:
    st.title("KIU Resource Hub")
    st.caption("Hostels, jobs and scholarships for KIU students, kept in one spreadsheet.")
with header_r:
    st.write("")
    if st.button("Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if not DATA_PATH.exists():
    st.error(
        f"Can't find {DATA_PATH.relative_to(Path(__file__).parent)}. "
        "Make sure listings.xlsx is committed under the data/ folder."
    )
    st.stop()

try:
    workbook = load_workbook(str(DATA_PATH), DATA_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"Couldn't read listings.xlsx: {exc}")
    st.stop()

tabs = st.tabs(list(TABS.keys()))

for tab, (label, cfg) in zip(tabs, TABS.items()):
    with tab:
        df = workbook.get(cfg["sheet"])
        if df is None:
            st.warning(f"No sheet named '{cfg['sheet']}' in listings.xlsx.")
            continue

        df = clean(df)
        if df.empty:
            st.info(cfg["empty_hint"])
            continue

        search_col, filter_col_ui = st.columns([3, 1])
        query = search_col.text_input(
            "Search", key=f"q_{cfg['sheet']}", placeholder=cfg["search_hint"], label_visibility="hidden"
        )
        filter_col = cfg["filter_col"]
        options = ["All"]
        if filter_col in df.columns:
            options += sorted(v for v in df[filter_col].dropna().unique().tolist() if str(v).strip())
        chosen = filter_col_ui.selectbox(filter_col, options, key=f"f_{cfg['sheet']}")

        rows = df
        if query:
            mask = df.astype(str).apply(
                lambda col: col.str.contains(query, case=False, na=False, regex=False)
            ).any(axis=1)
            rows = rows[mask]
        if chosen != "All" and filter_col in rows.columns:
            rows = rows[rows[filter_col] == chosen]

        st.caption(f"{len(rows)} of {len(df)} entries")

        if rows.empty:
            st.info("Nothing matches that search.")
        else:
            for _, row in rows.iterrows():
                cfg["renderer"](row)
