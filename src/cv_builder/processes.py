from __future__ import annotations

import shutil
import subprocess
import tempfile
import json
from pathlib import Path
from string import Template
from typing import Any


LLM_PROVIDERS = ("Codex CLI", "Gemini CLI", "Claude Code")
PROVIDER_COMMANDS = {"Codex CLI": "codex", "Gemini CLI": "gemini", "Claude Code": "claude"}
PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_prompt(name: str, **values: str) -> str:
    """Load a customizable prompt template from the project prompts directory."""
    prompt_path = PROMPT_DIR / f"{name}.txt"
    try:
        template = prompt_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Prompt file could not be read: {prompt_path.name}") from exc
    try:
        return Template(template).substitute(**values)
    except KeyError as exc:
        raise RuntimeError(f"Prompt template {prompt_path.name} is missing a value: {exc.args[0]}") from exc


def run_llm_prompt(
    prompt: str,
    *,
    provider: str = "Codex CLI",
    task: str = "AI request",
    schema: dict[str, Any] | None = None,
    timeout: int = 240,
) -> str:
    """Run one prompt through an installed local AI CLI, without granting file-edit tools."""
    command = PROVIDER_COMMANDS.get(provider)
    if command is None:
        raise RuntimeError(f"Unknown AI provider: {provider}")
    executable = shutil.which(command)
    if not executable:
        raise RuntimeError(f"{provider} was not found. Install and authenticate it, or choose another provider.")
    with tempfile.TemporaryDirectory(prefix="resume-studio-llm-") as temp_dir:
        temp_path = Path(temp_dir)
        output_path = temp_path / "response.txt"
        schema_path = temp_path / "schema.json"
        request = prompt
        if schema:
            schema_text = json.dumps(schema, ensure_ascii=False)
            if provider == "Codex CLI":
                schema_path.write_text(schema_text, encoding="utf-8")
            else:
                request += "\n\n" + load_prompt("structured_output_suffix", schema_text=schema_text)
        if provider == "Codex CLI":
            args = [executable, "exec", "--ephemeral", "--sandbox", "read-only",
                    "--output-last-message", str(output_path)]
            if schema:
                args.extend(["--output-schema", str(schema_path)])
            args.append("-")
            input_text = request
        elif provider == "Gemini CLI":
            args = [executable, "--prompt", request, "--output-format", "json" if schema else "text",
                    "--approval-mode", "plan"]
            input_text = None
        else:
            args = [executable, "--bare", "--tools", "", "--no-session-persistence", "-p"]
            if schema:
                args.extend(["--json-schema", json.dumps(schema, ensure_ascii=False), "--output-format", "json"])
            args.append(request)
            input_text = None
        try:
            result = subprocess.run(
                args, input=input_text, capture_output=True, text=True, timeout=timeout,
                check=False, cwd=Path(__file__).resolve().parents[2],
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"{task} timed out after {timeout // 60} minutes.") from exc
        if result.returncode:
            details = (result.stderr or result.stdout).strip()
            raise RuntimeError(f"{task} failed using {provider}: {details[-2000:] or 'unknown error'}")
        raw = output_path.read_text(encoding="utf-8").strip() if output_path.is_file() else result.stdout.strip()
        if provider in {"Gemini CLI", "Claude Code"} and (schema or provider == "Claude Code"):
            try:
                envelope = json.loads(raw)
            except json.JSONDecodeError:
                envelope = None
            if isinstance(envelope, dict):
                if isinstance(envelope.get("response"), str):
                    raw = envelope["response"].strip()
                elif "structured_output" in envelope:
                    raw = json.dumps(envelope["structured_output"], ensure_ascii=False)
                elif isinstance(envelope.get("result"), str):
                    raw = envelope["result"].strip()
        if not raw:
            raise RuntimeError(f"{task} returned an empty response from {provider}.")
        return raw


def refine_text(text: str, context: str = "", job_description: str = "", provider: str = "Codex CLI") -> str:
    if len(job_description) > 50_000:
        raise RuntimeError("The job description is too long. Please limit it to 50,000 characters.")
    targeting = ""
    if job_description.strip():
        targeting = load_prompt("refine_targeting", job_description=job_description.strip())
    prompt = load_prompt(
        "refine_text",
        targeting=targeting,
        context=context,
        text=text,
    )
    return run_llm_prompt(prompt, provider=provider, task="Text refinement", timeout=180)


