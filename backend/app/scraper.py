"""Playwright-based scraper for SignUpGenius sign-up sheets.

A sheet has one or more slot *categories* (e.g. "Teacher Volunteers",
"Student Volunteers"), each rendered on its own line pair:

    Teacher Volunteers
    2 of 12 slots filled

    Student Volunteers
    All 25 slots filled

"All N slots filled" replaces "N of N slots filled" once a category is
completely full, so both phrasings need to be matched or full categories
get silently dropped. The exact markup can change between SignUpGenius
templates, so this matches on that "<name>\\n<count> slots filled" text
pattern rather than CSS classes -- verify against your actual sheets and
adjust `_extract_slots` if the wording differs.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

_CATEGORY_PATTERN = re.compile(
    r"^(?P<name>.+)\n(?:All (?P<full_count>\d+)|(?P<taken>\d+) of (?P<total>\d+))\s+slots?\s+filled\s*$",
    re.MULTILINE | re.IGNORECASE,
)


@dataclass
class ScrapedSlot:
    name: str
    slots_total: int
    slots_filled: int


@dataclass
class ScrapedEvent:
    title: str
    url: str
    slots: list[ScrapedSlot]


def _extract_slots(page_text: str) -> list[ScrapedSlot]:
    """Pull out every "<category name>" / "N of M slots filled" (or
    "All N slots filled") pair found in the page text."""
    slots = []
    for match in _CATEGORY_PATTERN.finditer(page_text):
        name = match.group("name").strip()
        if match.group("full_count") is not None:
            count = int(match.group("full_count"))
            slots.append(ScrapedSlot(name=name, slots_total=count, slots_filled=count))
        else:
            slots.append(
                ScrapedSlot(
                    name=name,
                    slots_total=int(match.group("total")),
                    slots_filled=int(match.group("taken")),
                )
            )
    return slots


def scrape_event(url: str) -> ScrapedEvent:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            # SignUpGenius keeps background requests (analytics, chat widget)
            # going indefinitely, so "networkidle" never fires. Wait for the
            # DOM instead, then give the SPA a bounded grace period to render.
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                pass
            title = page.title()
            body_text = page.inner_text("body")
        finally:
            browser.close()

    return ScrapedEvent(title=title, url=url, slots=_extract_slots(body_text))


def scrape_all(urls: list[str]) -> list[ScrapedEvent]:
    return [scrape_event(url) for url in urls]
