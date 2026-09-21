"""Project introduction page. Save as pages/0_Introduction.py."""
import streamlit as st

from shared import GROUP_NAME, PROJECT_TITLE, render_sidebar

st.set_page_config(page_title="Introduction", page_icon="📖", layout="wide")
render_sidebar()

# ---- Fill these in ----------------------------------------------------------
TEAM_MEMBERS = ["Shaza Nurayuni binti Shamsul Anuar", "Tion Jia Le", "Yip Yoong Eng", "Ain Mardhiah binti Abdul Hamid]
# -----------------------------------------------------------------------------

st.title(PROJECT_TITLE)
st.caption(f"Group: {GROUP_NAME}")

st.header("Background")
st.markdown(
    """
Malaysia is a leading destination for health travel, and Indonesia is by far the
largest source market (roughly 70-80% of health tourists). Most of this activity
is concentrated around a few urban hospital hubs, while many rural regions see
little of the economic benefit.
"""
)

st.header("What this app does")
c1, c2 = st.columns(2)
with c1:
    st.subheader("1. Hospital Recommendation")
    st.markdown(
        "Ranks hospitals by specialty and state with a rule-based approach, using "
        "accreditation, membership tier and international patient services."
    )
with c2:
    st.subheader("2. Recovery Plan")
    st.markdown(
        "Takes the chosen hospital and treatment and suggests where the patient can "
        "recover. Major surgery keeps patients close to the treating hospital for "
        "follow-up, while minor procedures and wellness stays can move to rural "
        "destinations."
    )

st.header("Data and method")
st.markdown(
    """
- **Hospital data:** a real dataset of 91 hospitals with coordinates, accreditation,
  membership tier, specialist listings and international patient service details.
- **Public sources for the wider study:** MHTC, OpenDOSM, KKMNOW (MOH data
  catalogue), data.gov.my and Tourism Malaysia.
- **Curated / heuristic layers:** specialist names are normalised into 27 categories,
  treatment intensity per specialty is a heuristic default, and the 14 rural
  destinations are hand-curated and matched to hospital states.
"""
)


st.header("Team")
st.markdown("\n".join(f"- {name}" for name in TEAM_MEMBERS))
