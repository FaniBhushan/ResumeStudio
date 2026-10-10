from __future__ import annotations

import re
import tempfile
import copy
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
DATA_OUTPUT = ROOT / "data" / "app"
RESUME_OUTPUT = ROOT / "resumes" / "generated"
STARTER_YAML = ROOT / "resumes" / "Fani_Bhushan_CV.yaml"


class QuotedString(str):
    """A YAML string that must remain a string even when it looks numeric."""


class CVYamlDumper(yaml.SafeDumper):
    pass


def _represent_quoted_string(dumper: yaml.SafeDumper, value: QuotedString) -> yaml.ScalarNode:
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(value), style="'")


CVYamlDumper.add_representer(QuotedString, _represent_quoted_string)


def slugify(value: str, fallback: str = "my_cv") -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or fallback


def load_yaml(path: Path) -> dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    value = yaml.safe_load(content)
    if not isinstance(value, dict) or not isinstance(value.get("cv"), dict):
        raise ValueError("This file does not look like a RenderCV YAML document.")
    # PyYAML's YAML 1.1 resolver can parse an unquoted phone such as
    # 09620531036 as an integer and discard its leading zero. Recover the
    # original scalar spelling from the YAML syntax tree before editing it.
    root = yaml.compose(content)
    if isinstance(root, yaml.MappingNode):
        for root_key, cv_node in root.value:
            if root_key.value == "cv" and isinstance(cv_node, yaml.MappingNode):
                for cv_key, phone_node in cv_node.value:
                    if cv_key.value == "phone" and isinstance(phone_node, yaml.ScalarNode):
                        if phone_node.tag != "tag:yaml.org,2002:null":
                            value["cv"]["phone"] = phone_node.value
                        break
                break
    phone = value["cv"].get("phone")
    if phone is not None:
        value["cv"]["phone"] = str(phone)
    return value


def dump_yaml_atomic(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serializable = copy.deepcopy(document)
    phone = serializable.get("cv", {}).get("phone")
    if phone is not None:
        serializable["cv"]["phone"] = QuotedString(str(phone))
    content = yaml.dump(serializable, Dumper=CVYamlDumper, allow_unicode=True, sort_keys=False, width=1000)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temp:
        temp.write(content)
        temp_path = Path(temp.name)
    temp_path.replace(path)


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temp:
        temp.write(content)
        temp_path = Path(temp.name)
    temp_path.replace(path)


def save_markdown(
    profile: dict[str, Any],
    roles: list[dict[str, Any]],
    achievements: dict[str, str],
    sections: dict[str, Any],
) -> None:
    write_text_atomic(DATA_OUTPUT / "profile.md", profile_markdown(profile, sections))
    role_folder = DATA_OUTPUT / "roles"
    for index, role in enumerate(roles, start=1):
        title = role.get("position", "Role")
        company = role.get("company", "Company")
        filename = f"role-{index:02d}-{slugify(company)}-{slugify(title)}.md"
        write_text_atomic(role_folder / filename, role_markdown(role))
    achievement_folder = DATA_OUTPUT / "achievements"
    for category, text in achievements.items():
        write_text_atomic(achievement_folder / f"{slugify(category)}-achievements.md", achievement_markdown(category, text))


def profile_markdown(profile: dict[str, Any], sections: dict[str, Any]) -> str:
    lines = [f"# {profile.get('name') or 'CV Profile'}", ""]
    for label, key in (("Location", "location"), ("Email", "email"), ("Phone", "phone"), ("Links", "links")):
        value = profile.get(key)
        if value:
            lines += [f"**{label}:** {value}"]
    lines += ["", "## About", "", profile.get("summary", "").strip(), ""]
    if profile.get("skills"):
        lines += ["## Skills", "", profile["skills"].strip(), ""]
    education = sections.get("education", [])
    if education:
        lines += ["## Education", ""]
        for entry in education:
            if isinstance(entry, dict):
                details = " · ".join(str(entry.get(key, "")) for key in
                                     ("institution", "degree", "area", "start_date", "end_date", "location")
                                     if entry.get(key))
                lines += [f"- {details}"]
        lines += [""]
    certifications = sections.get("certifications", [])
    if certifications:
        lines += ["## Certifications", ""]
        lines += [f"- {item.get('bullet', '') if isinstance(item, dict) else item}" for item in certifications]
        lines += [""]
    languages = sections.get("languages", [])
    if languages:
        lines += ["## Languages", ""]
        lines += [f"- {item.get('label', '')}: {item.get('details', '')}" for item in languages if isinstance(item, dict)]
        lines += [""]
    return "\n".join(lines)


def role_markdown(role: dict[str, Any]) -> str:
    lines = [f"# {role.get('position') or 'Role'} — {role.get('company') or 'Company'}", ""]
    for label, key in (("Dates", "dates"), ("Location", "location")):
        if role.get(key):
            lines += [f"**{label}:** {role[key]}"]
    lines += ["", "## Description", "", role.get("summary", "").strip(), "", "## Achievements", ""]
    lines += [f"- {item.strip()}" for item in role.get("highlights", "").splitlines() if item.strip()]
    lines += [""]
    return "\n".join(lines)


def achievement_markdown(category: str, text: str) -> str:
    lines = [f"# {category.title()} Achievements", ""]
    lines += [f"- {line.strip()}" for line in text.splitlines() if line.strip()]
    return "\n".join(lines) + "\n"
