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
    "https://app.powerbi.com/view?r=eyJrIjoiYTZlYjczNTAtNDc0MC00NTY3LWJkNzgtYjkxN2YxYWNkNWJjIiwidCI6IjdmMDQ4ZmMxLTJlYTMtNDhlNC1hYzkyLTkxZDFlYjA5ODA3YyIsImMiOjEwfQ%3D%3D"
)

components.iframe(
    POWER_BI_EMBED_URL,
    height=700,
    scrolling=False
)
