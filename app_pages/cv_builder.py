from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

import streamlit as st
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cv_builder.importing import extract_cv_text, extract_job_description
from cv_builder.processes import (
    categorize_achievements,
    extract_cv_fields,
    refine_text,
    render_cv,
    review_ats_alignment,
)
from cv_builder.storage import (
    DATA_OUTPUT,
    RESUME_OUTPUT,
    STARTER_YAML,
    dump_yaml_atomic,
    load_yaml,
    save_markdown,
    slugify,
)
from cv_builder.ui import select_ai_provider
from cv_builder.validation import date_format_error, email_format_error, links_format_error, phone_format_error


ACHIEVEMENT_CATEGORIES = {
    "Technical": "technical_achievements",
    "Leadership": "leadership_achievements",
    "Product": "product_achievements",
}
SUPPORTED_NETWORKS = {
    name.casefold(): name for name in (
        "LinkedIn", "GitHub", "GitLab", "IMDB", "Instagram", "ORCID", "Mastodon",
        "StackOverflow", "ResearchGate", "YouTube", "Google Scholar", "Telegram",
        "WhatsApp", "Leetcode", "X", "Bluesky", "Reddit",
    )
}
RENDERCV_THEMES = [
    "classic", "ember", "engineeringclassic", "engineeringresumes", "harvard",
    "ink", "moderncv", "opal", "sb2nov",
]
RENDERCV_THEME_LABELS = {
    "classic": "Classic",
    "ember": "Ember",
    "engineeringclassic": "Engineering Classic",
    "engineeringresumes": "Engineering Resumes",
    "harvard": "Harvard",
    "ink": "Ink",
    "moderncv": "ModernCV",
    "opal": "Opal",
    "sb2nov": "SB2Nov",
}
IS_STREAMLIT_CLOUD = st.context.headers.get("host", "").split(":", 1)[0].casefold().endswith(".streamlit.app")


def strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result = []
        for item in value:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                for key in ("bullet", "text", "summary"):
                    if isinstance(item.get(key), str):
                        result.append(item[key])
                        break
        return result
    return []


def icon_text_area(label: str, icon: str, **kwargs: Any) -> Any:
    st.markdown(f":material/{icon}: **{label}**")
    return st.text_area(label, label_visibility="collapsed", **kwargs)


def split_lines(value: str) -> list[str]:
    return [line.strip().lstrip("-• ").strip() for line in value.splitlines() if line.strip()]


def load_editor_state(document: dict[str, Any], source_path: str) -> None:
    cv = document.get("cv", {})
    sections = cv.get("sections", {})
    photo_value = str(cv.get("photo", ""))
    photo_path = Path(photo_value) if photo_value else Path()
    if photo_value and not photo_path.is_absolute() and Path(source_path).is_file():
        photo_path = Path(source_path).resolve().parent / photo_path
    st.session_state["_base_document"] = copy.deepcopy(document)
    st.session_state["_source_path"] = source_path
    profile = {
        "name": cv.get("name", ""),
        "location": cv.get("location", ""),
        "email": cv.get("email", ""),
        "phone": cv.get("phone", ""),
        "photo_path": str(photo_path.resolve()) if photo_value and photo_path.is_file() else "",
        "summary": "\n".join(strings(sections.get("professional_summary", []))),
    }
    links = cv.get("social_networks", [])
    link_lines = [
        f"{item.get('network', 'Link')}: {item.get('username', item.get('url', ''))}"
        for item in links if isinstance(item, dict)
    ]
    websites = cv.get("website", [])
    if isinstance(websites, str):
        websites = [websites]
    link_lines += [f"Website: {url}" for url in websites]
    profile["links"] = "\n".join(link_lines)
    profile["skills"] = "\n".join(
        f"{item.get('label', 'Skills')} | {item.get('details', '')}"
        for item in sections.get("skills", []) if isinstance(item, dict)
    )
    for key, value in profile.items():
        st.session_state[f"profile_{key}"] = value

    role_ids = []
    for index, entry in enumerate(sections.get("experience", [])):
        if not isinstance(entry, dict):
            continue
        role_id = index + 1
        role_ids.append(role_id)
        for key, value in {
            "company": entry.get("company", ""),
            "position": entry.get("position", ""),
            "start": entry.get("start_date", ""),
            "end": entry.get("end_date", ""),
            "location": entry.get("location", ""),
            "summary": entry.get("summary", ""),
            "highlights": "\n".join(strings(entry.get("highlights", []))),
        }.items():
            st.session_state[f"role_{role_id}_{key}"] = str(value)
    if not role_ids:
        role_ids = [1]
        for key in ("company", "position", "start", "end", "location", "summary", "highlights"):
            st.session_state[f"role_1_{key}"] = ""
    st.session_state["_role_ids"] = role_ids
    st.session_state["_next_role_id"] = max(role_ids, default=0) + 1

    categorized_achievements = {
        label: strings(sections.get(section_key, []))
        for label, section_key in ACHIEVEMENT_CATEGORIES.items()
    }
    achievements_text = "\n".join(
        item for label in ACHIEVEMENT_CATEGORIES for item in categorized_achievements[label]
    )
    st.session_state["section_all_achievements"] = achievements_text
    st.session_state["_categorized_achievements"] = categorized_achievements
    st.session_state["_categorized_achievements_source"] = achievements_text
    st.session_state.pop("_achievement_categorization_proposal", None)
    st.session_state.pop("_achievement_categorization_source", None)
    st.session_state["section_education"] = "\n".join(
        " | ".join(str(item.get(key, "")) for key in ("institution", "degree", "area", "start_date", "end_date", "location"))
        for item in sections.get("education", []) if isinstance(item, dict)
    )
    st.session_state["section_certifications"] = "\n".join(strings(sections.get("certifications", [])))
    st.session_state["section_languages"] = "\n".join(
        f"{item.get('label', '')} | {item.get('details', '')}"
        for item in sections.get("languages", []) if isinstance(item, dict)
    )
    st.session_state.pop("_suggestion", None)
    st.session_state["_pdf_path"] = ""
    st.session_state["selected_template"] = None
    st.session_state.pop("_template_preview_path", None)
    st.session_state.pop("_template_preview_key", None)
    st.session_state.pop("_template_preview_draft_hash", None)


