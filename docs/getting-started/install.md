---
title: Install Resume Studio on Windows, macOS, or Linux
description: Download and install the free Resume Studio CV builder on Windows, macOS Apple silicon or Intel, and Linux.
---

# Install Resume Studio

Resume Studio is a desktop app that opens in your browser and runs on your computer. Download the latest installer from the [home page](../index.md#downloads) or [GitHub Releases](https://github.com/FaniBhushan/ResumeStudio/releases).

| Operating system | Installer | Quick start |
| --- | --- | --- |
| Windows x64 | `.exe` | Run setup and follow the prompts. |
| macOS Apple silicon | `macOS-arm64.dmg` | Open the DMG and drag the app to **Applications**. [Read the security guide](macos.md). |
| macOS Intel | `macOS-x64.dmg` | Open the DMG and drag the app to **Applications**. [Read the security guide](macos.md). |
| Linux x86_64 | `.AppImage` | Follow the steps below. |

## Windows { #windows }

1. Download **ResumeStudio-Setup-Windows.exe** from the latest release.
2. Run the installer and follow its prompts.
3. Windows SmartScreen may warn because the installer is unsigned. Continue only if you downloaded it from the project's official Releases page and trust the source.

## macOS

1. Choose the correct build: Apple silicon (`arm64`) or Intel (`x64`).
2. Open the downloaded DMG.
3. Drag **Resume Studio** into **Applications**.
4. If macOS shows a security alert, follow the [macOS-specific guide](macos.md). The app is not notarized by Apple.

## Linux { #linux }

In a terminal, go to the folder containing the downloaded AppImage and run:

```bash
chmod +x ResumeStudio-*.AppImage
./ResumeStudio-*.AppImage
```

Some distributions require FUSE 2 compatibility libraries to run AppImages. Install them using your distribution's package manager if the app reports a FUSE error.

## When the app is open

Resume Studio opens its local workspace in your browser at `http://127.0.0.1:8501`. Closing the browser tab does not stop the server. When you are finished, quit the app from the Dock (macOS), taskbar (Windows), or application menu (Linux).

If clicking the app appears to do nothing, it may already be running. Check for the local page above, then quit the existing app process and launch it again. [See more troubleshooting answers](../guides/faq.md).
