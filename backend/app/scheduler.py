from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from . import config
from .api import Api


def start_scheduler(api: Api) -> BackgroundScheduler:
    """Periodically re-scrapes in the background so the UI can just read
    from SQLite. Runs alongside the manual refresh button in the UI."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        api.refresh_events,
        "interval",
        minutes=config.REFRESH_INTERVAL_MINUTES,
        next_run_time=None,  # first run is triggered manually / by the UI, not at startup
    )
    scheduler.start()
    return scheduler
