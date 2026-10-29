from __future__ import annotations

"""Stage 5: per-lead output — dossier JSON, one-page markdown summary,
WhatsApp-first outreach draft in the lead's language, referencing one
specific observation from their audit evidence. Never a generic template.
"""
import json
from pathlib import Path

from .db import jloads, now, evidence_of
from . import config

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "briefs"

GREETINGS = {
    "tw": "Maakye! Ɛte sɛn?",
    "ga": "Ojekoo!",
    "ewe": "Miawoenam! Akpe na wo.",
    "ha": "Sannu! Barka da zuwa.",
    "en": "Hello!",
}


def first_observation(lead: dict) -> str:
    """The distinct, specific hook: evidence-based, not generic."""
    evidence = evidence_of(lead.get("evidence"))
    metrics = evidence.get("metrics", {})
    weak = [f for f in evidence.get("flags", []) if f.get("weak")]
    if lead.get("website_status") == "SOCIAL_ONLY":
        ig = (jloads(lead.get("socials"), {}) or {}).get("instagram")
        if ig:
            return f"your Instagram ({ig.split('instagram.com/')[-1]}) shows the craft but doesn't take bookings"
        return "customers meet you on Facebook but no page actually takes bookings"
    if lead.get("website_status") == "NONE" and lead.get("reviews_count"):
        return f"{lead['reviews_count']} people reviewed you, yet a Google search shows no website of yours"
    if lead.get("website_status") == "BROKEN":
        return f"your website ({lead.get('website')}) doesn't load for customers"
    if "not_mobile_friendly" in {f["flag"] for f in weak}:
        return "your website hides its text on phones — most of your customers browse on mobile data"
    if "no_booking_or_order" in {f["flag"] for f in weak}:
        return "there's no way to book or order on your site — customers who are ready to buy give up"
    if not metrics.get("has_momo", True):
        return "customers can't pay MoMo online even though that's how Ghanaians pay"
    if (lead.get("weakness_score") is not None and lead["weakness_score"] >= 55
            and lead.get("website_status") in ("WEAK", "OK", "BROKEN")):
        return f"your site takes {metrics.get('load_time') or 'ages'} to load on mobile data"
    cat = (jloads(lead.get("categories"), [None])[0] or lead.get("category") or "business")
    cat = cat.replace("_", " ")
    return (f"customers find your {cat} listing on {lead.get('city') or 'Google'}, "
            "but there is nothing behind it to browse or book — and no site of yours")


def outreach_draft(lead: dict) -> str:
    lang = lead.get("language") or "en"
    greet = GREETINGS.get(lang, GREETINGS["en"])
    obs = first_observation(lead)
    name = (lead.get("name") or "").split(" ")[0]
    cat = lead.get("category") or (jloads(lead.get("categories"), [None])[0] or "businesses")
    cat = cat.replace("_", " ")
    lines = [
        f"{greet} {name} —",
        f"I went through {lead.get('city') or 'Accra'} {cat} listing your business and noticed {obs}.",
        "I build one-page websites for businesses like yours: WhatsApp booking, MoMo payments, your best photos front and centre.",
        "I have already put together a free preview mockup based on your own photos — it is specific to your business, not a template.",
        "May I send the preview images here on WhatsApp? If it is not for you, just tell me and I will not message again.",
        "— Emmanuel, [Studio]",
    ]
    return "\n".join(lines)


