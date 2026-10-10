from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import streamlit as st
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cv_builder.importing import extract_cv_text, extract_job_description
from cv_builder.processes import generate_cover_letter
from cv_builder.storage import DATA_OUTPUT, slugify, write_text_atomic
from cv_builder.ui import select_ai_provider


_wide_inputs = (
    st.session_state.get("cover_letter_source_mode") == "Blank from description"
    and st.session_state.get("cover_letter_use_job_description", False)
)
_sidebar_width = 520 if _wide_inputs else 420
st.html(
    f"""<style>
    section[data-testid="stSidebar"] {{
      width: {_sidebar_width}px !important;
      min-width: {_sidebar_width}px !important;
    }}
    @media (max-width: 768px) {{
      section[data-testid="stSidebar"] {{
        width: min(88vw, {_sidebar_width}px) !important;
        min-width: min(88vw, {_sidebar_width}px) !important;
      }}
    }}
    </style>"""
)

st.title("Cover Letter")
st.caption("Create an editable, job-specific letter from your CV or your own career notes.")

with st.sidebar:
    st.subheader("Cover letter source", icon=":material/description:")
    select_ai_provider()
    source_mode = st.selectbox(
        "Start with",
        ["Existing CV", "Blank from description"],
        key="cover_letter_source_mode",
    )

    cv_upload = None
    user_description = ""
    if source_mode == "Existing CV":
        cv_upload = st.file_uploader(
            "Load an existing CV",
            type=["pdf", "yaml", "yml", "docx", "txt"],
            max_upload_size=20,
            key="cover_letter_cv_upload",
            help="Use a text-based PDF, RenderCV YAML, DOCX, or TXT file. Scanned PDFs are not supported.",
        )
    else:
        st.markdown(":material/person: **Describe your background and relevant experience**")
        user_description = st.text_area(
            "Describe your background and relevant experience", label_visibility="collapsed",
            key="cover_letter_user_description",
            height=110 if _wide_inputs else 180,
            max_chars=50_000,
            placeholder="Relevant experience, strengths, examples, and why this role interests you…",
            help="Use facts you can support. The draft will use only information you provide.",
        )

    st.divider()
    use_job_description = st.toggle(
        "Use a job description",
        value=False,
        key="cover_letter_use_job_description",
        help="Turn this on to tailor the letter to a specific job. When off, the job description is not used.",
    )
    job_description = ""
    if use_job_description:
        st.markdown(":material/work: **Job description**")
        jd_input_mode = st.segmented_control(
            "Job description input",
            ["Paste text", "Upload file"],
            default="Paste text",
            key="cover_letter_jd_input_mode",
            label_visibility="collapsed",
            width="stretch",
        )
        if jd_input_mode == "Upload file":
            cover_jd_file = st.file_uploader(
                "Load a job description",
                type=["pdf", "docx", "txt", "md"],
                max_upload_size=20,
                key="cover_letter_job_description_upload",
                help="Text-based PDF, DOCX, TXT, or Markdown.",
            )
            if st.button(
                "Load file text",
                key="load_cover_letter_job_description",
                disabled=cover_jd_file is None,
                width="stretch",
            ):
                try:
                    st.session_state["cover_letter_job_description"] = extract_job_description(
                        cover_jd_file.name, cover_jd_file.getvalue()
                    )
                    st.session_state["cover_letter_jd_input_mode"] = "Paste text"
                    st.session_state["_cover_jd_file_notice"] = (
                        f"Loaded job description from {cover_jd_file.name}. Review or edit it below."
                    )
                    st.rerun()
                except (OSError, ValueError) as exc:
                    st.error(str(exc))
        if notice := st.session_state.pop("_cover_jd_file_notice", None):
            st.success(notice)
        if jd_input_mode == "Paste text":
            job_description = st.text_area(
                "Paste or edit job description", label_visibility="collapsed",
                key="cover_letter_job_description",
                height=110 if _wide_inputs else 160,
                max_chars=50_000,
                placeholder="Paste the job posting here…",
            )
    cover_label = st.text_input(
        "Role or company",
        key="cover_letter_label",
        placeholder="e.g. Product Engineer — Acme",
        icon=":material/business_center:",
        help="Used as the saved Markdown file name.",
    )
    generate_clicked = st.button(
        "Generate cover letter",
        type="primary",
        key="generate_cover_letter",
        width="stretch",
    )

    if generate_clicked:
        try:
            cv_content = ""
            if source_mode == "Existing CV":
                if cv_upload is None:
                    raise ValueError("Upload an existing CV first.")
                suffix = Path(cv_upload.name).suffix.casefold()
                upload_bytes = cv_upload.getvalue()
                if suffix in {".yaml", ".yml"}:
                    document: Any = yaml.safe_load(upload_bytes)
                    if not isinstance(document, dict) or not isinstance(document.get("cv"), dict):
                        raise ValueError("This is not a valid RenderCV YAML document.")
                    cv_content = yaml.safe_dump(document, allow_unicode=True, sort_keys=False)
                else:
                    cv_content = extract_cv_text(cv_upload.name, upload_bytes)
            elif not user_description.strip():
                raise ValueError("Describe your background before generating a letter.")
            with st.spinner("Drafting your cover letter…"):
                letter = generate_cover_letter(
                    cv_content=cv_content,
                    user_description=user_description,
                    job_description=job_description,
                    provider=st.session_state.get("llm_provider", "Codex CLI"),
                )
            st.session_state["cover_letter_text"] = letter
            st.session_state["_cover_letter_notice"] = (
                "Draft created. Review and edit it before downloading or saving."
            )
            st.rerun()
        except (OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
            st.error(str(exc))

if notice := st.session_state.pop("_cover_letter_notice", None):
    st.success(notice)

st.markdown(":material/draft: **Cover letter draft**")
letter_text = st.text_area(
    "Cover letter draft", label_visibility="collapsed",
    key="cover_letter_text",
    height=560,
    placeholder="Your generated letter will appear here. You can also write or edit it directly.",
    help="Generate a draft using the inputs on the left, then edit it here before saving or downloading.",
)
filename = f"{slugify(cover_label, fallback='cover_letter')}.md"
with st.container(horizontal=True):
    st.download_button(
        "Download Markdown",
        data=letter_text,
        file_name=filename,
        mime="text/markdown",
        key="download_cover_letter",
        width="stretch",
        disabled=not letter_text.strip(),
    )
    if st.button(
        "Save cover letter",
        key="save_cover_letter",
        width="stretch",
        disabled=not letter_text.strip() or not cover_label.strip(),
    ):
        try:
            write_text_atomic(DATA_OUTPUT / "cover-letters" / filename, letter_text.rstrip() + "\n")
            st.success("Saved. Download it from CV Builder → Files → Markdown.")
        except OSError as exc:
            st.error(f"Could not save the cover letter: {exc}")
