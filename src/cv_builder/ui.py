from __future__ import annotations

import streamlit as st

from .processes import LLM_PROVIDERS


def _remember_ai_provider() -> None:
    st.session_state["_selected_ai_provider"] = st.session_state["llm_provider"]


def select_ai_provider() -> str:
    """Render the provider selector and persist its value across Streamlit pages."""
    selected = st.session_state.get("_selected_ai_provider", "Codex CLI")
    st.session_state["llm_provider"] = selected
    st.selectbox(
        "AI provider",
        LLM_PROVIDERS,
        key="llm_provider",
        on_change=_remember_ai_provider,
        help="Uses the selected provider's locally installed CLI and your existing sign-in or subscription.",
    )
    return str(st.session_state.get("_selected_ai_provider", selected))
