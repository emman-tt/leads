from __future__ import annotations

"""Website audit: detect no-website / weak-website businesses and enrich them.

Scoring model (weakness_score, higher = worse opportunity):
  100           = no website at all at the source (hottest lead)
  site dead     = DNS failure / timeout / 5xx / parked  -> floor 55
  site alive    = graded 0..100 from the flags below

Flags (per alive site):
  no_https 15 | not_mobile 15 | thin_content 12 | no_phone 12 |
  no_email 10 | slow_load 8 | default_template 6 | no_socials 5 |
  park_like 12 | error_page 20
"""
import ipaddress
import re
import socket
import time
from urllib.parse import urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

from .http import USER_AGENT
from .db import jdumps

AUDIT_TIMEOUT = 15

SOCIAL_PATTERNS = {
    "facebook":  r"(?:https?://)?(?:www\.|m\.)?facebook\.com/(?![a-z.]*sharer|share\.php)([A-Za-z0-9_.\-/]+)",
    "instagram": r"(?:https?://)?(?:www\.)?instagram\.com/([A-Za-z0-9_.]+)",
    "twitter":   r"(?:https?://)?(?:www\.)?(?:twitter|x)\.com/([A-Za-z0-9_]+)",
    "linkedin":  r"(?:https?://)?(?:[a-z]{2,3}\.)?linkedin\.com/(?:company|in)/([A-Za-z0-9_\-/]+)",
    "tiktok":    r"(?:https?://)?(?:www\.)?tiktok\.com/@([A-Za-z0-9_.]+)",
    "youtube":   r"(?:https?://)?(?:www\.)?youtube\.com/(?:channel/|c/|user/|@)([A-Za-z0-9_\-@]+)",
    "pinterest": r"(?:https?://)?(?:www\.)?pinterest\.[a-z.]+/([A-Za-z0-9_.]+)",
    "snapchat":  r"(?:https?://)?(?:www\.)?snapchat\.com/add/([A-Za-z0-9_.]+)",
}
EMAIL_RE = re.compile(
    r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,14}"
)
BAD_EMAIL_HINTS = ("example.", "no-reply", "noreply", "sentry.", "godaddy",
                   "domain.", "email@", "yourdomain", "@2x", "u003", "wixpress")
IMG_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif", ".css", ".js")
PHONE_RE = re.compile(r"(?:\+233|0)\s?\d{2,3}[\s\-]?\d{3}[\s\-]?\d{3,4}")
TEMPLATE_GENERATORS = ("wix.com", "wordpress", "elementor", "godaddy", "squarespace",
                       "shopify", "jimdo", "webnode", "sitebuilder", "drupal")

CONTACT_HINT_PATHS = ("contact", "contact-us", "about", "about-us")


def normalize_website(raw: str) -> str | None:
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        url = raw
    elif re.match(r"^[\w.-]+\.[a-z]{2,}", raw, re.I):
        url = "https://" + raw
    else:
        return None
    parts = urlsplit(url)
    try:
        ipaddress.ip_address(parts.hostname)
        return None  # bare IP = probably a parked/junk entry, skip
    except ValueError:
        pass
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, "", ""))


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def _visible_text(soup: BeautifulSoup) -> str:
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return soup.get_text(" ", strip=True)


def _extract(page_html: str, base_url: str) -> dict:
    soup = _soup(page_html)
    text = _visible_text(soup)
    full = page_html
    emails = []
    for e in EMAIL_RE.findall(full):
        e = e.lower().strip(".")
        if len(e) > 60:
            continue
        if e.split("@")[0].lower().startswith(IMG_EXT):
            continue
        if any(h in e.lower() for h in BAD_EMAIL_HINTS):
            continue
        if e.endswith((".png", ".jpg", ".gif", ".webp", ".svg", ".webp")):
            continue
        if e not in emails:
            emails.append(e)
    phones = []
    for p in PHONE_RE.findall(text + " " + full):
        p = re.sub(r"\s+", " ", p).strip()
        if p not in phones:
            phones.append(p)
    socials = {}
    for name, pat in SOCIAL_PATTERNS.items():
        m = re.search(pat, full, re.I)
        if m:
            socials[name] = m.group(0)
    images = []
    og = soup.find("meta", property="og:image")
    if og and og.get("content", "").startswith("http"):
        images.append(og["content"])
    for img in soup.find_all("img", src=True)[:15]:
        src = img["src"]
        if src.startswith("http") and not src.lower().endswith(IMG_EXT + (".ico",)):
            if src not in images:
                images.append(src)
    videos = set()
    for m in re.finditer(
        r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/)[\w\-]{6,}"
        r"|youtu\.be/[\w\-]{6,}|vimeo\.com/\d+)", full, re.I):
        videos.add(m.group(0))
    for v in soup.find_all("video", src=True):
        videos.add(v["src"])
    return {
        "emails": emails[:10],
        "phones": phones[:5],
        "socials": socials,
        "images": images[:15],
        "videos": sorted(videos)[:10],
        "title": (soup.title.get_text(strip=True) if soup.title else "")[:200],
        "text_len": len(text),
        "viewport": bool(soup.find("meta", attrs={"name": re.compile("viewport", re.I)})),
        "generator": (soup.find("meta", attrs={"name": re.compile("generator", re.I)})
                      or {}).get("content", "").lower() if soup.find(
                          "meta", attrs={"name": re.compile("generator", re.I)}) else "",
        "text": text[:4000],
    }


