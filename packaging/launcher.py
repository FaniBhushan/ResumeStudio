"""PyInstaller entry point for the desktop app and its bundled RenderCV command."""

import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--rendercv":
        sys.argv = ["rendercv", *sys.argv[2:]]
        from rendercv.cli.entry_point import entry_point

        entry_point()
        return

    app_file = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1])) / "app.py"
    sys.argv = [
        "streamlit",
        "run",
        str(app_file),
        "--global.developmentMode=false",
        "--server.headless=false",
        "--server.address=127.0.0.1",
        "--server.port=8501",
        "--browser.serverPort=8501",
        "--browser.gatherUsageStats=false",
    ]
    from streamlit.web.cli import main as streamlit_main

    streamlit_main()


if __name__ == "__main__":
    main()
