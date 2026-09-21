import streamlit as st
import pandas as pd

from shared import load_hospitals
from specialty_severity import default_intensity
import attractions

st.set_page_config(page_title="Recovery Plan", layout="wide", page_icon="🌿")

hosp_df = load_hospitals()

st.title("🌿 Recovery Plan")
st.caption(
    "Major surgery usually means staying close to the hospital for follow-up visits. "
    "Minor procedures or mental-health/wellness care leave more room to choose — "
    "stay in the city, or go somewhere quieter and more scenic."
)

# ---------------------------------------------------------------------------
# Step 1: which hospital
# ---------------------------------------------------------------------------

st.markdown("### Step 1 — Which hospital are you planning around?")

carried_hospital = st.session_state.get("recovery_anchor_hospital")
carried_specialty = st.session_state.get("recovery_specialty")

all_hospital_names = hosp_df["Hospital_Name"].tolist()
default_idx = (
    all_hospital_names.index(carried_hospital)
    if carried_hospital in all_hospital_names
    else None
)

if carried_hospital:
    st.info(
        f"Carried over from Hospital Recommendation: **{carried_hospital}** "
        f"({carried_specialty}). Change it below if you'd like.",
        icon="↩️",
    )

anchor_hospital_name = st.selectbox(
    "Hospital", all_hospital_names, index=default_idx, placeholder="Choose a hospital..."
)

if anchor_hospital_name is None:
    st.markdown(
        "<div style='background-color:#0e4c5c; padding:0.75rem 1rem; "
        "border-radius:0.5rem; color:lightgray;'>"
        "Pick a hospital above to plan your recovery stay.</div>",
        unsafe_allow_html=True,
    )
    st.stop()

anchor = hosp_df[hosp_df["Hospital_Name"] == anchor_hospital_name].iloc[0]

# ---------------------------------------------------------------------------
# Step 2: treatment intensity
# ---------------------------------------------------------------------------

st.markdown("### Step 2 — What best describes your treatment?")

intensity_options = {
    "major": "Major surgery (e.g. cardiac, joint replacement, tumour removal) — needs close follow-up",
    "minor": "Minor / outpatient procedure (e.g. dental, screening, minor scope)",
    "mental_health": "Mental health or wellness-focused care",
}

if anchor_hospital_name == carried_hospital and carried_specialty:
    suggested = default_intensity(carried_specialty)
    help_text = (
        f"Pre-selected based on '{carried_specialty}' as a general rule of thumb — not "
        "medical advice. Please follow your doctor's actual aftercare guidance."
    )
else:
    suggested = "minor"
    help_text = (
        "No specialty context carried over, so this defaults to 'minor' — please pick "
        "what actually matches your treatment. Not medical advice."
    )

intensity = st.radio(
    "Treatment type",
    options=list(intensity_options.keys()),
    format_func=lambda k: intensity_options[k],
    index=list(intensity_options.keys()).index(suggested),
    help=help_text,
)

# ---------------------------------------------------------------------------
# Helpers: urban (near-hospital) and rural (candidate region) recommendations
# ---------------------------------------------------------------------------