def score_site(audit: dict, load_time: float, status: int, scheme: str) -> tuple[int, list[str]]:
    flags = []
    if scheme == "http":
        flags.append("no_https")
    if not audit["viewport"]:
        flags.append("not_mobile_friendly")
    if audit["text_len"] < 2000:
        flags.append("thin_content")
    if not audit["emails"]:
        flags.append("no_contact_email")
    if not audit["phones"]:
        flags.append("no_phone_visible")
    if not audit["socials"]:
        flags.append("no_social_links")
    if load_time > 5.0:
        flags.append("slow_load")
    if any(t in audit["generator"] for t in TEMPLATE_GENERATORS):
        flags.append("default_template")
    if audit["text_len"] < 500:
        flags.append("park_like")
    weights = {"no_https": 15, "not_mobile_friendly": 15, "thin_content": 12,
               "no_contact_email": 10, "no_phone_visible": 12, "no_social_links": 5,
               "slow_load": 8, "default_template": 6, "park_like": 12, "error_page": 20}
    return min(100, sum(weights.get(f, 5) for f in flags)), flags


def audit_website(website: str, client) -> dict:
    """Fetch the site (https first, fall back http; then /contact if thin)."""
    result = {"website": website, "status_code": None, "final_url": website,
              "load_time": None, "scheme": "https", "error": None}
    try:
        start = time.time()
        resp = client.session.get(website, timeout=AUDIT_TIMEOUT, stream=False,
                                  headers={"User-Agent": USER_AGENT})
        result.update(load_time=round(time.time() - start, 2),
                      status_code=resp.status_code,
                      final_url=resp.url, scheme=resp.url.split(":")[0])
        if resp.ok:
            result["extract"] = _extract(resp.text, str(resp.url))
            if result["extract"]["text_len"] < 1200:
                for path in CONTACT_HINT_PATHS:  # thin homepage -> try contact page
                    alt = website.rstrip("/") + "/" + path
                    try:
                        r2 = client.session.get(alt, timeout=AUDIT_TIMEOUT,
                                                headers={"User-Agent": USER_AGENT})
                        if r2.ok:
                            ex2 = _extract(r2.text, str(r2.url))
                            for k in ("emails", "phones", "socials", "videos", "images"):
                                if ex2[k]:
                                    result["extract"][k] = ex2[k]
                            if result["extract"]["text_len"] < len(ex2["text_len"] * " ") and \
                               result["extract"]["text_len"] < 3000:
                                result["extract"]["text_len"] = max(
                                    result["extract"]["text_len"],
                                    min(ex2["text_len"], 3000))
                    except requests.RequestException:
                        continue
        else:
            result["error"] = f"HTTP {resp.status_code}"
        return result
    except requests.SSLError:
        try:  # broken TLS -> try plain http, still counts as weak
            start = time.time()
            http_url = "http://" + urlsplit(website).netloc
            resp = client.session.get(http_url, timeout=AUDIT_TIMEOUT,
                                      headers={"User-Agent": USER_AGENT})
            result.update(load_time=round(time.time() - start, 2), scheme="http",
                          status_code=resp.status_code)
            if resp.ok:
                result["extract"] = _extract(resp.text, str(resp.url))
                return result
        except requests.RequestException as exc:
            result["error"] = str(exc)
        return result
    except (requests.ConnectionError, requests.Timeout, socket.gaierror) as exc:
        result["error"] = str(exc)
        return result


def classify(website: str | None, audit: dict | None) -> tuple[str, int, list[str]]:
    """Return (website_status, weakness_score, flags) for a business row."""
    if website is None:
        return "none", 100, ["no_website"]
    if audit is None:
        return "unknown", None, []
    if audit.get("status_code") is None or (audit.get("error") and not audit.get("extract")):
        return "dead", max(55, len(website) and 60 or 60), ["site_unreachable"]
    extract = audit["extract"]
    flags_score, flags = score_site(extract, audit.get("load_time") or 0,
                                    audit.get("status_code") or 0, audit.get("scheme", "https"))
    if audit.get("status_code") and audit["status_code"] >= 400:
        flags_score = min(100, flags_score + 20)
        flags.append("error_page")
    status = "weak" if flags_score >= 30 else "ok"
    return status, flags_score, flags


def audit_business(client, row) -> dict:
    """Full audit+enrichment for one business row (dict/sqlite3.Row)."""
    website = normalize_website(row["website"])
    out = {"website": None, "website_status": "unknown", "weakness_score": None,
           "weakness_flags": jdumps([])}
    if not website:
        out.update(website_status="none", weakness_score=100,
                   weakness_flags=jdumps(["no_website"]))
        return out
    audit = audit_website(website, client)
    status, score, flags = classify(website, audit)
    out.update(website=website, website_status=status, weakness_score=score,
               weakness_flags=jdumps(flags))
    ex = audit.get("extract")
    if ex:
        extras = {
            "emails": jdumps(ex["emails"]),
            "socials": jdumps(ex["socials"]),
            "images": jdumps([*ex["images"]]),
            "videos": jdumps(ex["videos"]),
        }
        if ex.get("emails"):
            extras["email"] = ex["emails"][0]
        # fill in a phone if the directory never recorded one
        if not row["phone"] and ex.get("phones"):
            extras["phone"] = ex["phones"][0]
        out.update(extras)
    return out
