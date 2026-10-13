<p align="center">
  <img src="assets/resume-studio-logo.svg" alt="Resume Studio" width="420">
</p>

<h1 align="center">Resume Studio</h1>

<p align="center">Build a thoughtful CV, tailor it to a role, and create a matching cover letter — all in one local workspace.</p>

<p align="center">
  <a href="https://www.python.org/"><img alt="Python 3.12+" src="https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="https://streamlit.io/"><img alt="Streamlit" src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white"></a>
  <a href="https://rendercv.com/"><img alt="RenderCV" src="https://img.shields.io/badge/PDF-RenderCV-333333"></a>
  <img alt="Local-first" src="https://img.shields.io/badge/data-local--first-2E8B57">
</p>

Resume Studio is a local Streamlit app for turning career notes into polished, editable application documents. It uses [RenderCV](https://rendercv.com/) to render CV PDFs from structured YAML with RenderCV's templates. Keep your experience in your own words, optionally get AI-assisted suggestions, and review every change before saving or generating a PDF.

> **Enjoying Resume Studio?** [Star the project on GitHub](https://github.com/FaniBhushan/ResumeStudio) to support its development.

## Quick start

Run these commands from a terminal with Python 3.12 or newer:

```bash
git clone https://github.com/FaniBhushan/ResumeStudio.git
cd ResumeStudio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local address Streamlit prints. In **CV Builder**, start with the blank CV or import a RenderCV YAML, selectable-text PDF, DOCX, or TXT file. Review and edit the fields, then save your CV and generate a PDF. Open **Cover Letter** to create a draft from your CV or background notes. AI features are optional; configure a local provider CLI if you want suggestions.

## Desktop installers

Windows, macOS, and Linux installers are built by the **Build desktop installers** GitHub Actions workflow. It currently targets Windows x64, macOS Intel and Apple silicon, and Linux x86_64. To publish downloads, push a version tag such as `v1.0.0`; the workflow builds a Windows setup `.exe`, macOS `.dmg` images, and a Linux `.AppImage`, then attaches them to a GitHub Release. The [GitHub Pages download section](https://fanibhushan.github.io/ResumeStudio/) lists assets from the latest release, and the [Releases page](https://github.com/FaniBhushan/ResumeStudio/releases) lists all published versions. Running the workflow manually builds artifacts for download from Actions without publishing a release.

The app and PDF renderer are bundled. Optional AI features still require a separately installed and signed-in Codex CLI, Gemini CLI, or Claude Code. Windows installers are unsigned. macOS installers receive an ad-hoc signature to preserve the app bundle's integrity, but they are not trusted by Apple because they are not signed with a paid Developer ID certificate or notarized. On first open, macOS may say it cannot check the app for malicious software; use **System Settings → Privacy & Security → Open Anyway** after trying to open it. This should not show the separate “app is damaged” message; if it does, make sure you downloaded the newest release. To enable trusted macOS installers, configure all six secrets: `MACOS_CERTIFICATE_P12` (base64-encoded Developer ID Application `.p12` certificate), `MACOS_CERTIFICATE_PASSWORD`, `MACOS_SIGNING_IDENTITY` (the certificate's identity name), `APPLE_API_KEY_P8_BASE64` (base64-encoded App Store Connect API key), `APPLE_API_KEY_ID`, and `APPLE_API_ISSUER_ID`. The workflow then signs the app and notarizes and staples each DMG. A partial configuration fails the macOS job so it cannot silently publish a partially signed build.

### Install and run

- **Windows:** Download the Windows `.exe` and run it. Windows may show a SmartScreen warning because the installer is not code signed; continue only if you downloaded it from this project's Releases page.
- **macOS:** Download the image for your Mac (Apple silicon or Intel), open the `.dmg`, and drag Resume Studio into **Applications**. Open it once. For the “Apple cannot check it for malicious software” message, open **System Settings → Privacy & Security**, scroll to Security, and choose **Open Anyway** for Resume Studio. Confirm the prompt. This first-open override is needed because this free release is not notarized. If macOS says the app is damaged and moved it to the Bin, download the latest release; that indicates an older or invalid bundle.
- **Linux:** Download the `.AppImage`, make it executable (`chmod +x ResumeStudio-*.AppImage`), then run it (`./ResumeStudio-*.AppImage`). You may need FUSE 2 compatibility libraries for your distribution.

### Optional AI command-line tools

AI features are optional. Install Node.js/npm first, then install a provider and launch its command once to complete sign-in. Restart Resume Studio from a terminal where that command is available on `PATH`.

```bash
npm install -g @openai/codex@latest
npm install -g @google/gemini-cli
npm install -g @anthropic-ai/claude-code
```

Follow each provider's current setup guide: [Codex CLI](https://developers.openai.com/codex/cli/), [Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/installation.mdx), and [Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started). Provider access may require an account, plan, or API billing depending on the provider and authentication option you choose.

**Device support:** Resume Studio is designed for use in a desktop or laptop browser. The interface is not currently optimized for mobile screens.

Personal notes, imported resumes, and generated documents are stored locally in `data/` and `resumes/`; these folders are excluded from Git.

<p align="center"><a href="https://youtu.be/aEDAM6XIsAg"><img src="https://img.youtube.com/vi/aEDAM6XIsAg/hqdefault.jpg" alt="Watch the Resume Studio video" width="560"></a></p>

## What you can do

- **Build a CV:** edit your profile, summary, experience, achievements, education, certifications, skills, and links.
- **Start from an existing CV:** import RenderCV YAML, selectable-text PDF, DOCX, or TXT into editable fields. Scanned PDFs and legacy `.doc` files are not supported.
- **Refine with AI:** choose Codex CLI, Gemini CLI, or Claude Code for imports, wording suggestions, achievement grouping, and job-description alignment. Suggestions are reviewable before they change your draft.
- **Customize AI prompts:** edit the task-specific text files in `prompts/`; changes are loaded the next time the action runs.
- **Check ATS alignment:** optionally compare your CV with a job description and see matching terms, gaps, and targeted suggestions. ATS mode is off by default.
- **Preview and generate:** preview RenderCV templates with sample content, then use RenderCV to generate and download your CV PDF from the saved YAML.
- **Write a cover letter:** start with an existing CV or a description of your background, add a job description if useful, and edit the resulting draft.
- **Keep useful source files:** save career notes as Markdown alongside the structured RenderCV YAML and generated resume artifacts.

### Optional AI providers

AI features use a locally installed CLI and its existing sign-in. Install one provider below, then launch the CLI once and follow its sign-in prompts. Ordinary editing, saving, and PDF generation work without an AI provider.

| Provider | Install | First run and sign in |
| --- | --- | --- |
| [OpenAI Codex](https://developers.openai.com/codex/cli/) | `npm install -g @openai/codex@latest` | Run `codex` and choose an available sign-in method. |
| [Google Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/index.md) | `npm install -g @google/gemini-cli` | Run `gemini` and follow its authentication prompts. |
| [Anthropic Claude Code](https://code.claude.com/docs/en/getting-started) | `npm install -g @anthropic-ai/claude-code` | Run `claude` and follow the browser login prompts. |

Install Node.js and npm first. Gemini CLI requires Node.js 20 or newer; Claude Code's npm installation requires Node.js 22 or newer. Check availability with `node --version` and `npm --version`. After installing and signing in, start or restart Streamlit from a terminal where the provider command works, so the app inherits the correct `PATH`. Verify with `codex --version`, `gemini --version`, or `claude --version`.

The chosen CLI receives the text needed for the action you request, such as resume content and, when ATS mode is on, the job description. The app does not call provider APIs directly or store provider API keys.

## Typical workflow

1. Open **CV Builder** and load a YAML, PDF, DOCX, or TXT resume, or start a blank CV.
2. Review imported content and edit the fields. Add a profile photo if you want one.
3. Optionally choose an AI provider to refine text or categorize achievements. Review and accept suggestions individually.
4. Turn on ATS mode only when you want refinements aligned with a specific job description. Paste the description or load it from a supported text-based file.
5. Choose a template to preview it with sample data, then generate your CV PDF.
6. Use **Files** to download Markdown source notes or generated CV files.
7. Open **Cover Letter** to draft a letter from your CV and job description, or from your own background description.

Personal career notes under `data/` and imported or generated resumes under `resumes/` are local-only and gitignored. The repository includes a blank sample CV at `assets/sample_cv.yaml` for app defaults and template settings.

## Roadmap

### Planned

- Add support for connecting AI providers with user-supplied API keys.
- Add support for local language models served by [Ollama](https://ollama.com/).

### Long-term direction

- Build a web-based version with a Vue or React frontend and a Python backend exposed through an API.
- Offer a free local installer, with an optional paid AI assistant.

## Project map

```text
app.py                         Streamlit entry point and navigation
app_pages/                     CV Builder and Cover Letter views
src/cv_builder/                Import, storage, provider, and RenderCV logic
prompts/                       Editable AI prompt templates
assets/                        Resume Studio logo and visual assets
data/                          Local-only career notes (gitignored)
resumes/                       Local-only CV inputs and generated outputs (gitignored)
assets/sample_cv.yaml          Blank generic RenderCV starter configuration
tests/                         Provider adapter tests
requirements.txt               Python dependencies
architecture-plan.md           Detailed architecture and implementation notes
```

RenderCV is the CV rendering engine: Resume Studio prepares the RenderCV YAML, applies the selected RenderCV template, and invokes RenderCV to produce the PDF.

## Architecture and project video

- [Architecture plan](architecture-plan.md) describes the components, data flow, local AI CLI providers, RenderCV integration, and implementation decisions.
### High-level architecture

[Open the interactive architecture diagram](https://htmlpreview.github.io/?https://github.com/FaniBhushan/ResumeStudio/blob/main/.archify/architecture-resume-studio-20261010-231114/resume-studio-architecture.html)

![Resume Studio high-level architecture](assets/architecture-diagram.svg)

### User workflow

[Open the interactive workflow diagram](https://htmlpreview.github.io/?https://github.com/FaniBhushan/ResumeStudio/blob/main/.archify/workflow-resume-studio-20261010-231114/resume-studio-workflow.html)

![Resume Studio user workflow, including AI CLI cover letter generation and RenderCV PDF output](assets/workflow-diagram.svg)


## Run checks

```bash
python -m unittest discover -s tests -v
```

## Notes

- PDF import requires selectable text; OCR is not included.
- Phone numbers are optional. For best RenderCV validation, enter them as quoted international numbers, including the country code (for example, `+49...`).
- AI-generated text can be inaccurate. Check names, dates, technologies, and metrics before accepting or exporting a suggestion.
- See [the architecture plan](architecture-plan.md) for data flow, provider behavior, and planned follow-on tools.
