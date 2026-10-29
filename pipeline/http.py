from __future__ import annotations

"""Polite HTTP client: single worker, delays, retries, real browser UA.

Scrapes only public directory pages, throttled to stay gentle on the source.
If the site starts returning 403 (Cloudflare blocking), we stop and tell the
user to wait / reduce frequency rather than trying to evade protection.
"""
import time
import random
import requests

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

DEFAULT_DELAY = 1.5          # seconds between requests to the same host
RETRIES = 2
TIMEOUT = 20


class HttpError(Exception):
    pass


class Client:
    def __init__(self, delay: float = DEFAULT_DELAY):
        self.delay = delay
        self._last_hit = 0.0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def _throttle(self):
        gap = time.time() - self._last_hit
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last_hit = time.time()

    def get(self, url: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", TIMEOUT)
        last_exc = None
        for attempt in range(RETRIES + 1):
            self._throttle()
            try:
                resp = self.session.get(url, **kwargs)
                if resp.status_code in (403, 429):
                    raise HttpError(
                        f"Source refused request ({resp.status_code}). "
                        "Rate limited or blocked — stop, wait a few hours, then rerun."
                    )
                return resp
            except (requests.ConnectionError, requests.Timeout) as exc:
                last_exc = exc
                time.sleep(2 * (attempt + 1))
        raise HttpError(f"Failed after {RETRIES + 1} attempts: {url} ({last_exc})")
