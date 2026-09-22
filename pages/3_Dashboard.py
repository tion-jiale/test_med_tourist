import streamlit as st
import streamlit.components.v1 as components

from shared import styled_box

st.set_page_config(
    page_title="Tourist Analysis Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("📊 Tourist Analysis Dashboard")
st.caption("CODE RED DASHBOARD")

POWER_BI_EMBED_URL = (
    "https://app.powerbi.com/reportEmbed"
    "?reportId=91d9806a-b675-4c8f-aceb-d17c794ac5a5"
    "&autoAuth=true"
    "&ctid=7f048fc1-2ea3-48e4-ac92-91d1eb09807c"
)

components.iframe(
    POWER_BI_EMBED_URL,
    height=800,
    scrolling=False
)
