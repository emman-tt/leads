from __future__ import annotations

"""Stage 2.5: find each lead's self-published social pages via search.

Enrichment only — leads are already in the DB from `scan`. Sources that
publish profiles themselves (Instagram / Facebook / Linktree / TikTok /
wa.me) surface first for businesses with no website, which is exactly the
class this pipeline pitches.

Engine: lite.duckduckgo.com — fetches only public result pages, verified
allowed by its robots.txt, keyless, and polite at 3.5s per query. Platform
pages are never scraped directly: profile URLs are lift-and-verify from
search results and matched against the business name before anything is
stored.
"""
import random
import re
import time
from urllib.parse import urlencode, unquote

_REDIRECT = re.compile(r'href=[\'"]([^\'"]+/l/\?uddg=([^\'"]+))')
_SOCIAL_HOSTS = ("instagram.com", "facebook.com", "linktr.ee", "wa.me",
                 "tiktok.com", "x.com", "twitter.com", "snapchat.com")
_QUERY_SITES = " OR ".join(f"site:{h}" for h in
                           ("instagram.com", "facebook.com", "linktr.ee", "wa.me"))
BASE = "https://lite.duckduckgo.com"

from .http import HttpError


def _decode(href: str) -> str | None:
    m = re.search(r"uddg=([^&]+)", href)
    if not m:
        return None
    url = unquote(m.group(1))
    # strip trailing '/about', '/videos' etc. into a clean profile root
    return url.split("?")[0].rstrip("/")


def parse_results(html: str) -> list[str]:
    """Result URLs, order preserved, deduped, social links only."""
    out, seen = [], set()
    for full_href, _ in _REDIRECT.findall(html):
        url = _decode(full_href)
        if not url or url in seen:
            continue
        seen.add(url)
        if any(h in url.lower() for h in _SOCIAL_HOSTS):
            out.append(url)
    return out


def _platform(url: str) -> str | None:
    low = url.lower()
    for host in _SOCIAL_HOSTS:
        if host in low:
            return {"linktr.ee": "linktree", "x.com": "twitter",
                    "wa.me": "whatsapp", "twitter.com": "twitter"}.get(host, host.split(".")[0])
    return None


def brand_match(url: str, tokens: set[str]) -> float:
    """How much of the business name shows up in the profile path (0..1)."""
    path = re.sub(r"[^a-z0-9]+", "", url.lower().split("://", 1)[-1])
    if not tokens:
        return 0.0
    hits = sum(1 for t in tokens if t in path)
    return hits / len(tokens)


def _lite_blocked(resp) -> bool:
    """DuckDuckGo soft-block signal: 202 with a challenge/consent payload that
    is not a result listing (its genuine result pages are plain 200s)."""
    if getattr(resp, "status_code", None) != 200:
        return True
    text = resp.text or ""
    return len(text) < 400 or "uddg=" not in text


def search_html(client, query: str) -> str:
    """One polite lite.duckduckgo.com query, jittered, block-aware."""
    time.sleep(random.uniform(0.4, 1.6))  # spreads bursts beyond the fixed delay
    resp = client.get(f"{BASE}/lite?{urlencode({'q': query})}")
    if _lite_blocked(resp):
        raise HttpError(
            "search engine soft-blocked us (202 challenge page, results withheld). "
            "Halt the stage now and cooldown: same-IP single queries were working "
            "minutes earlier, so wait a few hours and rerun slow batches.")
    return resp.text


def find_socials(client, name: str, city: str | None = None) -> list[dict]:
    """Search once for the lead; return ranked candidate list.

    Candidates carry url, platform and match; caller decides what to store.
    Raises HttpError on soft-blocks (caller should abort the whole stage).
    """
    q = f'"{name}" {city or ""} {_QUERY_SITES}'.strip()
    tokens = {t for t in re.findall(r"[a-z0-9]{3,}", name.lower())}
    cands = []
    for url in parse_results(search_html(client, q)):
        plat = _platform(url)
        cands.append({"url": url, "platform": plat, "match": round(brand_match(url, tokens), 2)})
    # strongest name matches first; one profile per platform
    cands.sort(key=lambda c: (-c["match"], c["platform"] or ""))
    dedup, out = set(), []
    for c in cands:
        if c["platform"] and c["platform"] in dedup:
            continue
        dedup.add(c["platform"])
        out.append(c)
    return out
