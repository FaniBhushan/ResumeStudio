---
title: Resume Studio desktop app FAQ and troubleshooting
description: Answers about Resume Studio's local server, free AI features, ATS review, RenderCV updates, and macOS installation alerts.
---

# Desktop app FAQ

??? faq-item "Does closing the browser tab quit Resume Studio?"
    No. The browser shows the local interface, while Resume Studio continues running in the background. Quit Resume Studio from the Dock (macOS), taskbar or Task Manager (Windows), or application menu (Linux) to stop the local server.

??? faq-item "Why does clicking the app appear to do nothing?"
    Resume Studio may already be running and using its local port. Check `http://127.0.0.1:8501`. If that page is not open, quit an existing Resume Studio process in your app or process manager, then launch the app again.

??? faq-item "Is Resume Studio free? Is the AI free?"
    The app is free and open source. AI support is optional and uses Codex CLI, Gemini CLI, or Claude Code that you install and authenticate. Provider account requirements, usage limits, and charges are set by each provider. [Set up an AI provider](../getting-started/ai-providers.md).

??? faq-item "Does the ATS checker give a score or guarantee a pass?"
    No. It compares CV content with a job description and returns matches, possible gaps, and reviewable suggestions. It does not predict a score from a specific ATS product or guarantee a particular result. [Read about the ATS review](ats-review.md).

??? faq-item "What happens when RenderCV changes?"
    Resume Studio uses RenderCV to validate CV data and generate PDFs. A RenderCV update can change supported YAML fields, theme output, or PDF layout. The desktop app includes a pinned version; upgrades should be reviewed for compatibility before a new app release. Existing CV YAML remains on your computer.

??? faq-item "What does the macOS security warning mean?"
    The “Apple cannot check it for malicious software” warning means the free app is not notarized. The “app is damaged and moved to the Bin” warning is different: stop and do not bypass it. [Read the macOS guide with screenshots](../getting-started/macos.md).

??? faq-item "Where are my files stored?"
    Resume Studio saves career notes and generated documents on your computer. It does not use a Resume Studio account or cloud database. AI actions send the relevant text to the provider CLI you selected; see the provider's privacy and account terms.
