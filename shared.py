from pathlib import Path

import pandas as pd
import streamlit as st

from specialist_mapping import normalize_specialist

# Resolved from this file's own location (not the caller's), so it works
# correctly whether imported from app.py or from pages/*.py.
APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR / "hospitals_raw.csv"

ACCRED_RANK = {"JCI Accredited": 3, "MSQH Accredited": 2, "RTAC Accredited": 1}
TIER_RANK = {"Elite Membership": 2, "Ordinary Member": 1, "Associate Member": 0}

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
        ACCRED_RANK.get(row["Accreditation"], 0),
        TIER_RANK.get(row["Membership_Tier"], 0),
    )