CV_IMPORT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "name", "location", "email", "phone", "summary", "social_networks", "websites",
        "skills", "experience", "technical_achievements", "leadership_achievements",
        "product_achievements", "education", "certifications", "languages",
    ],
    "properties": {
        "name": {"type": "string"},
        "location": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": "string"},
        "summary": {"type": "string"},
        "social_networks": {
            "type": "array", "items": {"type": "object", "additionalProperties": False,
                "required": ["network", "username"], "properties": {
                    "network": {"type": "string", "enum": [
                        "LinkedIn", "GitHub", "GitLab", "IMDB", "Instagram", "ORCID", "Mastodon",
                        "StackOverflow", "ResearchGate", "YouTube", "Google Scholar", "Telegram",
                        "WhatsApp", "Leetcode", "X", "Bluesky", "Reddit",
                    ]},
                    "username": {"type": "string"},
                }},
        },
        "websites": {"type": "array", "items": {"type": "string"}},
        "skills": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["label", "details"], "properties": {"label": {"type": "string"}, "details": {"type": "string"}}}},
        "experience": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["company", "position", "start_date", "end_date", "location", "summary", "highlights"],
            "properties": {
                "company": {"type": "string"}, "position": {"type": "string"},
                "start_date": {"type": "string"}, "end_date": {"type": "string"},
                "location": {"type": "string"}, "summary": {"type": "string"},
                "highlights": {"type": "array", "items": {"type": "string"}},
            }},
        },
        "technical_achievements": {"type": "array", "items": {"type": "string"}},
        "leadership_achievements": {"type": "array", "items": {"type": "string"}},
        "product_achievements": {"type": "array", "items": {"type": "string"}},
        "education": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["institution", "degree", "area", "start_date", "end_date", "location"],
            "properties": {key: {"type": "string"} for key in ("institution", "degree", "area", "start_date", "end_date", "location")}}},
        "certifications": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "array", "items": {"type": "object", "additionalProperties": False,
            "required": ["label", "details"], "properties": {"label": {"type": "string"}, "details": {"type": "string"}}}},
    },
}


def extract_cv_fields(text: str, provider: str = "Codex CLI") -> dict[str, Any]:
    """Map extracted CV text into editable fields using structured output."""
    if not text.strip():
        raise RuntimeError("No readable text was found in this file.")
    if len(text) > 120_000:
        raise RuntimeError("The extracted CV is unusually long. Please shorten the document and try again.")
    prompt = load_prompt("cv_import", cv_text=text)
    raw = run_llm_prompt(prompt, provider=provider, task="CV import", schema=CV_IMPORT_SCHEMA)
    try:
        fields = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("CV import returned data that could not be read. Please try another file.") from exc
    if not isinstance(fields, dict) or not isinstance(fields.get("name"), str):
        raise RuntimeError("CV import did not return the expected fields. Please try another file.")
    return fields


ACHIEVEMENT_CATEGORIES_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["technical", "leadership", "product"],
    "properties": {
        key: {"type": "array", "items": {"type": "string"}}
        for key in ("technical", "leadership", "product")
    },
}