def build_brief(conn, lead_row) -> dict:
    """Full Stage 5 JSON for one lead."""
    d = dict(lead_row)
    for col in ("images", "videos", "weakness_flags", "categories", "signals",
                "score_breakdown"):
        d[col] = jloads(d.get(col))
    d["evidence"] = evidence_of(d.get("evidence"))
    socials = jloads(d.get("socials"), {})
    if isinstance(socials, list):
        socials = {s.get("platform", "fb") if isinstance(s, dict) else "fb": s.get("url", "") if isinstance(s, dict) else str(s) for s in socials}
    d["socials"] = socials
    assets = [dict(a) for a in conn.execute(
        "SELECT url, poster_url, platform, type, res_w, res_h, quality, tags FROM assets WHERE lead_id=?",
        (d["id"],)).fetchall()]
    for a in assets:
        a["tags"] = jloads(a.get("tags"))
    selected = sorted(assets, key=lambda a: (-a["quality"], -(a["res_w"] or 0)))
    hero_ready = [a for a in selected if (a["res_w"] or 0) >= config.HERO_MIN_WIDTH]
    d["assets"] = selected[:15]
    d["assets_note"] = {
        "preview_only": True,
        "hero_worthy_count": len(hero_ready),
        "flagged_non_hero": [a["url"] for a in selected if (a["res_w"] or 0) < config.HERO_MIN_WIDTH][:5],
    }
    d["contacts"] = {
        "whatsapp": d.get("whatsapp"), "phone": d.get("phone"), "email": d.get("email"),
        "ig": d["socials"].get("instagram"), "fb": d["socials"].get("facebook"),
    }
    d["brand"] = {"colors": d["socials"].get("palette") or None,
                  "logo": d.get("logo_url"), "tagline": (d.get("description") or "")[:140]}
    d["outreach_draft"] = outreach_draft(d)
    return d


def one_page_summary(d: dict) -> str:
    sb = d.get("score_breakdown") or {}
    lines = [
        f"# {d['name']} — {d.get('city') or '?'} ({d.get('tier')}, {d.get('accept_score')} / 100)",
        "",
        f"- Category: {', '.join(d.get('categories') or []) or d.get('category') or '—'}",
        f"- Website: {d.get('website_status') or 'unknown'} — {d.get('website') or '—'} ({d.get('weakness_score')} weakness)",
        f"- Language: {d.get('language') or 'en'} · Area: {d.get('area') or '—'} · GhanaPost: {d.get('ghana_post') or '—'}",
        f"- Contacts: WA {d.get('whatsapp') or d.get('phone') or '—'} · {d.get('email') or '—'}",
        f"- Assets: {len(d.get('assets') or [])} previews (preview-only) · hero-ready {d['assets_note']['hero_worthy_count']}",
        "",
        "## Score factors",
        "- " + "\n- ".join(f"**{k}** {v['score']}/10 — {v['why']}" for k, v in sb.items()) if sb else "— disqualified:",
        f"  {d.get('reason') or '—'}",
        "",
        f"**Why pitch:** {d.get('reason') or '—'}",
        f"**Likely objection:** {d.get('objection') or '—'}",
        "",
        "## Outreach draft (WhatsApp)",
        "```",
        d.get("outreach_draft", "—"),
        "```",
    ]
    return "\n".join(lines)


def brief_dir(row) -> Path:
    """One folder per lead (keyed by stable row id), nested files inside."""
    return OUT_DIR / str(row["id"])


def migrate_legacy(conn) -> int:
    """One-time (idempotent): move flat <city>-<source_id>.{json,md} briefs
    into per-lead id folders so the tree is uniform and cli-deletable."""
    if not OUT_DIR.exists():
        return 0
    moved = 0
    for p in list(OUT_DIR.glob("*.json")) + list(OUT_DIR.glob("*.md")):
        key = p.stem.rsplit("-", 1)[-1]
        row = conn.execute("SELECT id FROM businesses WHERE source_id=? OR CAST(id AS TEXT)=?",
                           (key, key)).fetchone()
        if not row:
            continue
        dest = OUT_DIR / str(row["id"])
        dest.mkdir(parents=True, exist_ok=True)
        for sibling in (p.with_suffix(".json"), p.with_suffix(".md")):
            if sibling.exists():
                sibling.rename(dest / sibling.name)
                moved += 1
    for p in list(OUT_DIR.iterdir()):
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    return moved


def export_brief(conn, row) -> tuple[str, str]:
    d = build_brief(conn, row)
    bdir = brief_dir(row)
    bdir.mkdir(parents=True, exist_ok=True)
    json_path = bdir / "dossier.json"
    md_path = bdir / "summary.md"
    out_path = bdir / "outreach.txt"
    json_path.write_text(json.dumps(d, ensure_ascii=False, indent=2))
    md_path.write_text(one_page_summary(d), encoding="utf-8")
    out_path.write_text(d.get("outreach_draft", "—"), encoding="utf-8")
    return str(json_path), str(md_path)
