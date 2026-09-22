import streamlit as st
import streamlit.components.v1 as components

from shared import styled_box

st.set_page_config(
    page_title="Tourist Analysis Dashboard",
    layout="wide",
    page_icon="📊"
)

st.title("Tourist Analysis Dashboard")
st.caption("created by CODE RED")

POWER_BI_EMBED_URL = (
    "https://app.powerbi.com/links/jWvHi_JUcY?ctid=7f048fc1-2ea3-48e4-ac92-91d1eb09807c&pbi_source=linkShare&bookmarkGuid=ac8c7c64-a6cc-4a1e-8b92-0d013c7873ab"
)

components.iframe(
    POWER_BI_EMBED_URL,
    height=800,
    scrolling=False
)
