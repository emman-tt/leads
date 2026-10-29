from __future__ import annotations

"""Stage 3: project-acceptance score (0-100) with one-line reasons per factor.

Six factors, each scored 0-10, then weighted (config.WEIGHTS / weights table):
health(25%) readiness(20%) need(20%) pay(15%) reach(10%) assets(10%).
Hard disqualifiers short-circuit to score 0 + tier DISQUALIFIED.
"""
import json

from .db import get_weights, jloads, evidence_of
from . import config

GOV_NGO_TERMS = config.BLOCKLIST_TERMS


def _f0(reason): return 0, reason
def _r(score, reason): return max(0, min(10, score)), reason


def factor_health(row, signals: dict) -> tuple[int, str]:
    if signals.get("posts_30d") == 0:
        return _r(1, "no posts in last 30 days")
    if signals.get("posts_30d"):
        return _r(8, f"{signals['posts_30d']} posts in last 30 days")
    reviews = row["reviews_count"] or 0
    updated = signals.get("updated_ago_days")
    if reviews >= 10:
        return _r(8, f"{reviews} directory reviews suggest active trading")
    if reviews >= 3:
        return _r(6, f"{reviews} reviews, moderate activity")
    if updated and updated > config.INACTIVE_DAYS_DQ:
        return _f0(f"directory updated {updated}+ days ago — likely inactive")
    return _r(4, "thin activity data; treat as unverified active")


def factor_readiness(row, signals: dict) -> tuple[int, str]:
    socials = jloads(row["socials"], {})
    if isinstance(socials, list):  # legacy shape: [{platform, url}, ...]
        socials = {next(iter(s)) if isinstance(s, dict) else str(s): "" for s in socials}
    evidence = evidence_of(row["evidence"])
    metrics = evidence.get("metrics", {})
    same = [k for k in ("facebook", "instagram", "tiktok", "youtube") if socials.get(k)]
    wa = bool(socials.get("whatsapp")) or row["whatsapp"] is not None
    momo = bool(metrics.get("has_momo"))
    ads = bool(signals.get("runs_ads"))
    n = same.__len__()
    if momo and wa and n >= 1:
        return _r(9, "has MoMo path + WhatsApp Business + active socials")
    if wa and n >= 1:
        return _r(7, "WhatsApp Business live with socials")
    if wa or n >= 1:
        return _r(5, f"present on {max(n, 1)} channel(s) but sales funnel incomplete")
    return _r(2, "no meaningful digital storefront beyond directory")


def factor_need(row, signals: dict) -> tuple[int, str]:
    evidence = evidence_of(row["evidence"])
    metrics = evidence.get("metrics", {})
    reasons = []
    pts = 0
    if signals.get("questions_count", row["reviews_count"]) and row["reviews_count"] is not None:
        q = signals.get("questions_count") or 0
        if q >= 1:
            pts += 3
            reasons.append(f"{q} customer question(s) unanswered on listing")
    if not metrics.get("has_booking", True):
        pts += 3
        reasons.append("no booking or ordering flow found")
    elif row["website_status"] in ("NONE", "SOCIAL_ONLY"):
        pts += 2
        reasons.append("nowhere online to book or order — customers must call and hope")
    if not metrics.get("has_cta", True):
        pts += 2
        reasons.append("no clear call-to-action on their site")
    if row["reviews_count"] and row["reviews_count"] <= 3:
        pts += 1
        reasons.append("weak review/mapping visibility")
    if not reasons:
        return _r(3, "no strong need signal; site ~functional")
    grade = 8 if pts >= 4 else 6 if pts >= 3 else 5 if pts >= 2 else 4
    return _r(grade, "; ".join(reasons[:2]))


def factor_pay(row, signals: dict) -> tuple[int, str]:
    cats = jloads(row["categories"], [])
    premium = any(c in config.PREMIUM_CATEGORIES for c in cats)
    branches = signals.get("branch_count") or 1
    price_pts = signals.get("visible_prices", False)
    if premium and branches > 1:
        return _r(9, f"{', '.join(cats[:1])} business with {branches} locations")
    if premium or price_pts:
        return _r(7, f"premium category ({', '.join(cats[:1]) or 'n/a'})")
    if branches > 1:
        return _r(6, f"{branches} branches")
    return _r(4, "regular category; budget likely smaller")


def factor_reach(row, signals: dict) -> tuple[int, str]:
    if row["whatsapp"] or row["phone"]:
        return _r(8, "direct phone/WhatsApp on their listing")
    if jloads(row["socials"], {}):
        return _r(4, "socials DM only; owner identity unverified")
    if row.get("email"):
        return _r(5, "email only; slower decision path")
    return _r(2, "no working contact channel")


