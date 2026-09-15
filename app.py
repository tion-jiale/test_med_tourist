import streamlit as st
import pandas as pd
from specialist_mapping import normalize_specialist

st.set_page_config(
    page_title="Malaysia Medical Tourism — Hospital Recommender",
    layout="wide",
    page_icon="🏥",
)

ACCRED_RANK = {"JCI Accredited": 3, "MSQH Accredited": 2, "RTAC Accredited": 1}
TIER_RANK = {"Elite Membership": 2, "Ordinary Member": 1, "Associate Member": 0}


@st.cache_data
def load_data():
    df = pd.read_csv("data/hospitals_raw.csv")
    df["category"] = df["specialist"].apply(normalize_specialist)

    # One row per hospital, with all its specialties/categories collected into lists.
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


hosp_df = load_data()

ALL_CATEGORIES = sorted({c for cats in hosp_df["categories"] for c in cats})
ALL_STATES = sorted(hosp_df["State"].dropna().unique())


def rank_score(row):
    """Simple, transparent sort: accreditation level, then membership tier.
    Not a validated scoring model — just orders results so accredited /
    Elite-tier hospitals surface first."""
    return (
        ACCRED_RANK.get(row["Accreditation"], 0),
        TIER_RANK.get(row["Membership_Tier"], 0),
    )


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🏥 Malaysia Medical Tourism — Hospital Recommender")
st.caption(
    f"Built from {len(hosp_df)} hospitals in the uploaded dataset. "
    f"{hosp_df['has_specialty_listed'].sum()} of them have a specialty listed — "
    f"the other {(~hosp_df['has_specialty_listed']).sum()} have no specialty tag in the source "
    "data and won't appear in specialty-based results below."
)

# ---------------------------------------------------------------------------
# Step 1: choose specialist
# ---------------------------------------------------------------------------

st.markdown("### Step 1 — What specialist are you going for?")
specialty = st.selectbox(
    "Specialty", ALL_CATEGORIES, index=None, placeholder="Choose a specialty..."
)

if specialty is None:
    st.info("Pick a specialty above to see matching hospitals.")
    st.stop()

# ---------------------------------------------------------------------------
# Step 2: optional filters
# ---------------------------------------------------------------------------

st.markdown("### Step 2 — Narrow it down (optional)")
c1, c2, c3 = st.columns(3)
with c1:
    state_filter = st.multiselect("State", ALL_STATES)
with c2:
    accredited_only = st.checkbox("Accredited hospitals only (JCI / MSQH / RTAC)")
with c3:
    intl_services_only = st.checkbox("Has international patient services listed")

results = hosp_df[hosp_df["categories"].apply(lambda cats: specialty in cats)].copy()

if state_filter:
    results = results[results["State"].isin(state_filter)]
if accredited_only:
    results = results[results["Accreditation"].notna()]
if intl_services_only:
    results = results[results["International_Patient_Services"].notna()]

results["_score"] = results.apply(rank_score, axis=1)
results = results.sort_values("_score", ascending=False)

# ---------------------------------------------------------------------------
# Step 3: results
# ---------------------------------------------------------------------------

st.markdown("### Step 3 — Recommended hospitals")
st.caption(
    "Sorted by accreditation level (JCI > MSQH > RTAC) then membership tier "
    "(Elite > Ordinary > Associate) — a transparent sort on the data provided, not a validated ranking."
)

if results.empty:
    st.warning("No hospitals match this specialty with the current filters. Try loosening the filters.")
else:
    st.markdown(f"**{len(results)} hospital(s) found for {specialty}**")

    for _, row in results.iterrows():
        badges = []
        if row["Accreditation"]:
            badges.append(f"🏅 {row['Accreditation']}")
        if row["Membership_Tier"]:
            badges.append(f"⭐ {row['Membership_Tier']}")

        with st.container(border=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.subheader(row["Hospital_Name"])
                st.write(f"📍 {row['State']}" + (f" · {row['Hospital_Type']}" if pd.notna(row["Hospital_Type"]) else ""))
                if badges:
                    st.write(" &nbsp;·&nbsp; ".join(badges))
                st.write("**Specialties:** " + ", ".join(row["categories"]))
                if pd.notna(row["Languages_Spoken"]):
                    st.write(f"**Languages:** {row['Languages_Spoken']}")
                if pd.notna(row["International_Patient_Services"]):
                    st.write(f"**For international patients:** {row['International_Patient_Services']}")
                if pd.notna(row["Website_URL"]):
                    st.write(f"[Visit website]({row['Website_URL']})")
            with col_b:
                st.map(
                    pd.DataFrame({"lat": [row["Latitude"]], "lon": [row["Longitude"]]}),
                    latitude="lat", longitude="lon", size=30, zoom=9,
                )

    st.markdown("### All matching hospitals on one map")
    st.map(results, latitude="Latitude", longitude="Longitude", size=20)

with st.expander("About this data"):
    st.write(
        "Hospital names, states, coordinates, accreditation, membership tier, and specialty "
        "listings come directly from the uploaded dataset (`malaysia_hospitals_with_coords.csv`). "
        "Specialty labels were consolidated from the raw values in that file "
        "(e.g. 'ENT (Ear Nose Throat)' and 'Ear, Nose & Throat (ENT)' were merged into one "
        "'ENT' category) — see `specialist_mapping.py` for the exact mapping. Nothing about "
        "accreditation, membership tier, or specialties was invented or supplemented from outside "
        "the file."
    )
