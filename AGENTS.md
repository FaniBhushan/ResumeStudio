# AGENTS.md

## Collaboration

This is a collaborative project. Discuss proposals, tradeoffs, and questions with the user before making changes. Do not implement or edit files unless the user explicitly asks for implementation. When asked to implement, keep the user informed about meaningful decisions and summarize the changes and checks when finished.

## Project overview

Resume Studio helps people build and tailor CVs and cover letters from their career notes. It is a local Python application built with Streamlit and RenderCV, with optional AI assistance through installed provider CLIs. It has no database; user files are stored locally.

## Repository map

- `app.py`: Streamlit entry point and navigation.
- `app_pages/`: CV Builder and Cover Letter screens.
- `src/cv_builder/`: import, validation, storage, provider, and RenderCV logic.
- `prompts/`: editable AI prompt templates.
- `assets/`: visual assets and blank RenderCV starter YAML.
- `tests/`: standard-library unit tests.
- `data/` and `resumes/`: local-only user data and generated files; both are gitignored.
- `architecture-plan.md`: architecture and implementation notes.

## Setup and commands

Run from the repository root. Use Python 3.12 or newer.

- Create and activate an environment: `python3 -m venv .venv && source .venv/bin/activate`
- Install dependencies: `python -m pip install -r requirements.txt`
- Start the app: `streamlit run app.py`
- Run unit tests: `python -m unittest discover -s tests -v`

There are no separate type-check, lint, or build commands configured. AI features also require a locally installed and authenticated `codex`, `gemini`, or `claude` CLI.

## Implementation conventions

- Follow existing Python style: four-space indentation, `snake_case` functions and modules, and type hints where they fit existing patterns.
- Keep Streamlit screen code in `app_pages/` and reusable application logic in `src/cv_builder/`.
- Validate imported and user-provided content at the application boundary; preserve existing RenderCV YAML compatibility.
- Keep changes focused and explain any new production dependency and why existing dependencies are insufficient.

## Validation

- Run the full unittest discovery command after behavior changes; add focused regression tests for fixes.
- Tests use `unittest`; name files `test_*.py` and methods `test_<behavior>`.
- For UI changes, inspect the affected Streamlit screen at desktop and mobile sizes.
- Report checks that could not run and the reason. No coverage threshold is configured.

## Project pitfalls

- `data/` and `resumes/` may contain private career information. Never add their contents, provider credentials, imported resumes, or generated documents to Git.
- AI-generated content can contain errors; preserve review before users accept suggestions or export documents.
- Keep `assets/sample_cv.yaml` a blank generic starter rather than personal career data.

## Further guidance

- Read `architecture-plan.md` before changing component boundaries or data flow.
- Read `README.md` for setup, supported import formats, provider behavior, and the user workflow.
- Read `prompts/README.md` before changing prompt templates.

## Completion

- Complete the requested behavior and run relevant validation.
- Update documentation when usage or configuration changes.
- Summarize changes, checks performed, and any remaining limitations.