def categorize_achievements(text: str, provider: str = "Codex CLI") -> dict[str, list[str]]:
    """Classify achievements by primary impact while preserving each input line."""
    lines = [line.strip().lstrip("-• ").strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return {"technical": [], "leadership": [], "product": []}
    prompt = load_prompt("categorize_achievements", achievements="\n".join(lines))
    raw = run_llm_prompt(prompt, provider=provider, task="Achievement categorization", schema=ACHIEVEMENT_CATEGORIES_SCHEMA)
    try:
        candidate = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The selected AI provider returned categories that could not be read. Please try again.") from exc
    if not isinstance(candidate, dict):
        raise RuntimeError("The selected AI provider returned an invalid achievement categorization. Please try again.")
    categories: dict[str, list[str]] = {}
    for category in ("technical", "leadership", "product"):
        values = candidate.get(category)
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise RuntimeError("The selected AI provider returned an invalid achievement categorization. Please try again.")
        categories[category] = values
    from collections import Counter

    categorized_lines = [item for values in categories.values() for item in values]
    if Counter(categorized_lines) != Counter(lines):
        raise RuntimeError("The categorization did not preserve every achievement exactly. Please try again.")
    return categories


ATS_REVIEW_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["alignment_summary", "matched_keywords", "missing_keywords", "evidence_gaps", "recommendations", "suggested_rewrites", "formatting_concerns"],
    "properties": {
        "alignment_summary": {"type": "string"},
        "matched_keywords": {"type": "array", "items": {"type": "string"}},
        "missing_keywords": {"type": "array", "items": {"type": "string"}},
        "evidence_gaps": {"type": "array", "items": {"type": "string"}},
        "recommendations": {"type": "array", "items": {"type": "string"}},
        "suggested_rewrites": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["rendercv_field", "current_text", "suggested_text", "rationale"],
            "properties": {
                "rendercv_field": {"type": "string"},
                "current_text": {"type": "string"},
                "suggested_text": {"type": "string"},
                "rationale": {"type": "string"},
            },
        }},
        "formatting_concerns": {"type": "array", "items": {"type": "string"}},
    },
}


def review_ats_alignment(cv_content: dict[str, Any], job_description: str, provider: str = "Codex CLI") -> dict[str, Any]:
    """Compare current CV content with a job description without editing the CV."""
    if not job_description.strip():
        raise RuntimeError("Enter a job description before running the ATS check.")
    if len(job_description) > 50_000:
        raise RuntimeError("The job description is too long. Please limit it to 50,000 characters.")
    prompt = load_prompt(
        "ats_review",
        cv_json=json.dumps(cv_content, ensure_ascii=False),
        job_description=job_description.strip(),
    )
    raw = run_llm_prompt(prompt, provider=provider, task="ATS check", schema=ATS_REVIEW_SCHEMA)
    try:
        review = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("The ATS check returned data that could not be read. Please try again.") from exc
    if not isinstance(review, dict) or any(
        not isinstance(review.get(key), list) or not all(isinstance(item, str) for item in review[key])
        for key in ("matched_keywords", "missing_keywords", "evidence_gaps", "recommendations", "formatting_concerns")
    ) or not isinstance(review.get("alignment_summary"), str):
        raise RuntimeError("The ATS check returned an invalid review. Please try again.")
    rewrites = review.get("suggested_rewrites")
    if not isinstance(rewrites, list) or any(
        not isinstance(item, dict) or any(not isinstance(item.get(key), str)
            for key in ("rendercv_field", "current_text", "suggested_text", "rationale"))
        for item in rewrites
    ):
        raise RuntimeError("The ATS check returned invalid rewrite suggestions. Please try again.")
    return review


def generate_cover_letter(
    *,
    cv_content: str = "",
    user_description: str = "",
    job_description: str = "",
    provider: str = "Codex CLI",
) -> str:
    """Draft a factual, editable cover letter from either a CV or user notes."""
    if not cv_content.strip() and not user_description.strip():
        raise RuntimeError("Provide an existing CV or a description of your background before generating a letter.")
    if len(cv_content) > 120_000 or len(user_description) > 50_000 or len(job_description) > 50_000:
        raise RuntimeError("The provided content is too long. Shorten the input and try again.")
    prompt = load_prompt(
        "cover_letter",
        cv_content=cv_content.strip(),
        user_description=user_description.strip(),
        job_description=job_description.strip(),
    )
    return run_llm_prompt(prompt, provider=provider, task="Cover letter generation", timeout=240)


def render_cv(yaml_path: Path, output_dir: Path) -> Path:
    executable = shutil.which("rendercv")
    if not executable:
        raise RuntimeError("RenderCV was not found. Install dependencies with `python -m pip install -r requirements.txt`.")
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run(
            [executable, "render", str(yaml_path)],
            cwd=yaml_path.parent,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("RenderCV timed out after 3 minutes.") from exc
    if result.returncode:
        details = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"RenderCV failed: {details[-3000:] or 'unknown error'}")
    pdf_path = output_dir / f"{yaml_path.stem}.pdf"
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        candidates = list(output_dir.glob("*.pdf"))
        if not candidates:
            raise RuntimeError("RenderCV finished, but no PDF was created.")
        pdf_path = candidates[0]
    return pdf_path
