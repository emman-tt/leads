from __future__ import annotations

"""Stage 2: website audit -> NONE / SOCIAL_ONLY / BROKEN / WEAK / OK.

Every flag carries evidence (metrics; optional lighthouse JSON + screenshot).
Uses requests only; Lighthouse/headless screenshot are best-effort extras.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import requests

from . import config
from .qualify import normalize_website, _extract  # reuse extraction

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium", shutil.which("chromium") or "",
]
SOCIAL_HOSTS = ("facebook.com", "fb.me", "m.me", "instagram.com", "linktr.ee",
                "bio.link", "tiktok.com", "wa.me", "youtube.com", "twitter.com", "x.com")

CTA_HINTS = ("book", "appointment", "order", "reserve", "buy now", "shop",
             "get started", "enquiry", "contact us", "get in touch")
MOMO_HINTS = ("momo", "mtn momo", "mobile money", "telecel cash", "airteltigo",
              "at money", "paystack", "hubtel", "pay online", "payment")
BOOKING_HINTS = ("booking", "book now", "reserve", "make appointment", "order online",
                 "cart", "checkout", "order form", "calendly", "whatsapp order")

EVIDENCE_DIR = Path(__file__).resolve().parent.parent / "data" / "evidence"


def _chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    return None


def screenshot(url: str, lead_key: str) -> str | None:
    """Best-effort 390x844 headless screenshot as audit evidence. None if no Chrome."""
    chrome = _chrome()
    if not chrome:
        return None
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    out = EVIDENCE_DIR / f"{lead_key}.png"
    try:
        subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--screenshot=" + str(out),
             "--window-size=390,844", "--virtual-time-budget=6000",
             "--hide-scrollbars", url],
            timeout=40, capture_output=True)
        return str(out) if out.exists() else None
    except Exception:
        return None


def lighthouse_performance(url: str) -> tuple[float | None, str | None]:
    """Run Lighthouse (mobile-throttled) if installed. Returns (perf_score, json_path)."""
    lh = shutil.which("lighthouse") or shutil.which("npx")
    if not lh or not _chrome():
        return None, None
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    out = EVIDENCE_DIR / "lighthouse"
    out.mkdir(exist_ok=True)
    json_path = out / (urlsplit(url).netloc.replace(".", "_") + ".json")
    try:
        cmd = ["lighthouse" if shutil.which("lighthouse") else "npx", "--", "lighthouse"] \
            if lh.endswith("npx") else ["lighthouse"]
        subprocess.run(cmd + [url, "--output=json", "--output-path=" + str(json_path),
                              "--quiet", "--chrome-flags=--headless",
                              "--only-categories=performance",
                              "--form-factor=mobile", "--screenEmulation.mobile"],
                       timeout=120, capture_output=True)
        if json_path.exists():
            data = json.loads(json_path.read_text())
            cat = data.get("categories", {}).get("performance", {})
            return round(cat.get("score", 0) * 100), str(json_path)
    except Exception:
        return None, None
    return None, None


def classify_status(website: str | None, socials: dict | None) -> str:
    """NONE / SOCIAL_ONLY / OK / (BROKEN|WEAK determined by audit results)."""
    if not website:
        if socials and any(s in socials for s in ("facebook", "instagram", "tiktok")):
            return "SOCIAL_ONLY"
        return "NONE"
    host = urlsplit(website).netloc.replace("www.", "")
    if any(host == s or host.endswith("." + s) or s in host for s in SOCIAL_HOSTS):
        return "SOCIAL_ONLY"
    return "unknown"  # needs live audit


def run_lighthouse(url: str, evidence: dict) -> None:
    per_score, json_path = lighthouse_performance(url)
    if per_score is not None:
        evidence["flags"].append({"flag": "lighthouse_perf",
                                  "metric": per_score,
                                  "weak": per_score < 50,
                                  "file": json_path})


def audit_business_v2(client, row) -> dict:
    """Stage 2 audit row-updater. Returns fields to write to businesses."""
    website = normalize_website(row["website"] or "")
    socials = json.loads(row["socials"] or "{}") if row.get("socials") else {}
    status = classify_status(website or None, socials)
    evidence = {"flags": [], "metrics": {}}
    evidence["metrics"]["phone"] = row["phone"]

    if status in ("NONE", "SOCIAL_ONLY"):
        score = 100 if status == "NONE" else 88
        return {"website_status": status, "weakness_score": score,
                "weakness_flags": json.dumps([status == "SOCIAL_ONLY" and "social_only" or "no_website"]),
                "evidence": json.dumps(evidence)}

    if not website:  # no url but flagged has_website
        return {"website_status": "BROKEN", "weakness_score": 85,
                "weakness_flags": json.dumps(["website_on_file_but_unreachable"]),
                "evidence": json.dumps(evidence)}

    out = audit_website(website, client)
    text = out.get("extract") or {}
    html_ok = bool(text)

    if not html_ok:
        evidence["flags"].append({"flag": "unreachable", "metric": out.get("error")})
        if row["phone"]:  # evidence screenshot still useful for a broken site
            screenshot(website, "e-" + str(row["source_id"]))
        return {"website": website, "website_status": "BROKEN", "weakness_score": 80,
                "weakness_flags": json.dumps(["site_unreachable"]),
                "evidence": json.dumps(evidence)}

    m = evidence["metrics"]
    m["title"] = text.get("title", "")[:100]
    m["text_len"] = text.get("text_len")
    m["load_time"] = out.get("load_time")
    m["https"] = out.get("scheme") == "https"
    full_html_flag_values = {"generator": text.get("generator", "")}

    def flag(name, weak, metric):
        evidence["flags"].append({"flag": name, "weak": bool(weak), "metric": metric})

    if out.get("scheme") != "https":
        flag("no_https", True, out.get("scheme"))
    if not text.get("viewport"):
        flag("not_mobile_friendly", True, "no viewport meta")
    if text.get("text_len", 0) < 1200:
        flag("thin_content", True, text.get("text_len"))
    full = ""  # page html kept out of extraction to remain schema light
    if not text.get("emails"):
        flag("no_contact_email", True, None)
    if not text.get("phones"):
        flag("no_phone_visible", True, None)
    if not text.get("socials"):
        flag("no_social_links", True, None)
    if out.get("load_time") and out.get("load_time") > 5.0:
        flag("slow_load", True, out.get("load_time"))
    if full_html_flag_values["generator"]:
        flag("template_generator", True, full_html_flag_values["generator"])

    # SEO basics
    if not m["title"] or len(m["title"]) < 10:
        flag("no_seo_title", True, m["title"])
    if not text.get("viewport"):  # viewport doubles as the common SEO signal
        flag("no_seo_basics", True, None)

    # CTA / booking / MoMo path: keyword scan over the real extracted text
    joined = (text.get("text", "") + " " + m["title"]).lower()
    has_cta = any(h in joined for h in CTA_HINTS)
    has_booking = any(h in joined for h in BOOKING_HINTS)
    has_momo = any(h in joined for h in MOMO_HINTS)
    m["has_cta"], m["has_booking"], m["has_momo"] = has_cta, has_booking, has_momo
    flag("no_clear_cta", not has_cta, None)
    flag("no_booking_or_order", not has_booking, None)
    flag("no_momo_payment", not has_momo, None)
    flag("no_whatsapp_button", not text.get("socials", {}).get("whatsapp") and "wa.me" not in joined, None)

    run_lighthouse(website, evidence)
    shot = screenshot(website, "e-" + str(row["source_id"]))
    if shot:
        evidence["screenshot"] = shot

    score, _flags = _score_from_flags(evidence["flags"])
    status = "WEAK" if score >= 30 else "OK"
    return {"website": website, "website_status": status, "weakness_score": score,
            "weakness_flags": json.dumps([f["flag"] for f in evidence["flags"] if f.get("weak")]),
            "evidence": json.dumps(evidence), "email": (text.get("emails") or [None])[0],
            "emails": json.dumps(text.get("emails") or []),
            "socials": json.dumps(text.get("socials") or {}),
            "images": json.dumps(text.get("images") or []),
            "videos": json.dumps(text.get("videos") or [])}


def _score_from_flags(flags: list[dict]) -> tuple[int, list[str]]:
    weights = {"no_https": 15, "not_mobile_friendly": 20, "thin_content": 10,
               "no_contact_email": 8, "no_phone_visible": 10, "no_social_links": 5,
               "slow_load": 8, "template_generator": 6, "park_like": 12,
               "no_seo_title": 6, "no_seo_basics": 5, "no_clear_cta": 8,
               "no_booking_or_order": 10, "no_momo_payment": 5,
               "no_whatsapp_button": 8, "lighthouse_perf": 12}
    score = 0
    out = []
    for f in flags:
        if f.get("weak"):
            score += weights.get(f["flag"], 5)
            if f["flag"] == "lighthouse_perf" and isinstance(f.get("metric"), (int, float)):
                score += int((50 - f["metric"]) / 50.0 * 12)
            out.append(f["flag"])
    return min(100, score), out
