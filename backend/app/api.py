from __future__ import annotations

from datetime import datetime

from . import config
from .db import SignupEvent, SignupSlot, get_session, init_db
from .scraper import scrape_all


class Api:
    """Methods on this class are exposed to the frontend as
    `window.pywebview.api.<method>()`, called via `js_api` in main.py."""

    def __init__(self) -> None:
        init_db()

    def ping(self) -> str:
        return "pong"

    def list_events(self) -> list[dict]:
        with get_session() as session:
            events = session.query(SignupEvent).order_by(SignupEvent.title).all()
            return [event.to_dict() for event in events]

    def refresh_events(self) -> list[dict]:
        scraped = scrape_all(config.SIGNUP_GENIUS_URLS)
        now = datetime.now()

        with get_session() as session:
            for item in scraped:
                event = session.query(SignupEvent).filter_by(url=item.url).one_or_none()
                if event is None:
                    event = SignupEvent(url=item.url)
                    session.add(event)
                event.title = item.title
                event.last_synced = now
                # Replace the whole slot list rather than diffing -- category
                # names/counts can change between scrapes, and cascade
                # delete-orphan cleans up the old rows.
                event.slots = [
                    SignupSlot(name=slot.name, slots_total=slot.slots_total, slots_filled=slot.slots_filled)
                    for slot in item.slots
                ]
            session.commit()

            events = session.query(SignupEvent).order_by(SignupEvent.title).all()
            return [event.to_dict() for event in events]
