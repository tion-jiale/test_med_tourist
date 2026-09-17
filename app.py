import streamlit as st

from shared import load_hospitals

st.set_page_config(
    page_title="Malaysia Medical Tourism",
    layout="wide",
    page_icon="🏥",
)

hosp_df = load_hospitals()

st.title("🏥 Malaysia Medical Tourism")
st.markdown(
    "This app has two parts — use the sidebar, or the links below, to get started."
)

col1, col2 = st.columns(2)
with col1:
    st.subheader("1. Hospital Recommendation")
    st.write(
        "Choose the specialist you're going for and filter by state, "
        "accreditation, and international patient services."
    )
    st.page_link("1_Hospital_Recommendation.py", label="Go to Hospital Recommendation", icon="🏥")
with col2:
    st.subheader("2. Recovery Plan")
    st.write(
        "Plan where to recover: close to the hospital for major surgery, "
        "or somewhere rural and scenic for minor procedures or mental-health/wellness care."
    )
    st.page_link("2_Recovery_Plan.py", label="Go to Recovery Plan", icon="🌿")

st.markdown("---")
st.caption(
    f"Built from the uploaded hospital dataset — {len(hosp_df)} hospitals, "
    f"{hosp_df['has_specialty_listed'].sum()} with a specialty listed."
)

