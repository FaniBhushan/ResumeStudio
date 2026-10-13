---
title: Build a CV and export a RenderCV PDF
description: Create or import a CV in Resume Studio, preview a template, and generate a PDF using RenderCV.
---

# Build a CV and export a PDF

Resume Studio helps you maintain your career information and generate a PDF CV from structured RenderCV YAML.

## Start a CV

- Start from the blank CV in the app, or
- Import RenderCV YAML, a selectable-text PDF, DOCX, or TXT file.

Scanned PDFs and legacy `.doc` files are not supported. Review imported information before saving it.

## Edit and save

Add your profile, summary, roles, achievements, education, certifications, skills, and links. Resume Studio stores your notes and generated files locally. AI suggestions are optional and remain reviewable before they change a draft.

## Choose a template and render

The template chooser currently previews **nine built-in RenderCV themes** with sample content. Preview information is fictional; your personal CV is not used for the sample preview. Pick a theme, save your CV, and generate the PDF.

The app preserves RenderCV design settings from imported YAML, including a theme not shown among the built-in choices. Bringing a separate custom Typst/Jinja theme folder into the desktop app is not currently supported.

RenderCV validates the YAML and creates the PDF. You can download the generated PDF and source files from the app's Files view.

## Files and privacy

The app has no account or database. Career notes, imported files, and generated documents are saved on your computer. If you choose an AI action, the relevant text is sent to the selected provider CLI; see the [AI-assisted ATS review privacy details](ats-review.md#privacy-and-provider-use).
