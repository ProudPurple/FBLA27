"""Filesystem locations that need to work both in dev and frozen (PyInstaller) builds."""

import sys
from pathlib import Path

APP_NAME = "SignUpGeniusTracker"


def user_data_dir() -> Path:
    """Writable per-user directory for the SQLite DB, separate from the (often
    read-only, e.g. Program Files) install location of a packaged .exe."""
    import os

    base = os.environ.get("LOCALAPPDATA") or Path.home() / ".local" / "share"
    path = Path(base) / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def frontend_dist_dir() -> Path:
    """Location of the built React app, relative to the .exe when frozen or
    the repo layout when running from source."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "frontend_dist"  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent.parent / "frontend_dist"