def factor_assets(row, signals: dict) -> tuple[int, str]:
    media = row["media_ready"]
    if media is None:
        imgs = len(jloads(row["images"], []))
        if imgs >= 8:
            return _r(8, f"{imgs} usable images on file")
        if imgs >= 3:
            return _r(6, f"{imgs} images on file; media pass pending")
        return _r(3, "too few quality images from public sources yet")
    if media >= 8:
        return _r(9, "media pass complete: hero + product shots + video")
    if media >= 4:
        return _r(6, "partial media; needs a shoot or more scraping")
    return _r(3, "media pass found too little usable material")


FACTORS = {
    "health": factor_health,
    "readiness": factor_readiness,
    "need": factor_need,
    "pay": factor_pay,
    "reach": factor_reach,
    "assets": factor_assets,
}


def hard_disqualifiers(row, signals: dict) -> list[str]:
    dq = []
    name = (row["name"] or "").lower()
    if any(t in name for t in GOV_NGO_TERMS):
        dq.append("government_or_ngo")
    if signals.get("updated_ago_days") and signals["updated_ago_days"] > config.INACTIVE_DAYS_DQ:
        dq.append("inactive_over_90_days")
    if row["website_status"] == "OK" and (row["weakness_score"] or 100) < 25:
        dq.append("already_strong_site")
    socials = jloads(row["socials"], {})
    if not (row["phone"] or row["whatsapp"] or row.get("email")
            or row.get("phone_e164")) and not socials:
        dq.append("no_working_contact")
    if row["opt_out"]:
        dq.append("opted_out")
    return dq


def reason_to_pitch(row, breakdown, signals) -> str:
    evidence = jloads(row["evidence"], {})
    flags = {f.get("flag") for f in evidence.get("flags", []) if f.get("weak")}
    top2 = sorted(breakdown.items(), key=lambda kv: kv[1].get("weighted", 0), reverse=True)[:2]
    parts = []
    if "not_mobile_friendly" in flags:
        parts.append("their website fights mobile users — that is where your customers are")
    if row["website_status"] in ("NONE", "SOCIAL_ONLY") and row["reviews_count"]:
        parts.append(f"{row['reviews_count']} happy directory reviews, but nobody can find you on a map search")
    if not parts and top2:
        parts.append(f"strongest selling point: {' and '.join(k.title() for k, _ in top2)}")
    if jloads(row["evidence"], {}).get("metrics", {}).get("no_momo_payment") is False:
        parts.append("you already accept MoMo — a store/booking page would close sales while you sleep")
    return "; ".join(parts[:2]) or "your online presence doesn't match the quality of your work"


def likely_objection(row, signals) -> str:
    if row["website_status"] == "SOCIAL_ONLY":
        return "our Facebook page is enough — counter with how many sales slip to booking-capable competitors"
    if row["website_status"] == "NONE":
        return "too expensive — counter with one-page price anchored to visible prices they display"
    if row["tier" if "tier" in row.keys() else "website_status"] == "WEAK":
        return "we paid for a website before — counter with our evidence page of what went wrong (screenshot in hand)"
    return "no time on the phone — send WhatsApp proof (screenshots) not paragraphs"


def score_business(conn, row) -> dict:
    """Stage 3 entry point. Returns write-set for businesses row."""
    signals = jloads(row["signals"], {})
    dq = hard_disqualifiers(row, signals)
    if dq:
        return {"accept_score": 0, "tier": "DISQUALIFIED", "score_breakdown": json.dumps({}),
                "objection": "n/a",
                "reason": " OR ".join(dq)}
    weights = get_weights(conn)
    if set(weights) != set(config.WEIGHTS):
        weights = config.WEIGHTS
    breakdown = {}
    total = 0.0
    for name, fn in FACTORS.items():
        s, why = fn(row, signals)
        w = weights.get(name, config.WEIGHTS[name])
        breakdown[name] = {"score": s, "weighted": round(s * w * 10, 2), "why": why}
        total += s * w * 10
    accept = round(min(100, total))
    tier = "A" if accept >= config.TIERS["A"] else ("B" if accept >= config.TIERS["B"] else "C")
    out = {
        "accept_score": accept,
        "tier": tier,
        "score_breakdown": json.dumps(breakdown),
        "reason": reason_to_pitch(row, breakdown, signals),
        "objection": likely_objection(row, signals),
    }
    return out
