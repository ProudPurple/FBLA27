from __future__ import annotations

import sys

import webview

from .api import Api
from .paths import frontend_dist_dir
from .scheduler import start_scheduler

DEV_SERVER_URL = "http://localhost:5173"


def resolve_ui_url() -> str:
    if "--dev" in sys.argv:
        return DEV_SERVER_URL

    index_html = frontend_dist_dir() / "index.html"
    if not index_html.exists():
        raise FileNotFoundError(
            f"{index_html} not found. Run `npm run build` in frontend/ first, "
            "or pass --dev to load the Vite dev server instead."
        )
    return str(index_html)


def main() -> None:
    api = Api()
    start_scheduler(api)

    webview.create_window("SignUpGenius Tracker", resolve_ui_url(), js_api=api, width=900, height=700)
    webview.start(debug="--dev" in sys.argv)


if __name__ == "__main__":
    main()
