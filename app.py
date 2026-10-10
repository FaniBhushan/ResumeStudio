from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Resume Studio", page_icon=":material/description:", layout="wide")
st.html(
    """<style>
    [data-testid="stSidebar"] .st-key-resume_studio_logo {
      transform: translateY(-4rem);
      margin-bottom: -4rem;
    }
    </style>"""
)
with st.sidebar.container(key="resume_studio_logo"):
    st.image(str(ROOT / "assets" / "resume-studio-logo.svg"), width=260)

page = st.navigation(
    [
        st.Page("app_pages/cv_builder.py", title="CV Builder", icon=":material/description:"),
        st.Page("app_pages/cover_letter.py", title="Cover Letter", icon=":material/draft:"),
    ],
    position="top",
)
page.run()
