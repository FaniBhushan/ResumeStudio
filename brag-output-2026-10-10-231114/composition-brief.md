# Hyperframes Composition Brief: Resume Studio

## Objective
Create a polished 40-second launch-style video for Resume Studio, a local CV and cover letter workspace.

## Output
- Composition directory: `brag-output-2026-10-10-231114/composition/`
- Rendered video: `brag-output-2026-10-10-231114/brag.mp4`
- Format: landscape — 1920x1080
- Duration: 40 seconds (user requested this length)

## Source Material
- Project root: `/Users/fanibhushan/ResumeStudio`
- Primary files read: `app.py`, `app_pages/cv_builder.py`, `app_pages/cover_letter.py`, `src/cv_builder/importing.py`, `src/cv_builder/processes.py`, `src/cv_builder/storage.py`, `README.md`, `.streamlit/config.toml`, `assets/resume-studio-logo.svg`
- Product name: Resume Studio
- Tagline / strongest claim: “Build a thoughtful CV, tailor it to a role, and create a matching cover letter — all in one local workspace.”
- Key UI moment to recreate: CV Builder tabs and actions, with the Cover Letter editor as the payoff.
- Copy that must appear verbatim:
  - “Your story. One local workspace.”
  - “Preview with sample CV content.”
  - “Clear · Confident · Personal”
- Use only fictional candidate “Avery Morgan”; do not display names, contact information, career details, or screenshots from repository resume data.

## Creative Direction
- Tone preset: polished
- Creative direction: quiet, confident product film for a personal writing workspace
- Interpretation: measured scene changes, crisp typography, real editor details, and warm green/blue brand colors.
- Angle: Your experience stays yours while Resume Studio helps move it from source material to an edited CV, optional role alignment, PDF output, and matching cover letter.
- Hook: “Your story. One local workspace.” over an open CV page.
- Outro / punchline: CV and editable cover letter sit together beneath “Clear · Confident · Personal.”
- Avoid: personal resume data; generic SaaS language; vendor-specific ATS claims; abstract filler; exaggerated AI/autopilot claims.

## Visual Identity
- Background: `#FAFCFB`
- Text: `#1F2D3D`
- Accent: `#18794E` green and `#2563EB` blue
- Display font: system sans-serif
- Body font: system sans-serif
- Visual references: actual Resume Studio logo mark; CV Builder tabs (`Profile`, `Experience`, `Other sections`, `Templates`, `ATS Checker`, `Files`); source upload, review suggestion, template preview, PDF and cover letter views.

## Storyboard
Use `brag-plan.md` as the complete creative contract.

1. Your story — 4s — opening hook and editor frame.
2. Start anywhere — 5s — supported source formats and simulated file load.
3. Make it yours — 6s — profile/experience editing and reviewable suggestion.
4. Align when useful — 6s — opt-in ATS mode and content-based findings.
5. Preview the page — 6s — template preview with sample content.
6. Save the finished CV — 7s — Markdown/YAML save and RenderCV PDF.
7. A matching letter — 6s — editable cover letter and brand outro.

## Audio
- Audio role: warm, understated bed with sparse interface accents.
- Audio arc: light start, soft clicks/drops on import and output moments, gentle resolution.
- Music: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3`
- Music treatment: low-to-moderate level, brief fade-in and final fade-down.
- Music cue guidance: bundled preset `assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json`; use 8.74s, 17.47s and 22.93s as optional cue hints. Detect beats for later scenes.
- Audio-reactive treatment: skipped because the HyperFrames extractor could not run (`numpy` is unavailable); do not simulate a response.
- Audio-coupled moments: import click; suggestion card landing; template/PDF reveal; final logo.
- SFX guidance: use bundled soft click/drop/impact assets sparingly, with motion-matched timing.
- SFX analysis guidance: `/Users/fanibhushan/.codex/plugins/cache/brag/brag/0.4.0/skills/brag/assets/sfx/sfx-analysis.md`.
- Audio files: all selected music/SFX are copied under `composition/assets/`.

## Hyperframes Instructions
- Build one seek-safe standalone composition with the current HyperFrames contract.
- Show actual app labels and actions, recreated with fictional content.
- Keep all copy readable and grounded in source files.
- This requested 40-second duration overrides the default brag length.
- Run `hyperframes check` before preview; review the final preview before rendering.
- Keep creation and rendering local.
