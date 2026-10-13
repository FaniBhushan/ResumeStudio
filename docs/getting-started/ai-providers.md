---
title: Set up Codex, Gemini CLI, or Claude Code for Resume Studio
description: Install and sign in to an AI provider CLI to use Resume Studio's optional CV import, writing suggestions, ATS alignment review, and cover letter features.
---

# Set up an optional AI provider

AI features are optional. Ordinary CV editing, saving, and PDF generation work without an AI provider.

Resume Studio sends the text needed for an AI action to the provider CLI you choose. For an ATS review, this includes your CV content and target job description. The app does not call provider APIs directly or store provider API keys. Check your provider's account terms, privacy policy, usage limits, and billing before using it.

## Before you install

Install **Node.js and npm** using the official [Node.js download page](https://nodejs.org/en/download). Check that both commands work:

```bash
node --version
npm --version
```

Follow the selected provider's current system requirements. Gemini CLI currently requires Node.js 20 or newer; [Gemini's setup guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/index.md) has the latest details.

## Choose a provider

| Provider | Install command | First sign-in |
| --- | --- | --- |
| [OpenAI Codex CLI](https://developers.openai.com/codex/cli/) | `npm install -g @openai/codex@latest` | Run `codex` and follow its authentication prompts. |
| [Google Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/index.md) | `npm install -g @google/gemini-cli` | Run `gemini` and choose an authentication option. |
| [Anthropic Claude Code](https://docs.anthropic.com/en/docs/claude-code/getting-started) | `npm install -g @anthropic-ai/claude-code` | Run `claude` and follow its sign-in prompts. |

Open the provider CLI once and finish sign-in. Verify the command is available:

```bash
codex --version
gemini --version
claude --version
```

You only need to verify the provider you installed. Start or restart Resume Studio from an environment where that command is on your `PATH`. The app inherits the environment from the process that launched it.

## Provider access and costs

Resume Studio does not bundle a model or provider subscription. The provider may require an account, a paid subscription, API billing, or may offer usage subject to its own limits. Check the provider's current terms before sending career or job-search information.
