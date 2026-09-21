from pathlib import Path
import re

import pandas as pd
import streamlit as st

from specialist_mapping import normalize_specialist

# Resolved from this file's own location (not the caller's), so it works
# correctly whether imported from app.py or from pages/*.py.
APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR / "hospitals_raw.csv"

TIER_RANK = {"Elite Membership": 2, "Ordinary Member": 1, "Associate Member": 0}


def accreditation_rank(value):
    """Accreditation values in this dataset are messy and sometimes combined
    (e.g. "JCI, MSQH", "MSQH, QTAC", "RTAC" with no "Accredited" suffix), so
    rank by presence of each accreditation body rather than exact match."""
    if pd.isna(value):
        return 0
    v = str(value).lower()
    if "jci" in v:
        return 3
    if "msqh" in v:
        return 2
    if "rtac" in v or "qtac" in v:
        return 1
    return 0

# WP Kuala Lumpur/Putrajaya sits inside Selangor geographically, so for
# recovery-destination matching purposes treat it as Selangor.
STATE_ALIAS = {"Wilayah Persekutuan": "Selangor"}


@st.cache_data
def load_hospitals():
    df = pd.read_csv(DATA_PATH)
    df["category"] = df["specialist"].apply(normalize_specialist)

    def agg(group):
        first = group.iloc[0]
        cats = sorted(set(c for c in group["category"] if pd.notna(c)))
        raw_specs = sorted(set(s for s in group["specialist"] if pd.notna(s)))
        return pd.Series({
            "State": first["State"],
            "Hospital_Type": first["Hospital_Type"],
            "Membership_Tier": first["Membership_Tier"],
            "Accreditation": first["Accreditation"],
            "Languages_Spoken": first["Languages_Spoken"],
            "International_Patient_Services": first["International_Patient_Services"],
            "Website_URL": first["Website_URL"],
            "Latitude": first["Latitude"],
            "Longitude": first["Longitude"],
            "categories": cats,
            "raw_specialists": raw_specs,
        })

    hosp = df.groupby("Hospital_Name").apply(agg, include_groups=False).reset_index()
    hosp["has_specialty_listed"] = hosp["categories"].apply(lambda c: len(c) > 0)
    return hosp


def rank_score(row):
    """Simple, transparent sort: accreditation level, then membership tier.
    Not a validated scoring model - just orders results so accredited /
    Elite-tier hospitals surface first."""
    return (
        accreditation_rank(row["Accreditation"]),
        TIER_RANK.get(row["Membership_Tier"], 0),
    )


def styled_box(text, icon="", bg="#0e4c5c", color="lightgray"):
    """Replacement for st.info/st.success/st.warning with a fixed, readable
    text color instead of Streamlit's theme-dependent default. Supports
    **bold** markdown (converted to <strong> manually, since markdown syntax
    inside a raw HTML div isn't reliably parsed by st.markdown)."""
    html_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    prefix = f"{icon} " if icon else ""
    st.markdown(
        f"<div style='background-color:{bg}; padding:0.75rem 1rem; "
        f"border-radius:0.5rem; color:{color};'>{prefix}{html_text}</div>",
        unsafe_allow_html=True,
    )