def imported_fields_document(fields: dict[str, Any]) -> dict[str, Any]:
    """Translate the importer's normalized result into the editor's CV model."""
    cv: dict[str, Any] = {}
    for key in ("name", "location", "email", "phone"):
        value = fields.get(key, "")
        if isinstance(value, str) and value.strip():
            cv[key] = value.strip()
    networks = fields.get("social_networks", [])
    if isinstance(networks, list) and networks:
        cv["social_networks"] = networks
    websites = fields.get("websites", [])
    if isinstance(websites, list) and websites:
        cv["website"] = websites

    sections: dict[str, Any] = {}
    summary = fields.get("summary", "")
    if isinstance(summary, str) and summary.strip():
        sections["professional_summary"] = summary.strip()
    for key in ("skills", "experience", "technical_achievements", "leadership_achievements",
                "product_achievements", "education", "certifications", "languages"):
        value = fields.get(key, [])
        if isinstance(value, list) and value:
            sections[key] = value
    if sections:
        cv["sections"] = sections
    return {
        "cv": cv,
        "design": copy.deepcopy(st.session_state.get("_base_document", {}).get("design", {"theme": "classic"})),
        "locale": copy.deepcopy(st.session_state.get("_base_document", {}).get("locale", {})),
        "settings": copy.deepcopy(st.session_state.get("_base_document", {}).get("settings", {})),
    }


def initialize() -> None:
    if "_base_document" not in st.session_state:
        # A hosted Streamlit process may retain files from an earlier
        # deployment, and its filesystem is shared by app sessions. Never
        # make a saved CV the default for a new session; require users to
        # load their own CV explicitly through the uploader.
        load_editor_state(load_yaml(STARTER_YAML), str(STARTER_YAML))
    remove_id = st.session_state.pop("_remove_role_next", None)
    if remove_id is not None:
        ids = st.session_state.get("_role_ids", [])
        st.session_state["_role_ids"] = [item for item in ids if item != remove_id]
        for key in list(st.session_state.keys()):
            if key.startswith(f"role_{remove_id}_"):
                del st.session_state[key]
    apply = st.session_state.pop("_apply_suggestion_next", None)
    if apply:
        st.session_state[apply["key"]] = apply["text"]
        st.session_state.pop("_suggestion", None)


def current_profile() -> dict[str, str]:
    return {key: str(st.session_state.get(f"profile_{key}", "")) for key in
            ("name", "location", "email", "phone", "photo_path", "links", "summary", "skills")}


def current_roles() -> list[dict[str, str]]:
    roles = []
    for role_id in st.session_state.get("_role_ids", []):
        role = {key: str(st.session_state.get(f"role_{role_id}_{key}", "")) for key in
                ("company", "position", "start", "end", "location", "summary", "highlights")}
        role["dates"] = " – ".join(part for part in (role["start"], role["end"]) if part)
        roles.append(role)
    return roles


def draft_hash() -> str:
    state = {
        "profile": current_profile(),
        "roles": current_roles(),
        "achievements": st.session_state.get("section_all_achievements", ""),
        "achievement_categories": st.session_state.get("_categorized_achievements", {}),
        "education": st.session_state.get("section_education", ""),
        "certifications": st.session_state.get("section_certifications", ""),
        "languages": st.session_state.get("section_languages", ""),
    }
    return hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def parse_links(text: str) -> tuple[list[dict[str, str]], list[str]]:
    social_networks: list[dict[str, str]] = []
    websites: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if ":" in line:
            network, username = (part.strip() for part in line.split(":", 1))
            if network.casefold() in {"website", "url", "portfolio"}:
                url = username
                if url and not url.startswith(("https://", "http://")):
                    url = f"https://{url}"
                if url:
                    websites.append(url)
            elif network.casefold() in SUPPORTED_NETWORKS:
                social_networks.append({"network": SUPPORTED_NETWORKS[network.casefold()], "username": username})
            else:
                raise ValueError(f"Unsupported social network '{network}'. Use a supported network name or Website: URL.")
        else:
            url = line.strip()
            if not url.startswith(("https://", "http://")):
                url = f"https://{url}"
            websites.append(url)
    return social_networks, websites


def pair_entries(text: str, keys: tuple[str, str]) -> list[dict[str, str]]:
    entries = []
    for line in split_lines(text):
        if "|" in line:
            first, second = line.split("|", 1)
            entries.append({keys[0]: first.strip(), keys[1]: second.strip()})
    return entries


