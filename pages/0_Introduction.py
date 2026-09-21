"""Project introduction page. Save as pages/0_Introduction.py."""
import streamlit as st

from shared import GROUP_NAME, PROJECT_TITLE, render_sidebar

st.set_page_config(page_title="Introduction", page_icon="📖", layout="wide")
render_sidebar()

# ---- Fill these in ----------------------------------------------------------
TEAM_MEMBERS = ["Shaza Nurayuni binti Shamsul Anuar", "Tion Jia Le", "Yip Yoong Eng", "Ain Mardhiah binti Abdul Hamid"]
# -----------------------------------------------------------------------------

st.title(PROJECT_TITLE)
st.caption(f"Group: {GROUP_NAME}")

st.header("Background")
st.markdown(
    """
Malaysia has become one of Southeast Asia's fastest-growing medical tourism hubs, drawing patients with low-cost, 
high-quality care and English-speaking doctors, and welcoming nearly 38 million foreign visitors in 2024, up 31.1% from 2023. 
The industry took shape after the 1998 formation of the National Committee for the Promotion of Health Tourism, which 
brought together government and private hospital bodies, and it received dedicated budget support from the Eighth Malaysia Plan onward, 
along with facilitation measures such as immigration Green Lanes. Foreign patient numbers rose from 75,210 in 2001 to 296,687 in 2006, 
generating RM203 million in revenue, and later growth was supported by international accreditation (such as JCI) and investment in specialized centers for cardiology, oncology, fertility, and orthopedics. 
However, this growth has been concentrated in a few well-known hospitals and hubs, while equally capable hospitals elsewhere struggle to attract medical tourists. 
Patients tend to choose based on informal recommendations and reputation rather than objective assessments of capability, which creates a cycle where already visible hospitals stay dominant. 
With tax policy and cost structures also becoming more complex, the document concludes that Malaysia lacks a centralized, 
data-driven mechanism for identifying and communicating hospital-level treatment capabilities across states, 
which limits efficient matching between patients and suitable hospitals.
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
