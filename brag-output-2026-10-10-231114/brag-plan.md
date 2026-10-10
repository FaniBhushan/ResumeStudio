# Brag Plan: Resume Studio

## What is this app?
Resume Studio is a local Streamlit workspace for turning career notes into editable CVs, tailored application documents, and cover letters.

## The angle
Your experience stays yours: Resume Studio gives it a clear path from source material to an edited CV, an optional role alignment check, a rendered PDF, and a matching cover letter. The film follows that real flow with a fictional candidate and restrained, confident motion.

## Hook (first 2-3 seconds)
Open on a quiet, unfinished CV page. “Your story. One local workspace.” arrives, then the Resume Studio editor comes into view.

## Key moments (the middle)
- Load a CV from YAML, PDF, DOCX, or TXT and review the imported fields.
- Edit Profile, Experience, and Other sections; show an optional AI wording suggestion beside the original for review.
- Turn on ATS mode only when useful; show matched terms and gaps as a content-based alignment review.
- Preview a RenderCV template with sample content, then generate the PDF.
- Draft an editable cover letter from an existing CV or a background description.

## Outro / punchline
The finished CV and cover letter sit side by side under “Clear · Confident · Personal.” Close on the Resume Studio mark.

## User flow worth showing
Choose or import a CV → review and edit fields → optionally refine or align to a job → preview and generate a PDF → draft a matching cover letter.

## Tone
- Preset: polished
- Creative direction: quiet, confident product film for a personal writing workspace
- Interpretation: measured scene changes, crisp typography, real editor details, and a warm green/blue palette; UI movement supplies energy without hype.

## Format: landscape — 1920x1080
## Duration: 40 seconds (explicitly requested)

## Visual identity (from the project)
- Background: `#FAFCFB`
- Accent: `#18794E` (primary green), `#2563EB` (blue)
- Text: `#1F2D3D`
- Display font: system sans-serif (Streamlit theme)
- Body font: system sans-serif
- Strongest visual element: the CV Builder’s Profile / Experience / Other sections / Templates / ATS Checker / Files tabs, paired with its green document mark.
- Sample content: fictional “Avery Morgan”; no personal resume data from the repository is used.

## Share copy (draft)
Resume Studio turns career notes into an editable CV, a role-aware review when you want one, and a matching cover letter—all in one local workspace.

## Audio direction
- Role: warm, understated bed with a few soft interface accents
- Music: `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` (steady, clean)
- Music treatment: start under the opening; low-to-moderate level, fade in briefly and down over the final second.
- Music cue guidance: bundled cue preset at `composition/assets/music/cues/happy-beats-business-moves-vol-12-by-ende-dot-app.music-cues.json` (109.96 BPM). Strong cues near 8.74s, 17.47s, and 22.93s can guide UI reveals; detect the remaining beat grid at composition time for events after 25s.
- Audio-reactive treatment: unavailable in this environment (the extractor requires NumPy, which is not installed); skip rather than simulate an audio response.
- SFX posture: sparse, soft, motion-matched clicks and drops.
- Audio-coupled moments: import action; suggestion card settling; template/PDF result; cover letter landing.
- Restraint rule: no typewriter-key barrage or noisy transition effects; keep the read easy.

## Storyboard

### Scene 1 — Your story — 4s
A clean, open CV page and the line “Your story. One local workspace.” The Resume Studio mark appears as the real editor frame begins to form.
Sequential/interaction: the headline arrives first; editor chrome follows.
Audio intent: soft warm start.
Audio-coupled idea: one restrained reveal accent.
Music: steady bed begins gently.
Transition mood: soft slide → Scene 2

### Scene 2 — Start anywhere — 5s
Recreate the CV Builder source panel with a fictional `Avery_Morgan_CV.pdf`. Show the supported choices: YAML, PDF, DOCX, TXT. A simulated click loads it into the editor.
Sequential/interaction: file choice, then “Load into editor.”
Audio intent: a crisp but quiet UI tap.
Audio-coupled idea: land the editor reveal near the 4.39s cue; keep text settled.
Music: warm and steady.
Transition mood: clean wipe → Scene 3

### Scene 3 — Make it yours — 6s
Show Profile, Experience, and Other sections in the actual app’s tab style with fictional content. A summary suggestion appears beside “Current wording” for review.
Sequential/interaction: Profile → Experience tabs; suggestion card arrives after the field view.
Audio intent: quiet page movement and a soft suggestion-card landing.
Audio-coupled idea: card reveal near 8.74s; hold both original and suggestion long enough to read.
Music: steady, understated.
Transition mood: soft crossfade → Scene 4

### Scene 4 — Align when useful — 6s
Show the ATS mode toggle initially off, then a fictional “Product Engineer” job brief and a compact alignment result: “Matched terms” and “Terms to review.” Include the qualifier “Content-based review.”
Sequential/interaction: toggle on, then result panel appears.
Audio intent: subtle switch and result accent.
Audio-coupled idea: result lands near 17.47s; avoid implying a vendor-specific ATS score.
Music: stays beneath the UI.
Transition mood: clean wipe → Scene 5

### Scene 5 — Preview the page — 6s
Recreate the Templates view with a fictional sample CV preview and the selected “Classic” template. The copy says “Preview with sample CV content.”
Sequential/interaction: preview page slides in, then template label settles.
Audio intent: light page reveal.
Audio-coupled idea: preview reveal near 22.93s.
Music: gently lifts, without dominating.
Transition mood: soft slide → Scene 6

### Scene 6 — Save the finished CV — 7s
Show the “Save Markdown + YAML” and “Generate PDF” actions, then a fictional PDF page beside a small “Ready to download” state. Make clear that the PDF is produced from the saved YAML through RenderCV.
Sequential/interaction: save action, then PDF output appears.
Audio intent: measured confirmation, no exaggerated success sound.
Audio-coupled idea: two action beats, with a single soft completion cue.
Music: smooth, level bed.
Transition mood: crossfade → Scene 7

### Scene 7 — A matching letter — 6s
Show the Cover Letter page, an editable fictional draft, and a finished CV/letter pair. Close with “Clear · Confident · Personal” and the Resume Studio logo.
Sequential/interaction: letter page arrives, then logo lockup.
Audio intent: small logo accent and gentle final resolve.
Audio-coupled idea: fade the bed over the last second.
Music: resolves softly.
Transition mood: hold → end

**Music mood for this video:** polished, warm, steady.
**Audio summary:** a quiet business bed supports the edit, with sparse UI clicks and soft landings at meaningful product moments.