def make_document() -> tuple[dict[str, Any], dict[str, str]]:
    base = copy.deepcopy(st.session_state["_base_document"])
    selected_theme = st.session_state.get("selected_template")
    if selected_theme:
        base["design"] = {"theme": selected_theme}
    profile = current_profile()
    if not profile["name"].strip():
        raise ValueError("Please enter a name before saving the CV.")
    roles = current_roles()
    cv = base.setdefault("cv", {})
    for key in ("name", "location", "email", "phone"):
        if profile[key].strip():
            cv[key] = profile[key].strip()
        else:
            cv.pop(key, None)
    photo_path = str(st.session_state.get("profile_photo_path", "")).strip()
    if photo_path:
        cv["photo"] = os.path.relpath(Path(photo_path), RESUME_OUTPUT)
    else:
        cv.pop("photo", None)
    parsed_networks, websites = parse_links(profile["links"])
    if parsed_networks:
        cv["social_networks"] = parsed_networks
    else:
        cv.pop("social_networks", None)
    if websites:
        cv["website"] = websites
    else:
        cv.pop("website", None)
    sections = cv.setdefault("sections", {})
    summary = split_lines(profile["summary"])
    if summary:
        sections["professional_summary"] = summary
    else:
        sections.pop("professional_summary", None)
    sections["experience"] = []
    for role in roles:
        if not (role["company"].strip() and role["position"].strip()):
            continue
        item: dict[str, Any] = {"company": role["company"].strip(), "position": role["position"].strip()}
        for key, source in (("start_date", "start"), ("end_date", "end"), ("location", "location"), ("summary", "summary")):
            if role[source].strip():
                item[key] = role[source].strip()
        item["highlights"] = split_lines(role["highlights"])
        sections["experience"].append(item)
    if not sections["experience"]:
        sections.pop("experience", None)

    achievement_text = str(st.session_state.get("section_all_achievements", ""))
    if achievement_text.strip():
        if achievement_text != st.session_state.get("_categorized_achievements_source", ""):
            raise ValueError("Categorize and review the achievements before saving.")
        categorized = st.session_state.get("_categorized_achievements", {})
        achievements = {
            label: "\n".join(categorized.get(label, []))
            for label in ACHIEVEMENT_CATEGORIES
        }
    else:
        achievements = {label: "" for label in ACHIEVEMENT_CATEGORIES}
    for label, section_key in ACHIEVEMENT_CATEGORIES.items():
        values = split_lines(achievements[label])
        if values:
            sections[section_key] = values
        else:
            sections.pop(section_key, None)
    education = []
    for line in split_lines(str(st.session_state.get("section_education", ""))):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) >= 2:
            fields = ("institution", "degree", "area", "start_date", "end_date", "location")
            education.append({key: value for key, value in zip(fields, parts) if value})
    if education:
        sections["education"] = education
    else:
        sections.pop("education", None)
    certifications = split_lines(str(st.session_state.get("section_certifications", "")))
    if certifications:
        sections["certifications"] = [{"bullet": item} for item in certifications]
    else:
        sections.pop("certifications", None)
    skills = []
    for line in split_lines(profile["skills"]):
        if "|" in line:
            label, details = line.split("|", 1)
            skills.append({"label": label.strip(), "details": details.strip()})
    if skills:
        sections["skills"] = skills
    else:
        sections.pop("skills", None)
    languages = pair_entries(str(st.session_state.get("section_languages", "")), ("label", "details"))
    if languages:
        sections["languages"] = languages
    else:
        sections.pop("languages", None)
    if not sections:
        cv.pop("sections", None)

    slug = slugify(profile["name"] or "my_cv")
    render_folder = f"{slug}_rendercv_output"
    render_settings = base.setdefault("settings", {}).setdefault("render_command", {})
    render_settings["output_folder"] = render_folder
    for artifact, extension in (("pdf_path", "pdf"), ("markdown_path", "md"), ("html_path", "html"), ("typst_path", "typ"), ("png_path", "png")):
        render_settings[artifact] = f"OUTPUT_FOLDER/{slug}_CV.{extension}"
    render_settings["dont_generate_pdf"] = False
    render_settings["dont_generate_png"] = False
    return base, achievements


def save_current() -> tuple[Path, dict[str, Any], dict[str, str]]:
    document, achievements = make_document()
    profile = current_profile()
    slug = slugify(profile["name"] or "my_cv")
    yaml_path = RESUME_OUTPUT / f"{slug}_CV.yaml"
    dump_yaml_atomic(yaml_path, document)
    save_markdown(profile, current_roles(), achievements, document.get("cv", {}).get("sections", {}))
    st.session_state["_saved_yaml"] = str(yaml_path)
    return yaml_path, document, achievements


def active_job_description() -> str:
    if not st.session_state.get("ats_mode", False):
        return ""
    return str(st.session_state.get("ats_job_description", "")).strip()


def refinement_disabled(text: str) -> bool:
    return not text.strip() or (st.session_state.get("ats_mode", False) and not active_job_description())


def validate_form_fields() -> list[str]:
    errors: list[str] = []
    profile = current_profile()
    for label, error in (
        ("Email", email_format_error(profile["email"])),
        ("Phone", phone_format_error(profile["phone"])),
        ("Links", links_format_error(profile["links"])),
    ):
        if error:
            errors.append(f"{label}: {error}")
    for role_id in st.session_state.get("_role_ids", []):
        start = str(st.session_state.get(f"role_{role_id}_start", ""))
        end = str(st.session_state.get(f"role_{role_id}_end", ""))
        start_error = date_format_error(start)
        end_error = date_format_error(end, end_date=True)
        label = str(st.session_state.get(f"role_{role_id}_position", "")).strip() or "Experience"
        if start_error:
            errors.append(f"{label} — start date: {start_error}")
        if end_error:
            errors.append(f"{label} — end date: {end_error}")
        if not start_error and not end_error and start and end and end.casefold() not in {"present", "current"} and end < start:
            errors.append(f"{label}: end date must be the same as or later than the start date.")
    for index, line in enumerate(split_lines(str(st.session_state.get("section_education", ""))), start=1):
        parts = [part.strip() for part in line.split("|")]
        start = parts[3] if len(parts) > 3 else ""
        end = parts[4] if len(parts) > 4 else ""
        start_error = date_format_error(start)
        end_error = date_format_error(end, end_date=True)
        if start_error:
            errors.append(f"Education entry {index} — start date: {start_error}")
        if end_error:
            errors.append(f"Education entry {index} — end date: {end_error}")
        if not start_error and not end_error and start and end and end.casefold() not in {"present", "current"} and end < start:
            errors.append(f"Education entry {index}: end date must be the same as or later than the start date.")
    try:
        parse_links(profile["links"])
    except ValueError as exc:
        errors.append(f"Links: {exc}")
    return errors


def current_cv_content() -> dict[str, Any]:
    profile = current_profile()
    roles = current_roles()
    categorized = st.session_state.get("_categorized_achievements", {})
    return {
        "name": profile["name"],
        "summary": profile["summary"],
        "skills": profile["skills"],
        "experience": [
            {key: role[key] for key in ("company", "position", "start", "end", "location", "summary", "highlights")}
            for role in roles if role["company"].strip() or role["position"].strip() or role["highlights"].strip()
        ],
        "achievements": {
            label: categorized.get(label, []) for label in ACHIEVEMENT_CATEGORIES
        } if str(st.session_state.get("section_all_achievements", "")) == st.session_state.get("_categorized_achievements_source", "") else {
            "uncategorized": str(st.session_state.get("section_all_achievements", ""))
        },
        "education": str(st.session_state.get("section_education", "")),
        "certifications": str(st.session_state.get("section_certifications", "")),
        "languages": str(st.session_state.get("section_languages", "")),
    }


