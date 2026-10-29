from __future__ import annotations

"""Stage 4: media enrichment for tier A/B leads.

Sources: business's own site (og/img), plus official-API socials when tokens
are configured (FB Graph / IG / TikTok). No login bypassing, no rate-limit
evasion. Everything stored as preview-only, with the business's own links.
"""
import io
import json
import re
import struct
from pathlib import Path

import requests

from . import config
from .db import jdumps, now

VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com")
WM_HINTS = ("shutterstock", "getty", "watermark", "stockadobe", "istock", "canva")


def _image_dims(data: bytes) -> tuple[int, int] | None:
    """Minimal JPEG / PNG dimension parser (no external deps)."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        if len(data) > 24 and data[12:16] == b"IHDR":
            w, h = struct.unpack(">II", data[16:24])
            return int(w), int(h)
        return None
    if data[:2] == b"\xff\xd8":  # JPEG segment walk
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return int(w), int(h)
            if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
            i += 2 + seg_len
        return None
    return None


def quality_score(w: int | None, h: int | None, nbytes: int, name_or_alt: str = "") -> int:
    """0-10 heuristic: resolution + weight; penalize stock-watermark names."""
    s = 3
    if w and h:
        s += 4 if min(w, h) >= 1080 else (2 if min(w, h) >= 720 else 0)
        if w * h >= 2_500_000:
            s += 1
    if nbytes > 250_000:
        s += 2
    elif nbytes > 80_000:
        s += 1
    if any(x in name_or_alt.lower() for x in WM_HINTS):
        s = min(s, 2)
    return max(0, min(10, s))


def tag_asset(name_or_alt: str, kind: str) -> list[str]:
    low = (name_or_alt or "").lower()
    tags = []
    if "team" in low or "staff" in low:
        tags.append("team")
    if "interior" in low or "shop" in low or "studio" in low or kind == "video":
        tags.append("interior")
    if "menu" in low or "price" in low or "product" in low or "service" in low:
        tags.append("product")
    if "review" in low or "testimonial" in low:
        tags.append("testimonial")
    return tags or ["product"]


def collect_from_site(href: str, images: list[str], videos: list[str], conn, lead_id: int,
                      session: requests.Session, limit: int = 20) -> list[int]:
    """Fetch resolution metadata for each candidate asset and store rows."""
    added = []
    for url in (images[:limit]):
        if not url.startswith("http"):
            continue
        meta_name = url.rsplit("/", 1)[-1][:120]
        nbytes, wh = 0, None
        try:
            r = session.get(url, timeout=12, stream=True)
            chunk = next(r.iter_content(300_000), b"")
            nbytes = int(r.headers.get("content-length", 0)) or len(chunk)
            wh = _image_dims(chunk if len(chunk) >= nbytes else _read_full(r))
        except requests.RequestException:
            continue
        finally:
            try:
                r.close()
            except Exception:
                pass
        if not wh:
            continue
        w, h = wh
        q = quality_score(w, h, nbytes, meta_name)
        tags = tag_asset(meta_name, "image")
        if min(w, h) >= config.HERO_MIN_WIDTH and q >= 7:
            tags.insert(0, "hero-worthy")
        conn.execute(
            "INSERT INTO assets (lead_id, url, platform, type, res_w, res_h, bytes, quality, tags, preview_only, created_at)"
            " VALUES (?,?,?,?,?,?,?,?,?,1,?)",
            (lead_id, url, "website", "image", w, h, nbytes, q, jdumps(tags), now()))
        added.append(1)
    for v in (videos or [])[:5]:
        poster = None
        m = re.search(r"(?:youtu\.be/|v=)([\w\-]{6,})", v)
        if m:
            poster = f"https://img.youtube.com/vi/{m.group(1)}/hqdefault.jpg"
        conn.execute(
            "INSERT INTO assets (lead_id, url, poster_url, platform, type, preview_only, created_at)"
            " VALUES (?,?,?,?,?,1,?)",
            (lead_id, v, poster, "website", "video", now()))
        added.append(1)
    return added


def _read_full(r) -> bytes:
    buf = io.BytesIO()
    for chunk in r.iter_content(65536) or []:
        buf.write(chunk)
    return buf.getvalue()


def collect_social(conn, row, session):
    """Official-API only adds: no tokens -> skip quietly (compliance-first)."""
    added = []
    socials = json.loads(row["socials"] or "{}")
    if config.FB_GRAPH_TOKEN:
        page = _fb_page_id_from_url(socials.get("facebook", ""))
        if page:
            added.append(_facebook_photos(conn, row, page, session))
    if config.IG_TOKEN:
        added.append(_instagram_media(conn, row, session))
    return added


def _fb_page_id_from_url(url: str) -> str | None:
    m = re.search(r"facebook\.com/([A-Za-z0-9_.\-]+)", url or "")
    return m.group(1) if m and m.group(1) not in ("policies", "help", "sharer") else None


def _facebook_photos(conn, row, page: str, session) -> list[int]:
    try:
        r = session.get(f"https://graph.facebook.com/{page}/picture?type=normal",
                        params={"access_token": config.FB_GRAPH_TOKEN,
                                "redirect": "false"}, timeout=15)
        data = r.json()
        url = data.get("data", {}).get("url")
        if url:
            conn.execute(
                "INSERT INTO assets (lead_id, url, platform, type, quality, tags, preview_only, created_at)"
                " VALUES (?,?,?,?,?,?,1,?)",
                (row["id"], url, "facebook", "image", 4, jdumps(["logo"]), now()))
            return [1]
    except Exception:
        return []
    return []


def _instagram_media(conn, row, session) -> list[int]:
    try:
        r = session.get(
            "https://graph.instagram.com/me/media",
            params={"fields": "id,media_url,media_type,permalink,thumbnail_url",
                    "access_token": config.IG_TOKEN}, timeout=15)
        payload = r.json()
    except Exception:
        return []
    added = []
    for item in (payload.get("data") or [])[:15]:
        url = item.get("media_url")
        if not url:
            continue
        conn.execute(
            "INSERT INTO assets (lead_id, url, poster_url, platform, type, preview_only, created_at)"
            " VALUES (?,?,?,?,?,1,?)",
            (row["id"], url, item.get("thumbnail_url"), "instagram",
             "video" if item.get("media_type") in ("VIDEO", "CAROUSEL_ALBUM") else "image", now()))
        added.append(1)
    return added


def update_media_ready(conn, row) -> int:
    n = conn.execute(
        "SELECT COUNT(*) c FROM assets WHERE lead_id=? AND preview_only=1", (row["id"],)).fetchone()["c"]
    conn.execute("UPDATE businesses SET media_ready=?, media_at=? WHERE id=?",
                 (n, now(), row["id"]))
    return n
