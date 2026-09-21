from pathlib import Path
import re

import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

from specialist_mapping import normalize_specialist

PROJECT_TITLE = "Matching Care, Measuring Growth: AI-Powered Recommendation for Malaysia’s Medical Tourism"   # <- fill in
GROUP_NAME = "CODE RED"         # <- fill in

def render_sidebar():
    # Title above the page navigation (CSS pseudo-element on the nav container)
    st.markdown(
        "<style>[data-testid='stSidebarNav']::before {"
        f"content: '{PROJECT_TITLE}';"
        "display: block; font-size: 1.2rem; font-weight: 700;"
        "line-height: 1.3; padding: 1.25rem 1rem 0.5rem;}</style>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.divider()
        st.caption(f"Group: {GROUP_NAME}")
        st.markdown("**About this project**")
        st.markdown(
            "A feasibility study on using medical tourism to drive rural economic "
            "development in Malaysia. See the Introduction page for details."
        )
        st.caption(
            "Hospital data is real (91 hospitals). Specialty groupings, treatment "
            "intensity and rural destinations are curated or heuristic."
        )

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


def styled_box(text, icon="", bg="#007B8A", color="#F0F2F6"):
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


MAP_STYLE = "carto-positron"  # clean light basemap, independent of the app's own theme


def plot_hospitals_map(hosp_df, height=450, zoom=9):
    """Map of hospitals with hover details (name, state, accreditation,
    tier, top specialties) - replaces st.map's plain dots with a light-theme
    map the user can hover to read details, instead of guessing from a dot."""
    if hosp_df.empty:
        return
    df = hosp_df.copy()
    df["specialties_str"] = df["categories"].apply(
        lambda c: ", ".join(c[:4]) + (", …" if len(c) > 4 else "")
    )
    fig = px.scatter_mapbox(
        df, lat="Latitude", lon="Longitude",
        hover_name="Hospital_Name",
        hover_data={
            "State": True,
            "Accreditation": True,
            "Membership_Tier": True,
            "specialties_str": True,
            "Latitude": False,
            "Longitude": False,
        },
        labels={"specialties_str": "Specialties"},
        color_discrete_sequence=["#007B8A"],
        zoom=zoom,
        height=height,
    )
    fig.update_traces(marker=dict(size=14))
    fig.update_layout(mapbox_style=MAP_STYLE, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)


def plot_hospital_and_attractions_map(hospital_row, attractions_df, height=450, zoom=10):
    """Combined map: the hospital (larger, red marker) plus a set of
    attraction points (teal markers), each hoverable for details. Used on
    the Recovery Plan page so the hospital's location and the recommended
    spots are visible together, not as two separate maps.

    Built as a single go.Scattermapbox trace (not px with color=, which
    splits into multiple traces sharing one mapbox subplot - that combination
    was found to break tile rendering in this Streamlit/Plotly setup even
    though plot_hospitals_map's single-trace approach renders fine)."""
    accred = hospital_row.get("Accreditation")
    hosp_detail = hospital_row["State"]
    if pd.notna(accred):
        hosp_detail += f" · {accred}"

    names = [hospital_row["Hospital_Name"]]
    lats = [hospital_row["Latitude"]]
    lons = [hospital_row["Longitude"]]
    colors = ["#D62728"]
    sizes = [20]
    details = [f"Hospital · {hosp_detail}"]

    if attractions_df is not None and not attractions_df.empty:
        names += attractions_df["attraction_name"].tolist()
        lats += attractions_df["lat"].tolist()
        lons += attractions_df["lon"].tolist()
        colors += ["#007B8A"] * len(attractions_df)
        sizes += [11] * len(attractions_df)
        details += [
            f"Attraction · {cat} · {dist:.1f}km"
            for cat, dist in zip(attractions_df["category"], attractions_df["distance_km"])
        ]

    fig = go.Figure(go.Scattermapbox(
        lat=lats, lon=lons,
        mode="markers",
        marker=dict(size=sizes, color=colors),
        text=names,
        customdata=details,
        hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
    ))
    fig.update_layout(
        mapbox_style=MAP_STYLE,
        mapbox=dict(
            center=dict(lat=hospital_row["Latitude"], lon=hospital_row["Longitude"]),
            zoom=zoom,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=height,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