def ats_review_key() -> str:
    source = {"draft": draft_hash(), "job_description": active_job_description()}
    return hashlib.sha256(json.dumps(source, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def render_template_preview(theme: str) -> Path:
    # Keep template browsing independent of user content and incomplete fields.
    starter = load_yaml(STARTER_YAML)
    document = {
        "cv": {
            "name": "Alex Morgan",
            "location": "Berlin, Germany",
            "email": "alex.morgan@example.com",
            "phone": "+493012345678",
            "website": ["https://alexmorgan.example"],
            "social_networks": [
                {"network": "LinkedIn", "username": "alex-morgan"},
                {"network": "GitHub", "username": "alexmorgan"},
            ],
            "sections": {
                "professional_summary": [
                    "Product-minded software engineer with 8 years of experience building reliable, user-focused platforms."
                ],
                "education": [
                    {
                        "institution": "Technical University of Berlin", "area": "Computer Science",
                        "degree": "M.Sc.", "start_date": "2014-09", "end_date": "2016-06",
                        "location": "Berlin, Germany",
                        "highlights": ["Thesis: Reliable event-driven systems at scale", "Graduated with distinction"],
                    },
                    {
                        "institution": "University of Bremen", "area": "Software Systems",
                        "degree": "B.Sc.", "start_date": "2011-09", "end_date": "2014-06",
                        "location": "Bremen, Germany",
                    },
                ],
                "experience": [
                    {
                        "company": "Northstar Labs", "position": "Senior Software Engineer",
                        "start_date": "2021-04", "end_date": "present", "location": "Berlin, Germany",
                        "highlights": [
                            "Led a platform modernization that reduced deployment time by 40% and improved release reliability.",
                            "Partnered with product and design to launch workflows used by more than 20,000 customers.",
                            "Designed event-driven services processing 2 million requests each month.",
                            "Mentored five engineers and introduced practices adopted across three product teams.",
                        ],
                    },
                    {
                        "company": "Brightside Digital", "position": "Software Engineer",
                        "start_date": "2018-07", "end_date": "2021-03", "location": "Hamburg, Germany",
                        "highlights": [
                            "Built customer-facing services and APIs used by teams in four European markets.",
                            "Reduced average API response time by 32% through profiling and targeted caching.",
                            "Worked with design and analytics to improve onboarding completion by 18%.",
                        ],
                    },
                    {
                        "company": "Harbor Systems", "position": "Associate Developer",
                        "start_date": "2016-08", "end_date": "2018-06", "location": "Bremen, Germany",
                        "highlights": [
                            "Developed internal tools that shortened weekly reporting from several hours to minutes.",
                            "Added automated tests and documentation to improve the reliability of core services.",
                        ],
                    },
                ],
                "skills": [{"label": "Technology", "details": "Python, TypeScript, cloud platforms, distributed systems"}],
                "certifications": [
                    {"bullet": "Cloud Architecture Professional"},
                    {"bullet": "Certified Scrum Product Owner"},
                ],
                "languages": [
                    {"label": "English", "details": "Fluent"},
                    {"label": "German", "details": "Professional working proficiency"},
                ],
            },
        },
        "design": {
            "theme": theme,
            "page": {"show_footer": True, "show_top_note": True},
            "templates": {
                "footer": "*NAME -- PAGE_NUMBER/TOTAL_PAGES*",
                "top_note": "*LAST_UPDATED CURRENT_DATE*",
            },
        },
        "locale": copy.deepcopy(starter.get("locale", {})),
        "settings": copy.deepcopy(starter.get("settings", {})),
    }
    preview_root = RESUME_OUTPUT / "template_previews"
    preview_root.mkdir(parents=True, exist_ok=True)
    yaml_path = preview_root / f"{slugify(theme)}_preview.yaml"
    settings = document.setdefault("settings", {}).setdefault("render_command", {})
    settings["output_folder"] = f"{slugify(theme)}_output"
    slug = slugify(str(document.get("cv", {}).get("name", "my_cv")))
    for artifact, extension in (("pdf_path", "pdf"), ("markdown_path", "md"), ("html_path", "html"), ("typst_path", "typ"), ("png_path", "png")):
        settings[artifact] = f"OUTPUT_FOLDER/{slug}_CV.{extension}"
    settings["dont_generate_pdf"] = False
    settings["dont_generate_png"] = False
    dump_yaml_atomic(yaml_path, document)
    return render_cv(yaml_path, preview_root / f"{slugify(theme)}_output")


def render_file_downloads(paths: list[Path], prefix: str, mime: str) -> None:
    existing = [path for path in paths if path.is_file()]
    if not existing:
        st.info("No files here yet. Save your CV or generate a PDF to populate this list.")
        return
    for index, path in enumerate(sorted(existing, key=lambda item: (item.name.casefold(), str(item)))):
        col, action = st.columns([4, 1])
        col.write(path.name)
        action.download_button(
            "Download", data=path.read_bytes(), file_name=path.name, mime=mime,
            key=f"download_{prefix}_{index}_{path.name}", width="stretch",
        )


initialize()
st.title("CV Builder")
st.caption("Edit your career information, save reusable Markdown and RenderCV YAML, then generate a PDF.")

with st.sidebar:
    st.subheader("CV source")
    select_ai_provider()
    st.caption(Path(st.session_state["_source_path"]).name)
    uploaded_cv = st.file_uploader(
        "Load an existing CV",
        type=["yaml", "yml", "pdf", "docx", "txt"],
        max_upload_size=20,
        key="existing_cv_upload",
        help="RenderCV YAML loads directly. PDF, DOCX, and TXT files are mapped into fields; PDFs need selectable text.",
    )
    st.caption("Text documents are processed by the selected local AI CLI. Review and edit the loaded fields before saving.")
    if uploaded_cv and st.button("Load into editor", width="stretch"):
        try:
            suffix = Path(uploaded_cv.name).suffix.casefold()
            with st.spinner("Loading CV into the editor…"):
                if suffix in {".yaml", ".yml"}:
                    document = yaml.safe_load(uploaded_cv.getvalue())
                    if not isinstance(document, dict) or not isinstance(document.get("cv"), dict):
                        raise ValueError("This is not a valid RenderCV YAML document.")
                else:
                    extracted_text = extract_cv_text(uploaded_cv.name, uploaded_cv.getvalue())
                    imported_fields = extract_cv_fields(extracted_text, provider=st.session_state.get("llm_provider", "Codex CLI"))
                    document = imported_fields_document(imported_fields)
                load_editor_state(document, uploaded_cv.name)
            st.session_state["_import_notice"] = f"Loaded {uploaded_cv.name} into the editor. Review and edit the fields before saving."
            st.rerun()
        except (OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
            st.error(str(exc))
    st.divider()
    st.toggle(
        "ATS mode",
        value=False,
        key="ats_mode",
        help="When enabled, all text refinement uses your target job description as context.",
    )
    if st.session_state.get("ats_mode", False):
        ats_jd_file = st.file_uploader(
            "Job description file",
            type=["pdf", "docx", "txt", "md"],
            max_upload_size=20,
            key="ats_job_description_upload",
            help="Upload a text-based PDF, DOCX, TXT, or Markdown file, then load its text into the field below.",
        )
        if st.button("Load file into job description", key="load_ats_job_description", disabled=ats_jd_file is None, width="stretch"):
            try:
                st.session_state["ats_job_description"] = extract_job_description(ats_jd_file.name, ats_jd_file.getvalue())
                st.session_state["_ats_jd_file_notice"] = f"Loaded job description from {ats_jd_file.name}. Review or edit the text below."
                st.rerun()
            except (OSError, ValueError) as exc:
                st.error(str(exc))
        if notice := st.session_state.pop("_ats_jd_file_notice", None):
            st.success(notice)
        icon_text_area(
            "Target job description", "work",
            key="ats_job_description",
            height=220,
            max_chars=50_000,
            placeholder="Paste the job description here…",
            help="This job description guides all refinement actions and the ATS alignment review.",
        )
        if not active_job_description():
            st.caption("Add a job description to enable job-specific refinements and checks.")
    if st.button("Start a blank CV", width="stretch"):
        starter = load_yaml(STARTER_YAML)
        blank = {
            "cv": {"sections": {}},
            "design": copy.deepcopy(starter.get("design", {})),
            "locale": copy.deepcopy(starter.get("locale", {})),
            "settings": copy.deepcopy(starter.get("settings", {})),
        }
        load_editor_state(blank, "Blank CV")
        st.rerun()
if import_notice := st.session_state.pop("_import_notice", None):
    st.success(import_notice)
tabs = st.tabs(
    ["Profile", "Experience", "Other sections", "Templates", "ATS Checker"]
    + ([] if IS_STREAMLIT_CLOUD else ["Files"])
)
tab_profile, tab_roles, tab_more, tab_templates, tab_ats = tabs[:5]
tab_files = tabs[5] if not IS_STREAMLIT_CLOUD else None

with tab_profile:
    left, right = st.columns(2)
    with left:
        st.text_input("Name", key="profile_name", icon=":material/person:")
        st.text_input("Location", key="profile_location", icon=":material/location_on:")
        st.text_input("Email", key="profile_email", icon=":material/mail:")
        if error := email_format_error(st.session_state.get("profile_email", "")):
            st.error(error)
        st.markdown(":material/account_box: **Profile photo**")
        uploaded_photo = st.file_uploader(
            "Upload a profile photo", type=["png", "jpg", "jpeg"], max_upload_size=10,
            key="profile_photo_upload", label_visibility="collapsed",
            help="PNG or JPEG, up to 10 MB. The photo is copied into your ignored app data folder and referenced by the generated CV YAML.",
        )
        if uploaded_photo is not None:
            photo_bytes = uploaded_photo.getvalue()
            photo_digest = hashlib.sha256(photo_bytes).hexdigest()
            if photo_digest != st.session_state.get("_removed_photo_digest"):
                photo_extension = Path(uploaded_photo.name).suffix.casefold()
                photo_path = DATA_OUTPUT / f"profile-photo-{photo_digest[:12]}{photo_extension}"
                photo_path.parent.mkdir(parents=True, exist_ok=True)
                photo_path.write_bytes(photo_bytes)
                st.session_state["profile_photo_path"] = str(photo_path)
        photo_path_text = str(st.session_state.get("profile_photo_path", ""))
        if photo_path_text and Path(photo_path_text).is_file():
            st.image(photo_path_text, caption="Photo used in the generated CV", alt="Uploaded profile photo", width=160)
            if st.button("Remove profile photo", key="remove_profile_photo"):
                st.session_state["profile_photo_path"] = ""
                st.session_state["_removed_photo_digest"] = hashlib.sha256(uploaded_photo.getvalue()).hexdigest()
                st.rerun()
    with right:
        st.text_input("Phone number (include country code)", key="profile_phone", icon=":material/call:", help="RenderCV expects an international number such as +491234567890. Leave this blank if you do not want to show a phone number.")
        if error := phone_format_error(st.session_state.get("profile_phone", "")):
            st.error(error)
        icon_text_area("Links (one per line, e.g. LinkedIn: username)", "link", key="profile_links", height=110)
        if error := links_format_error(st.session_state.get("profile_links", "")):
            st.error(error)
    icon_text_area("About / professional summary", "person", key="profile_summary", height=190)
    if st.button("Refine summary with Codex", key="refine_summary", disabled=refinement_disabled(st.session_state["profile_summary"])):
        try:
            with st.spinner("Asking Codex for a wording suggestion…"):
                target_job_description = active_job_description()
                suggestion = refine_text(
                    st.session_state["profile_summary"],
                    context=st.session_state["profile_name"],
                    job_description=target_job_description,
                    provider=st.session_state.get("llm_provider", "Codex CLI"),
                )
            st.session_state["_suggestion"] = {
                "key": "profile_summary", "original": st.session_state["profile_summary"], "text": suggestion,
                "ats_mode": bool(st.session_state.get("ats_mode", False)),
                "job_description": target_job_description,
            }
            st.rerun()
        except RuntimeError as exc:
            st.error(str(exc))
    icon_text_area("Skills (one category per line: Label | skill, skill)", "psychology", key="profile_skills", height=130)

with tab_roles:
    role_ids = st.session_state["_role_ids"]
    for role_id in role_ids:
        with st.expander(f"{st.session_state.get(f'role_{role_id}_position', '') or 'Role'} · {st.session_state.get(f'role_{role_id}_company', '') or 'New experience'}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Company", key=f"role_{role_id}_company", icon=":material/business:")
                st.text_input("Position", key=f"role_{role_id}_position", icon=":material/work:")
                st.text_input("Location", key=f"role_{role_id}_location", icon=":material/location_on:")
            with col2:
                st.text_input("Start date (YYYY-MM)", key=f"role_{role_id}_start", icon=":material/calendar_month:")
                st.text_input("End date (YYYY-MM or present)", key=f"role_{role_id}_end", icon=":material/calendar_month:")
                start_value = st.session_state.get(f"role_{role_id}_start", "")
                end_value = st.session_state.get(f"role_{role_id}_end", "")
                if error := date_format_error(start_value):
                    st.error(f"Start date: {error}")
                if error := date_format_error(end_value, end_date=True):
                    st.error(f"End date: {error}")
                if (start_value and end_value and not date_format_error(start_value)
                        and not date_format_error(end_value, end_date=True)
                        and end_value.casefold() not in {"present", "current"} and end_value < start_value):
                    st.error("End date must be the same as or later than the start date.")
                icon_text_area("Role summary", "description", key=f"role_{role_id}_summary", height=90)
            icon_text_area("Achievements (one bullet per line)", "emoji_events", key=f"role_{role_id}_highlights", height=160)
            action1, action2 = st.columns([1, 5])
            if action1.button(
                "Refine achievements",
                key=f"refine_role_{role_id}",
                disabled=refinement_disabled(st.session_state[f"role_{role_id}_highlights"]),
            ):
                try:
                    with st.spinner("Asking Codex for a wording suggestion…"):
                        target_job_description = active_job_description()
                        suggestion = refine_text(
                            st.session_state[f"role_{role_id}_highlights"],
                            context=f"{st.session_state[f'role_{role_id}_position']} at {st.session_state[f'role_{role_id}_company']}",
                            job_description=target_job_description,
                            provider=st.session_state.get("llm_provider", "Codex CLI"),
                        )
                    st.session_state["_suggestion"] = {
                        "key": f"role_{role_id}_highlights",
                        "original": st.session_state[f"role_{role_id}_highlights"],
                        "text": suggestion,
                        "ats_mode": bool(st.session_state.get("ats_mode", False)),
                        "job_description": target_job_description,
                    }
                    st.rerun()
                except RuntimeError as exc:
                    st.error(str(exc))
            if action2.button("Remove this experience", key=f"remove_role_{role_id}"):
                if len(role_ids) > 1:
                    st.session_state["_remove_role_next"] = role_id
                    st.rerun()
                st.info("Keep at least one experience row; you can leave it blank.")
    if st.button("＋ Add experience", key="add_role"):
        new_id = st.session_state["_next_role_id"]
        st.session_state["_next_role_id"] = new_id + 1
        st.session_state["_role_ids"].append(new_id)
        for key in ("company", "position", "start", "end", "location", "summary", "highlights"):
            st.session_state[f"role_{new_id}_{key}"] = ""
        st.rerun()

with tab_more:
    with st.expander("Achievement types and writing tips", expanded=True):
        st.markdown(
            """
**Technical** — engineering work and technical delivery: architecture, implementation, reliability, security, quality, or performance.

**Leadership** — how you led or enabled people and teams: mentoring, ownership, collaboration, stakeholder alignment, or execution.

**Product** — outcomes for users, customers, or the business: features, adoption, product direction, roadmap, or measurable value.

Write one achievement per line. Start with an action, say what changed and the result, and include metrics only when you know them. Codex assigns each line to the category that best matches its primary impact; review the grouping before saving.
            """
        )
    icon_text_area(
        "Achievements", "emoji_events",
        key="section_all_achievements",
        height=300,
        placeholder="One achievement per line…",
        help="Add technical, leadership, and product achievements together. They will be classified into separate CV sections.",
    )
    current_achievement_text = str(st.session_state.get("section_all_achievements", ""))
    refine_col, categorize_col = st.columns(2)
    if refine_col.button(
        "Refine achievements",
        key="refine_all_achievements",
        disabled=refinement_disabled(current_achievement_text),
        width="stretch",
    ):
        try:
            with st.spinner("Asking Codex to refine your achievements…"):
                target_job_description = active_job_description()
                suggestion = refine_text(
                    current_achievement_text,
                    context="Technical, leadership, and product achievements",
                    job_description=target_job_description,
                    provider=st.session_state.get("llm_provider", "Codex CLI"),
                )
            st.session_state["_suggestion"] = {
                "key": "section_all_achievements",
                "original": current_achievement_text,
                "text": suggestion,
                "ats_mode": bool(st.session_state.get("ats_mode", False)),
                "job_description": target_job_description,
            }
            st.rerun()
        except RuntimeError as exc:
            st.error(str(exc))
    if categorize_col.button(
        "Categorize achievements",
        key="categorize_achievements",
        disabled=not current_achievement_text.strip(),
        width="stretch",
    ):
        try:
            with st.spinner("Classifying achievements by primary impact…"):
                proposal = categorize_achievements(current_achievement_text, provider=st.session_state.get("llm_provider", "Codex CLI"))
            st.session_state["_achievement_categorization_proposal"] = proposal
            st.session_state["_achievement_categorization_source"] = current_achievement_text
            st.rerun()
        except RuntimeError as exc:
            st.error(str(exc))

    categorized_source = st.session_state.get("_categorized_achievements_source", "")
    if current_achievement_text.strip() and current_achievement_text != categorized_source:
        st.info("These achievements have changed. Categorize and review them before saving or previewing the CV.")
    elif current_achievement_text.strip():
        counts = st.session_state.get("_categorized_achievements", {})
        count_text = " · ".join(
            f"{label}: {len(counts.get(label, []))}"
            for label in ACHIEVEMENT_CATEGORIES
        )
        st.caption(f"Categorized and ready to save — {count_text}")
        with st.expander("View current categorization"):
            category_columns = st.columns(3)
            for column, label in zip(category_columns, ACHIEVEMENT_CATEGORIES):
                column.markdown(f"**{label}**")
                items = counts.get(label, [])
                if items:
                    column.markdown("\n".join(f"- {item}" for item in items))
                else:
                    column.caption("No achievements assigned")

    proposal = st.session_state.get("_achievement_categorization_proposal")
    if proposal:
        proposal_is_current = st.session_state.get("_achievement_categorization_source") == current_achievement_text
        with st.expander("Review suggested achievement categories", expanded=True):
            if not proposal_is_current:
                st.warning("The achievements changed after this suggestion. Categorize them again to review an up-to-date proposal.")
            review_columns = st.columns(3)
            category_keys = {"Technical": "technical", "Leadership": "leadership", "Product": "product"}
            for column, (label, category_key) in zip(review_columns, category_keys.items()):
                column.markdown(f"**{label}**")
                items = proposal.get(category_key, [])
                if items:
                    column.markdown("\n".join(f"- {item}" for item in items))
                else:
                    column.caption("No achievements assigned")
            if proposal_is_current and st.button("Accept these categories", key="accept_achievement_categories", type="primary"):
                st.session_state["_categorized_achievements"] = {
                    label: proposal[category_key]
                    for label, category_key in category_keys.items()
                }
                st.session_state["_categorized_achievements_source"] = current_achievement_text
                st.session_state.pop("_achievement_categorization_proposal", None)
                st.session_state.pop("_achievement_categorization_source", None)
                st.rerun()
    icon_text_area("Education (one entry per line: Institution | Degree | Area | Start | End | Location)", "school", key="section_education", height=120)
    education_errors = [error for error in validate_form_fields() if error.startswith("Education entry ")]
    for error in education_errors:
        st.error(error)
    icon_text_area("Certifications (one per line)", "workspace_premium", key="section_certifications", height=90)
    icon_text_area("Languages (one per line: Language | Proficiency)", "translate", key="section_languages", height=90)

with tab_templates:
    saved_theme = str(st.session_state.get("_base_document", {}).get("design", {}).get("theme", "classic"))
    themes = list(RENDERCV_THEMES)
    if saved_theme not in themes:
        themes.append(saved_theme)
    st.caption("Compare RenderCV templates using a fictional, multi-section sample CV. Your personal CV content is not used in these previews.")
    st.selectbox(
        "Choose a template", themes, index=None, placeholder="Select a template to preview",
        format_func=lambda theme: RENDERCV_THEME_LABELS.get(theme, theme), key="selected_template",
    )
    selected_theme = st.session_state.get("selected_template")
    if selected_theme:
        preview_key = f"{selected_theme}:sample-v2"
        st.subheader(f"{RENDERCV_THEME_LABELS.get(selected_theme, selected_theme)} preview")
        refresh_preview = st.button("Render preview again", key="refresh_template_preview")
        if refresh_preview or st.session_state.get("_template_preview_key") != preview_key:
            try:
                with st.spinner(f"Rendering {selected_theme} preview…"):
                    st.session_state["_template_preview_path"] = str(render_template_preview(selected_theme))
                    st.session_state["_template_preview_key"] = preview_key
                    st.session_state["_template_preview_draft_hash"] = draft_hash()
            except (OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
                st.error(str(exc))
        preview_str = st.session_state.get("_template_preview_path", "")
        if preview_str and Path(preview_str).is_file():
            preview_images = sorted(Path(preview_str).parent.glob("*.png"))
            for image_index, preview_image in enumerate(preview_images, start=1):
                theme_label = RENDERCV_THEME_LABELS.get(selected_theme, selected_theme)
                st.image(str(preview_image), caption=f"{theme_label} · page {image_index}", alt=f"CV preview using the {theme_label} template, page {image_index}", width="stretch")
            if not preview_images:
                st.info("The PDF was rendered, but page images are unavailable.")
            if st.session_state.get("_template_preview_draft_hash") != draft_hash():
                st.caption("The form has changed since this preview. Refresh the preview to see the latest content.")
            if phone_format_error(current_profile()["phone"]):
                st.caption("The phone number is hidden in this preview until it has a valid international format.")
        if selected_theme != saved_theme:
            st.caption("The selected template will be used for the next generated CV.")
    else:
        st.info("Choose a template to preview it with sample CV content. Your information is not used in the sample preview.")

with tab_ats:
    st.subheader("ATS alignment review")
    if not st.session_state.get("ats_mode", False):
        st.info("ATS mode is off. Turn it on in the sidebar to add a job description, run a check, and make refinements job-specific.")
    elif not active_job_description():
        st.info("Add a target job description in the sidebar to run an ATS check or enable job-specific refinements.")
    else:
        st.caption("With ATS mode on, all text refinement uses this job description as context. The check reports alignment findings and does not edit your CV.")
        if st.button("Check ATS alignment", key="run_ats_check", type="primary"):
            try:
                with st.spinner("Comparing your CV with the job description…"):
                    report = review_ats_alignment(current_cv_content(), active_job_description(), provider=st.session_state.get("llm_provider", "Codex CLI"))
                st.session_state["_ats_review"] = report
                st.session_state["_ats_review_key"] = ats_review_key()
            except (OSError, RuntimeError, ValueError) as exc:
                st.error(str(exc))

        report = st.session_state.get("_ats_review")
        if report:
            if st.session_state.get("_ats_review_key") != ats_review_key():
                st.warning("The CV or job description has changed since this review. Run the check again for current results.")
            st.markdown(f"**Alignment summary**\n\n{report['alignment_summary']}")
            st.caption("This content-based review does not predict the score from a specific ATS product.")
            keywords_col, gaps_col = st.columns(2)
            with keywords_col:
                st.markdown("**Relevant keywords found in your CV**")
                if report["matched_keywords"]:
                    st.markdown("\n".join(f"- {item}" for item in report["matched_keywords"]))
                else:
                    st.caption("No matching keywords identified.")
            with gaps_col:
                st.markdown("**Relevant keywords not found**")
                if report["missing_keywords"]:
                    st.markdown("\n".join(f"- {item}" for item in report["missing_keywords"]))
                else:
                    st.caption("No clear keyword gaps identified.")
            for heading, key in (
                ("Evidence gaps to review", "evidence_gaps"),
                ("Suggested improvements", "recommendations"),
                ("Formatting concerns", "formatting_concerns"),
            ):
                if report[key]:
                    st.markdown(f"**{heading}**")
                    st.markdown("\n".join(f"- {item}" for item in report[key]))
            if report["suggested_rewrites"]:
                st.markdown("**Targeted rewrite suggestions**")
                for rewrite_index, rewrite in enumerate(report["suggested_rewrites"], start=1):
                    with st.expander(f"{rewrite_index}. {rewrite['rendercv_field']}"):
                        st.markdown(f"**Current text**\n\n{rewrite['current_text']}")
                        st.markdown(f"**Suggested text**\n\n{rewrite['suggested_text']}")
                        st.caption(rewrite["rationale"])

if tab_files is not None:
    with tab_files:
        file_category = st.segmented_control("Your files", ["Markdown", "CVs"], default="Markdown", key="file_category")
        if file_category == "Markdown":
            markdown_files = [path for path in list(DATA_OUTPUT.rglob("*.md")) + list(RESUME_OUTPUT.rglob("*.md")) if "template_previews" not in path.parts]
            render_file_downloads(markdown_files, "markdown", "text/markdown")
        else:
            cv_files = [path for path in list(RESUME_OUTPUT.rglob("*.yaml")) + list(RESUME_OUTPUT.rglob("*.yml")) + list(RESUME_OUTPUT.rglob("*.pdf")) if "template_previews" not in path.parts]
            existing_cv_files = sorted((path for path in cv_files if path.is_file()), key=lambda item: (item.suffix.casefold(), item.name.casefold()))
            if not existing_cv_files:
                st.info("No CV files yet. Save your CV or generate a PDF to populate this list.")
            for index, path in enumerate(existing_cv_files):
                col, action = st.columns([4, 1])
                col.write(path.name)
                mime = "application/pdf" if path.suffix.casefold() == ".pdf" else "application/yaml"
                action.download_button("Download", data=path.read_bytes(), file_name=path.name, mime=mime, key=f"download_cv_{index}_{path.name}", width="stretch")

suggestion = st.session_state.get("_suggestion")
if suggestion:
    suggestion_matches_mode = (
        suggestion.get("ats_mode", False) == bool(st.session_state.get("ats_mode", False))
        and suggestion.get("job_description", "") == active_job_description()
    )
    st.divider()
    st.subheader("Review AI suggestion")
    if not suggestion_matches_mode:
        st.warning("ATS mode or the job description changed after this suggestion. Refine the text again before applying it.")
    before, after = st.columns(2)
    before.text_area("Current wording", value=suggestion["original"], disabled=True, key="suggestion_original")
    after.text_area("Suggested wording", value=suggestion["text"], disabled=True, key="suggestion_text")
    accept, reject = st.columns(2)
    if accept.button("Apply suggestion", type="primary", disabled=not suggestion_matches_mode):
        st.session_state["_apply_suggestion_next"] = {"key": suggestion["key"], "text": suggestion["text"]}
        st.rerun()
    if reject.button("Reject suggestion"):
        st.session_state.pop("_suggestion", None)
        st.rerun()

st.divider()
save_col, generate_col, status_col = st.columns([1, 1, 4])
if save_col.button("Save Markdown + YAML", type="primary", width="stretch"):
    validation_errors = validate_form_fields()
    if validation_errors:
        st.error("Please fix these fields before saving:\n\n" + "\n".join(f"- {error}" for error in validation_errors))
    else:
        try:
            with st.spinner("Saving your CV…"):
                yaml_path, _, _ = save_current()
            if IS_STREAMLIT_CLOUD:
                st.success("CV saved. The hosted app disables shared file downloads; generate a PDF to download your CV.")
            else:
                st.success("Markdown notes and CV YAML saved. Download them from Files.")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            st.error(f"Could not save the CV: {exc}")

if generate_col.button("Generate PDF", width="stretch"):
    validation_errors = validate_form_fields()
    if validation_errors:
        st.error("Please fix these fields before generating the PDF:\n\n" + "\n".join(f"- {error}" for error in validation_errors))
    else:
        try:
            with st.spinner("Saving and rendering the CV…"):
                yaml_path, document, _ = save_current()
                slug = slugify(str(document.get("cv", {}).get("name", "my_cv")))
                output_dir = RESUME_OUTPUT / f"{slug}_rendercv_output"
                pdf_path = render_cv(yaml_path, output_dir)
            st.session_state["_pdf_path"] = str(pdf_path)
            st.session_state["_rendered_hash"] = draft_hash()
            st.success("PDF generated. Download it using the button below.")
        except (OSError, RuntimeError, ValueError, yaml.YAMLError) as exc:
            st.error(str(exc))

pdf_path_str = st.session_state.get("_pdf_path", "")
pdf_is_stale = bool(pdf_path_str and st.session_state.get("_rendered_hash") != draft_hash())
if pdf_is_stale:
    st.info("The current form has changed since this PDF was generated. Generate again to refresh the preview.")
if pdf_path_str and Path(pdf_path_str).is_file():
    pdf_path = Path(pdf_path_str)
    with generate_col:
        st.download_button("Download PDF", data=pdf_path.read_bytes(), file_name=pdf_path.name, mime="application/pdf", width="stretch")

if pdf_path_str and Path(pdf_path_str).is_file() and pdf_is_stale:
    st.info("The current form has changed since this PDF was generated. Generate again to refresh it.")