def show_urban_recommendations(anchor, anchor_hospital_name):
    nearby = attractions.attractions_for_hospital(anchor_hospital_name)

    if nearby.empty:
        st.info(
            f"**Stay close to {anchor['Hospital_Name']} in {anchor['State']}.** "
            "No attraction data is available for this specific hospital yet "
            f"(only {len(attractions.hospitals_with_attraction_data())} of the 91 hospitals "
            "have nearby-attraction data so far) — for now, treat this as a reminder to "
            "book accommodation near the hospital, and confirm timing with the hospital's "
            "follow-up schedule if you have one.",
            icon="🏙️",
        )
        st.map(
            pd.DataFrame({"lat": [anchor["Latitude"]], "lon": [anchor["Longitude"]]}),
            latitude="lat", longitude="lon", zoom=10,
        )
        return

    st.success(
        f"**Staying near {anchor['Hospital_Name']} in {anchor['State']}.** "
        "Here are things nearby to pass the time "
        f"— all within {nearby['distance_km'].max():.0f}km of the hospital.",
        icon="🏙️",
    )
    available_cats = sorted(nearby["category"].unique())
    default_cats = [c for c in attractions.URBAN_DEFAULT_CATEGORIES if c in available_cats]
    cat_filter = st.multiselect(
        "Filter by type", available_cats, default=default_cats or available_cats[:5], key="urban_cat_filter"
    )
    shown = nearby[nearby["category"].isin(cat_filter)].sort_values("distance_km") if cat_filter else nearby.sort_values("distance_km")
    shown = shown.head(15)

    st.caption(f"Showing {len(shown)} of {len(nearby)} attractions within range, sorted by distance.")
    for _, row in shown.iterrows():
        st.write(f"**{row['attraction_name']}** — {row['category']} · {row['distance_km']:.1f}km away")
    if not shown.empty:
        st.map(shown, latitude="lat", longitude="lon", size=20)

    st.caption(
        "Attraction data sourced from OpenStreetMap (`attractions_near_hospitals.csv`) — "
        "real listed places, not curated or verified for accessibility/suitability."
    )


def show_rural_recommendations(anchor):
    ranked_regions = attractions.rural_regions_ranked_by_distance(
        anchor["Latitude"], anchor["Longitude"]
    )

    st.success(
        "**Recovering somewhere quieter.** "
        "Pick one of the project's candidate rural regions below — ranked by straight-line "
        f"distance from {anchor['Hospital_Name']}:",
        icon="🌿",
    )

    region_labels = [
        f"{row['label']} (≈{row['distance_km']:.0f}km away, {row['n_attractions']} attractions on file)"
        for _, row in ranked_regions.iterrows()
    ]
    region_codes = ranked_regions["reference_point"].tolist()

    chosen_idx = st.selectbox(
        "Rural region", range(len(region_codes)), format_func=lambda i: region_labels[i], key="rural_region_select"
    )
    chosen_region = region_codes[chosen_idx]

    region_attractions = attractions.attractions_for_region(chosen_region)
    available_cats = sorted(region_attractions["category"].unique())
    default_cats = [c for c in attractions.RURAL_DEFAULT_CATEGORIES if c in available_cats]
    cat_filter = st.multiselect(
        "Filter by type", available_cats, default=default_cats or available_cats[:5], key="rural_cat_filter"
    )
    shown = region_attractions[region_attractions["category"].isin(cat_filter)].sort_values("distance_km") if cat_filter else region_attractions.sort_values("distance_km")
    shown = shown.head(15)

    st.caption(f"Showing {len(shown)} of {len(region_attractions)} attractions in this region, sorted by distance from the region's reference point.")
    for _, row in shown.iterrows():
        st.write(f"**{row['attraction_name']}** — {row['category']} · {row['distance_km']:.1f}km from reference point")
    if not shown.empty:
        st.map(shown, latitude="lat", longitude="lon", size=20)

    st.caption(
        "Rural regions are the project's actual candidate sites (Sabah, Sarawak, Kelantan, "
        "Terengganu, Perak interior, Kedah, Melaka hinterland). Attractions sourced from "
        "OpenStreetMap (`attractions_rural_regions.csv`) — distance is straight-line from "
        "the hospital to each region's centroid, not driving distance or travel time."
    )


# ---------------------------------------------------------------------------
# Step 3: recommendation
# ---------------------------------------------------------------------------

st.markdown("### Step 3 — Where to recover")

if intensity == "major":
    st.caption(
        "Because this is major surgery, we're only showing options close to the hospital "
        "for easier follow-up — rural options aren't offered for this treatment type."
    )
    show_urban_recommendations(anchor, anchor_hospital_name)

else:
    location_choice = st.radio(
        "Where would you like to recover?",
        options=["urban", "rural"],
        format_func=lambda k: {
            "urban": "Stay in the city — near the hospital",
            "rural": "Go rural — quieter, scenic candidate region",
        }[k],
        horizontal=True,
    )

    if location_choice == "urban":
        show_urban_recommendations(anchor, anchor_hospital_name)
    else:
        show_rural_recommendations(anchor)
