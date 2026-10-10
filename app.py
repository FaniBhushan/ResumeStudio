from pathlib import Path
import shutil

import streamlit as st

from src.cv_builder.storage import DATA_OUTPUT, RESUME_OUTPUT


ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Resume Studio", page_icon=":material/description:", layout="wide")
host = st.context.headers.get("host", "").split(":", 1)[0].casefold()
IS_STREAMLIT_CLOUD = host.endswith(".streamlit.app")


@st.cache_resource(show_spinner=False)
def clear_legacy_cloud_files() -> bool:
    """Remove shared files left by older cloud deployments, once per process."""
    for directory in (DATA_OUTPUT, RESUME_OUTPUT):
        if directory.exists():
            shutil.rmtree(directory)
    return True


if IS_STREAMLIT_CLOUD:
    clear_legacy_cloud_files()

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
