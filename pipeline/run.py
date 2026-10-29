"""CLI: python -m pipeline.run <command>

Commands (each idempotent + resumable):
  scan       discovery (GhanaYello + BusinessGhana corroboration -> normalize -> dedupe)
  audit      stage 2 website audit (NONE/SOCIAL_ONLY/BROKEN/WEAK/OK + evidence)
  score      stage 3 acceptance score -> tier A/B/C (+ hard disqualifiers)
  media      stage 4 enrichment for tier A/B (preview-only assets)
  brief      stage 5 dossier per lead (JSON + one-pager + outreach draft)
  export     CSV (filters: --city --category --tier --min-assets)
  status     counts + tier table
  leads      top-lead view (--country ghana|kenya|nigeria; opted-out leads never listed)
  optout     add opt-out (honoured permanently; accepts #id, source:id, +phone or name part)
  outcome    log campaign outcome + recalibrate weights (needs >=10 outcomes)
"""
from __future__ import annotations
import warnings

# The venv's urllib3 screams about LibreSSL on every run (Python 3.9 on macOS
# ships system LibreSSL). Harmless: requests still negotiate TLS fine. Silence
# it during import, then permanently for later emissions.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import urllib3  # noqa: F401
    try:
        from urllib3 import NotOpenSSLWarning  # type: ignore[attr-defined]
        warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
    except ImportError:
        warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")

import json
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus


def _elapsed(t0: float) -> str:
    s = int(time.monotonic() - t0)
    return f"{s // 60:02d}:{s % 60:02d}"


def _progress(t0: float, src: str, msg: str) -> None:
    """Streaming ticker so long, polite crawls visibly stay alive."""
    print(f"[scan {_elapsed(t0):>6} | {src:>7}] {msg}", flush=True)

from . import db as store
from . import config, geo
from .http import Client, HttpError
from .ghanayello import list_categories, scrape_category, scrape_profile
from .sources_local import search_query as classifieds_search, profile_details, RobotsBlocked
from . import sources_local
from .sources_local import cards_kenya, kenya_profile_details, kenya_category
from .sources_local import cards_nigeria, nigeria_profile_details, nigeria_category
from .sources_local import cards_ngex, ngex_profile_details, ngex_category
from .sources_local import NGEX_BASE, NGEX_TERMS
from .audit import audit_business_v2
from .scoring import score_business
from . import media as media_mod
from .brief import export_brief, migrate_legacy, OUT_DIR as BRIEF_DIR
from .db import log, jdumps, jloads, now

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "exports"


def cmd_scan(args):
    country = (args.country or config.DEFAULT_COUNTRY).lower()
    if country not in config.COUNTRIES:
        raise SystemExit(f"unknown country '{country}' — known: {', '.join(config.COUNTRIES)}")
    if not config.COUNTRIES[country].get("scannable", True):
        raise SystemExit(
            f"{country}: no robots-compliant bulk source wired yet (all candidates "
            f"probed blocked). Kenya is live; retry Nigeria when a compliant "
            f"directory appears or a Google Programmable Search key is added.")

    if country == "kenya":
        return _scan_kenya(args, country)
    if country == "nigeria":
        return _scan_nigeria(args, country)
    return _scan_ghana(args, country)


def _scan_ghana(args, country="ghana"):
    t0 = time.monotonic()
    client = Client(delay=config.RATE_LIMITS["ghanayello"])
    cats = [args.category] if args.category else config.CATEGORIES[: args.limit or len(config.CATEGORIES)]
    total = added = 0
    cities = [args.city] if args.city else list(config.CITIES)
    _progress(t0, "boot", f"ghana: {len(cats)} categories x {len(cities)} cities"
              f" (politeness {config.RATE_LIMITS['ghanayello']}s ghayello /"
              f" {config.RATE_LIMITS['businessghana']}s businessghana)")
    with store.db() as conn:
        store.set_weights(conn)
        for slug in cats:
            for city in cities:
                _progress(t0, "yello", f"fetching {slug}/{city} …")
                try:
                    cards, total_in = scrape_category(client, slug, city=args.city and city, max_pages=args.pages)
                except Exception as exc:
                    store.source_log_failure(conn, "ghanayello", slug + "/" + city, str(exc))
                    _progress(t0, "yello", f"!! {slug}/{city}: {exc}")
                    continue
                _progress(t0, "yello", f"{len(cards)} cards from {slug}/{city}")
                for card in cards:
                    total += 1
                    card["categories"] = [slug]
                    card.setdefault("phone", None)
                    card["phone_e164"] = geo.normalize_phone(card.get("phone"))
                    card["area"] = geo.infer_area(card.get("address") or "", city or "")
                    card["ghana_post"] = geo.extract_ghana_post(card.get("address") or "")
                    card["language"] = "en"  # English listing copy default
                    card["source_of"] = "ghanayello"
                    card["area_key"] = f"{(city or '').lower()}|{(card.get('area') or '').lower()}"
                    card["dedupe_key"] = store.dedupe_key(card["phone_e164"], card["name"], card.get("area"))
                    if store.is_opted_out(conn, {"phone_e164": card["phone_e164"], "opt_out": 0,
                                                 "brand_key": store.brand_key(card["name"]),
                                                 "source_id": str(card["source_id"])}):
                        continue
                    dup = store.find_duplicate(conn, card)
                    if dup:  # merge phone/socials into the existing record instead
                        if not dup["phone_e164"] and card["phone_e164"]:
                            conn.execute("UPDATE businesses SET phone_e164=?, dedupe_key=? WHERE id=?",
                                         (card["phone_e164"], card["dedupe_key"], dup["id"]))
                        continue
                    row_id = store.upsert_business(conn, card)
                    added += 1
                    if added <= 3 or added % 5 == 0:
                        _progress(t0, "yello", f"new #{added} (id {row_id}): {str(card['name'])[:34]}")
                    if args.profiles and row_id:
                        _fetch_profile(conn, client, card)
            # second-source sweeps (robots-respecting; failures logged per source)
            # businessghana: real company directory, always on unless skipped;
            # tonaton/jiji: consumer classifieds, opt-in only (--classifieds)
            sources = ["businessghana"]
            if getattr(args, "classifieds", False):
                sources += ["tonaton", "jiji"]
            if not args.no_second_source:
                for source in sources:
                    try:
                        s_client = Client(delay=config.RATE_LIMITS[source])
                        _progress(t0, source, f"searching {slug} (national pass)…")
                        for card in classifieds_search(source, s_client, slug, city or "Accra",
                                                       limit=5, page=getattr(args, "pages", 1) or 1):
                            card["source_id"] = card.get("source_id") or f"{source}:{store.dedupe_key(None, card.get('name',''), card.get('area'))}"
                            card.setdefault("phone", card.get("phone_e164"))
                            card["categories"] = [slug]
                            # decide fate BEFORE spending a profile fetch on it:
                            # enrich only brand-new cards (or dupes missing contacts)
                            dup = store.find_duplicate(conn, card) if source == "businessghana" else None
                            needs = (dup is None or
                                     any(not dup[k] for k in ("website", "email", "address", "phone_e164")))
                            if source == "businessghana" and needs:
                                try:  # real contact block lives on the profile page
                                    card.update(profile_details(s_client, card["profile_url"]))
                                except Exception as exc:
                                    store.source_log_failure(conn, source, card["profile_url"], str(exc)[:180])
                                # nationwide search -> trust only the parsed address for city
                                card["city"] = next((c for c in (config.CITIES or {})
                                                     if c.lower() in (card.get("address") or "").lower()), None)
                            if source != "businessghana":
                                card["city"] = city or "Accra"
                            if card.get("city"):
                                card["area_key"] = f"{card['city'].lower()}|{card.get('area') or ''}"
                            card["phone_e164"] = geo.normalize_phone(card.get("phone") or card.get("phone_e164"))
                            card["area"] = geo.infer_area(card.get("address") or "", card.get("city") or "")
                            card["ghana_post"] = geo.extract_ghana_post(card.get("address") or "")
                            if card.get("alt_phone"):
                                card["whatsapp"] = geo.normalize_phone(card["alt_phone"]) or None
                            card["language"] = "en"
                            if store.is_opted_out(conn, {"phone_e164": card.get("phone_e164"), "opt_out": 0,
                                                         "brand_key": store.brand_key(card.get("name", "")),
                                                         "source_id": str(card.get("source_id"))}):
                                continue
                            dup = store.find_duplicate(conn, card)
                            if dup:  # corroborating source: backfill missing contacts
                                updates = {k: card[k] for k in ("website", "email", "address", "phone_e164")
                                           if card.get(k) and not dup[k]}
                                if updates:
                                    conn.execute(f"UPDATE businesses SET {','.join(f'{k}=?' for k in updates)} WHERE id=?",
                                                 (*updates.values(), dup["id"]))
                                    _progress(t0, source, f"dupe match {str(dup['name'])[:28]}: backfilled {','.join(updates)}")
                                continue
                            sid = store.upsert_business(conn, card)
                            added += 1
                            _progress(t0, source, f"new #{added} (id {sid}): {str(card['name'])[:32]}"
                                      f" ({'phone' if card.get('phone_e164') else 'no phone'})")
                    except (RobotsBlocked, Exception) as exc:
                        store.source_log_failure(conn, source, slug, str(exc)[:180])
                        if isinstance(exc, RobotsBlocked):
                            _progress(t0, source, f"[robots] {source} blocked {slug} — skipping source")
        log(conn, "scan", f"{added} new / {total} scanned")
        print(f"scan: {added} new leads stored ({total} scanned) — {_elapsed(t0)} elapsed", flush=True)


def _scan_kenya(args, country):
    """Yellow Pages Kenya sweep: category listing -> detail page contact block."""
    t0 = time.monotonic()
    client = Client(delay=config.RATE_LIMITS["kenyayp"])
    cats = [args.category] if args.category else config.CATEGORIES[: args.limit or len(config.CATEGORIES)]
    added, total = 0, 0
    _progress(t0, "boot", f"kenya: {len(cats)} categories"
              f" (politeness {config.RATE_LIMITS['kenyayp']}s per request)")
    with store.db() as conn:
        store.set_weights(conn)
        for slug in cats:
            url = f"https://www.yellowpageskenya.com/business-category/{kenya_category(slug)}"
            _progress(t0, "kenya", f"category {slug} → fetching listing …")
            try:
                cards = cards_kenya(client.get(url).text, "https://www.yellowpageskenya.com")
            except Exception as exc:
                store.source_log_failure(conn, "kenyayp", slug, str(exc)[:180])
                _progress(t0, "kenya", f"!! {slug}: {exc}")
                continue
            _progress(t0, "kenya", f"{len(cards)} businesses in {slug}")
            for card in cards:
                total += 1
                _progress(t0, "kenya", f"detail {total}: {str(card['name'])[:30]} …")
                try:
                    card.update(kenya_profile_details(client, card["profile_url"]))
                except Exception as exc:
                    store.source_log_failure(conn, "kenyayp", card["profile_url"], str(exc)[:180])
                card["country"] = "kenya"
                card["source_of"] = "kenyayp"
                card["categories"] = [slug]
                card["phone_e164"] = geo.normalize_phone(card.get("phone") or "", "kenya")
                if card.get("alt_phone"):
                    card["whatsapp"] = geo.normalize_phone(card["alt_phone"], "kenya") or None
                cities = config.COUNTRIES["kenya"]["cities"]
                card["city"] = next((c for c in cities
                                     if c.lower() in (card.get("address") or "").lower()), None)
                card["area"] = geo.infer_area(card.get("address") or "", card.get("city") or "")
                card["language"] = "en"
                if store.is_opted_out(conn, {"phone_e164": card.get("phone_e164"), "opt_out": 0,
                                             "brand_key": store.brand_key(card.get("name", "")),
                                             "source_id": card["source_id"]}):
                    continue
                dup = store.find_duplicate(conn, card)
                if dup:
                    updates = {k: card[k] for k in ("website", "email", "address", "phone_e164")
                               if card.get(k) and not dup[k]}
                    if updates:
                        conn.execute(f"UPDATE businesses SET {','.join(f'{k}=?' for k in updates)} WHERE id=?",
                                     (*updates.values(), dup["id"]))
                        _progress(t0, "kenya", f"dupe match {str(dup['name'])[:26]}: backfilled {','.join(updates)}")
                    else:
                        _progress(t0, "kenya", f"dupe match {str(dup['name'])[:26]}: already complete")
                    continue
                sid = store.upsert_business(conn, card)
                added += 1
                _progress(t0, "kenya", f"new #{added} (id {sid}): {str(card['name'])[:30]}"
                          f" ({'phone ✓' if card.get('phone_e164') else 'no phone'})")
        log(conn, "scan", f"kenya: {added} new / {total} scanned")
        print(f"scan(kenya): {added} new leads stored ({total} scanned) — {_elapsed(t0)} elapsed", flush=True)


def _scan_nigeria(args, country):
    source = getattr(args, "source", None) or "ngex"
    if source == "blng":
        return _scan_blng(args, country)
    return _scan_ngex(args, country)


def _scan_blng(args, country):
    """BusinessList.com.ng sweep. Their robots asks a 40s crawl-delay, so
    batches are slow by nature: ~1-2 categories per run is realistic."""
    t0 = time.monotonic()
    client = Client(delay=config.RATE_LIMITS["blng"])
    cats = [args.category] if args.category else ["lawyers", "hotels"]
    if args.limit:
        cats = cats[: args.limit]
    added, total = 0, 0
    _progress(t0, "boot", f"nigeria: {len(cats)} categories — politeness is"
              f" {config.RATE_LIMITS['blng']}s per request (their robots.txt "
              f"asks crawl-delay 40); expect ~{len(cats) * 7} min")
    with store.db() as conn:
        store.set_weights(conn)
        for slug in cats:
            url = f"{sources_local.NIGERIA_BASE}/category/{nigeria_category(slug)}"
            _progress(t0, "nigeria", f"category {slug} → fetching listing …")
            try:
                cards = sources_local.cards_nigeria(client.get(url).text,
                                                    sources_local.NIGERIA_BASE)
            except Exception as exc:
                store.source_log_failure(conn, "blng", slug, str(exc)[:180])
                _progress(t0, "nigeria", f"!! {slug}: {exc}")
                continue
            fetched = cards[:8]  # 8 details x 41s ≈ 6 min per category
            _progress(t0, "nigeria", f"{len(cards)} found, fetching {len(fetched)} details (≈{len(fetched) * 41 // 60} min)")
            for card in fetched:
                total += 1
                _progress(t0, "nigeria", f"detail {total}/8: {str(card['name'])[:30]} …")
                try:
                    card.update(sources_local.nigeria_profile_details(client, card["profile_url"]))
                except Exception as exc:
                    store.source_log_failure(conn, "blng", card["profile_url"], str(exc)[:180])
                card["country"] = "nigeria"
                card["source_of"] = "blng"
                card["categories"] = [slug]
                card["phone_e164"] = geo.normalize_phone(card.get("phone") or "", "nigeria")
                if card.get("alt_phone"):
                    card["whatsapp"] = geo.normalize_phone(card["alt_phone"], "nigeria") or None
                cities = config.COUNTRIES["nigeria"]["cities"]
                card["city"] = next((c for c in cities
                                     if c.lower() in (card.get("address") or "").lower()), None)
                card["area"] = geo.infer_area(card.get("address") or "", card.get("city") or "")
                card["language"] = "en"
                if store.is_opted_out(conn, {"phone_e164": card.get("phone_e164"), "opt_out": 0,
                                             "brand_key": store.brand_key(card.get("name", "")),
                                             "source_id": card["source_id"]}):
                    continue
                dup = store.find_duplicate(conn, card)
                if dup:
                    updates = {k: card[k] for k in ("website", "email", "address", "phone_e164")
                               if card.get(k) and not dup[k]}
                    if updates:
                        conn.execute(f"UPDATE businesses SET {','.join(f'{k}=?' for k in updates)} WHERE id=?",
                                     (*updates.values(), dup["id"]))
                        _progress(t0, "nigeria", f"dupe match {str(dup['name'])[:26]}: backfilled {','.join(updates)}")
                    else:
                        _progress(t0, "nigeria", f"dupe match {str(dup['name'])[:26]}: already complete")
                    continue
                sid = store.upsert_business(conn, card)
                added += 1
                reviews = card.get("reviews_count")
                _progress(t0, "nigeria", f"new #{added} (id {sid}): {str(card['name'])[:30]}"
                          f" ({'phone ✓' if card.get('phone_e164') else 'no phone'})"
                          + (f", {reviews} reviews" if reviews else ""))
        log(conn, "scan", f"nigeria: {added} new / {total} scanned")
        print(f"scan(nigeria): {added} new leads stored ({total} scanned) — {_elapsed(t0)} elapsed", flush=True)


def _scan_ngex(args, country="nigeria"):
    """Nigeria Galleria keyword search sweep: fast, structured, phone-rich."""
    t0 = time.monotonic()
    client = Client(delay=config.RATE_LIMITS["ngex"])
    cats = [args.category] if args.category else config.CATEGORIES[: args.limit or len(config.CATEGORIES)]
    cities = list(config.COUNTRIES["nigeria"]["cities"])  # priority order
    added, total = 0, 0
    per_city = int(getattr(args, "pages", 3) or 3)
    _progress(t0, "boot", f"nigeria/ngex: {len(cats)} categories x {len(cities)} cities"
              f" — politeness {config.RATE_LIMITS['ngex']}s (fast source)")
    with store.db() as conn:
        store.set_weights(conn)
        # reuse a single polite client for listing + detail fetches
        for slug in cats:
            term = ngex_category(slug)
            for city in cities:
                _progress(t0, "ngex", f"'{term}' in {city} → searching …")
                url = (f"{sources_local.NGEX_BASE}/bd/search"
                       f"?q={quote_plus(term)}&place={quote_plus(city)}")
                try:
                    cards = cards_ngex(client.get(url).text, sources_local.NGEX_BASE)
                except Exception as exc:
                    store.source_log_failure(conn, "ngex", f"{slug}/{city}", str(exc)[:180])
                    _progress(t0, "ngex", f"!! {slug}/{city}: {exc}")
                    continue
                _progress(t0, "ngex", f"{len(cards)} results in {city}")
                for card in cards[:per_city]:
                    total += 1
                    _progress(t0, "ngex", f"detail {total}: {str(card['name'])[:30]} …")
                    try:
                        card.update(ngex_profile_details(client, card["profile_url"]))
                    except Exception as exc:
                        store.source_log_failure(conn, "ngex", card["profile_url"], str(exc)[:180])
                    card["country"] = "nigeria"
                    card["source_of"] = "ngex"
                    card["categories"] = [slug]
                    card["phone_e164"] = geo.normalize_phone(card.get("phone") or "", "nigeria")
                    if card.get("alt_phone"):
                        card["whatsapp"] = geo.normalize_phone(card["alt_phone"], "nigeria") or None
                    card["city"] = card.get("address") and next(
                        (c for c in cities if c.lower() in card["address"].lower()), city) or city
                    card["area"] = geo.infer_area(card.get("address") or "", card.get("city") or "")
                    card["language"] = "en"
                    if store.is_opted_out(conn, {"phone_e164": card.get("phone_e164"), "opt_out": 0,
                                                 "brand_key": store.brand_key(card.get("name", "")),
                                                 "source_id": str(card.get("source_id"))}):
                        continue
                    dup = store.find_duplicate(conn, card)
                    if dup:
                        updates = {k: card[k] for k in ("website", "email", "address", "phone_e164")
                                   if card.get(k) and not dup[k]}
                        if updates:
                            conn.execute(f"UPDATE businesses SET {','.join(f'{k}=?' for k in updates)} WHERE id=?",
                                         (*updates.values(), dup["id"]))
                            _progress(t0, "ngex", f"dupe match {str(dup['name'])[:26]}: backfilled {','.join(updates)}")
                        else:
                            _progress(t0, "ngex", f"dupe match {str(dup['name'])[:26]}: already complete")
                        continue
                    sid = store.upsert_business(conn, card)
                    added += 1
                    _progress(t0, "ngex", f"new #{added} (id {sid}): {str(card['name'])[:30]}"
                              f" ({'phone ✓' if card.get('phone_e164') else 'no phone'})"
                              + (f", {card['reviews_count']} reviews" if card.get("reviews_count") else ""))
        log(conn, "scan", f"nigeria/ngex: {added} new / {total} scanned")
        print(f"scan(ngex): {added} new leads stored ({total} scanned) — {_elapsed(t0)} elapsed", flush=True)


def _fetch_profile(conn, client, card):
    existing = store.get_business(conn, card["source_id"])
    if existing and existing["profile_fetched_at"]:
        return
    try:
        prof = scrape_profile(client, existing["profile_url"])
    except Exception as exc:
        store.source_log_failure(conn, "ghanayello", existing["profile_url"], str(exc))
        return
    prof["source_id"] = card["source_id"]
    prof["profile_fetched_at"] = store.now()
    prof["discovered_at"] = existing["discovered_at"]
    prof["phone_e164"] = geo.normalize_phone(existing["phone"] if not prof.get("website") and existing["phone"] else prof.get("phone"))
    prof["ghana_post"] = geo.extract_ghana_post((prof.get("address") or "") ) or existing["ghana_post"]
    prof["language"] = geo.detect_language((prof.get("description") or "") + " " + (existing["description"] or ""))
    store.upsert_business(conn, prof)


def _sanitize_contacts(conn) -> int:
    """Null out garbage contact values (button text like 'Send to WhatsApp')
    and promote any extractable number to normalized form. Never discard a
    plain phone that still carries digits — non-Ghana numbers don't match the
    Ghana pattern set, and their canonical value lives in phone_e164."""
    import re
    patterns = re.compile(r"\+?233[\d ]{9}|\b0[2-5]\d[\d ]{7}\b")
    fixed = 0
    for row in conn.execute(
            "SELECT id, phone, whatsapp, phone_e164 FROM businesses WHERE phone IS NOT NULL OR whatsapp IS NOT NULL"):
        wa, ph = row["whatsapp"], row["phone"]
        new_wa = geo.normalize_phone(wa) if wa else None
        if wa and not new_wa:
            m = patterns.search(wa)
            new_wa = geo.normalize_phone(m.group(0)) if m else None
        if wa and not new_wa and not any(ch.isdigit() for ch in wa):
            new_wa = None  # pure button text
        elif wa and not new_wa:
            new_wa = wa  # digits we cannot normalize — keep, e164 stays canonical
        new_ph = geo.normalize_phone(ph) if ph else None
        if ph and not new_ph:
            m = patterns.search(ph)
            new_ph = geo.normalize_phone(m.group(0)) if m else None
        if ph and not new_ph:
            new_ph = ph if any(ch.isdigit() for ch in ph) else None
        phone_e164 = (row["phone_e164"] or geo.normalize_phone(ph or "")
                      or geo.normalize_phone(wa or "") or None)
        if new_wa != wa or new_ph != ph or phone_e164 != row["phone_e164"]:
            conn.execute("UPDATE businesses SET whatsapp=?, phone=?, phone_e164=? WHERE id=?",
                         (new_wa, new_ph, phone_e164, row["id"]))
            fixed += 1
    return fixed


def cmd_audit(args):
    client = Client(delay=0.8)
    with store.db() as conn:
        country = (getattr(args, "country", None) or "").lower().strip()
        where = ["website_status IN ('unknown','none','noparse') AND website_checked_at IS NULL"]
        params = []
        if country:
            where.append("country LIKE ?")
            params.append(country + "%")
        rows = conn.execute(
            f"SELECT * FROM businesses WHERE {' AND '.join(where)}"
            + (f" LIMIT {args.limit}" if args.limit else ""), (*params,)).fetchall()
        done = 0
        for row in rows:
            if store.is_opted_out(conn, row):
                continue
            try:
                result = audit_business_v2(client, dict(row))
            except Exception as exc:
                store.source_log_failure(conn, "audit", (row["website"] or row["profile_url"] or ""),
                                         f"{type(exc).__name__}: {exc}"[:180])
                continue
            if not result:
                continue
            cols = ", ".join(f"{k}=?" for k in result)
            conn.execute(f"UPDATE businesses SET {cols}, website_checked_at=? WHERE id=?",
                         (*result.values(), store.now(), row["id"]))
            done += 1
            if done % 20 == 0:
                print(f"  audited {done}/{len(rows)}")
        fixed = _sanitize_contacts(conn)
        log(conn, "audit", f"{done} audited, {fixed} contact fields cleaned")
        print(f"audited {done} ({fixed} contact fields cleaned)")


def cmd_score(args):
    with store.db() as conn:
        fixed = store.recalculate_dedupe_keys(conn)
        if fixed:
            print(f"  dedupe backfill: {fixed} rows rekeyed")
        country = (getattr(args, "country", None) or "").lower().strip()
        scope, scope_params = (" AND country LIKE ?", (country + "%",)) if country else ("", ())
        if getattr(args, "refresh", False):
            # reset everything: disqualified rows may recover when new contact
            # data has been backfilled; opt-out and dq checks re-derive here
            conn.execute("UPDATE businesses SET accept_score=NULL, tier=NULL WHERE 1=1" + scope,
                         scope_params)
        rows = conn.execute(
            "SELECT * FROM businesses WHERE accept_score IS NULL AND (tier IS NULL OR tier NOT IN ('DISQUALIFIED'))"
            + scope
            + (f" LIMIT {args.limit}" if args.limit else ""), scope_params).fetchall()
        done = 0
        tiers = {"A": 0, "B": 0, "C": 0, "DISQUALIFIED": 0}
        for row in rows:
            if store.is_opted_out(conn, row):
                conn.execute("UPDATE businesses SET tier='DISQUALIFIED', reason='opt_out' WHERE id=?", (row["id"],))
                continue
            out = score_business(conn, dict(row))
            if not out:
                continue
            cols = ", ".join(f"{k}=?" for k in out)
            conn.execute(f"UPDATE businesses SET {cols}, scored_at=? WHERE id=?",
                         (*out.values(), store.now(), row["id"]))
            tiers[out.get("tier", "DISQUALIFIED")] += 1
            done += 1
        log(conn, "score", f"{done} scored {tiers}")
        print(f"scored {done}: {tiers}")


def cmd_media(args):
    client = Client(delay=1.0)
    with store.db() as conn:
        rows = conn.execute(
            "SELECT * FROM businesses WHERE tier IN ('A','B') AND media_at IS NULL"
            + (f" LIMIT {args.limit}" if args.limit else "")).fetchall()
        done = 0
        for row in rows:
            images = jloads(row["images"], [])
            videos = jloads(row["videos"], [])
            if not images and not videos:
                continue
            media_mod.collect_from_site(None, images, videos, conn, row["id"], client.session)
            media_mod.collect_social(conn, row, client.session)
            media_mod.update_media_ready(conn, row)
            done += 1
        log(conn, "media", f"{done} enriched")
        print(f"media enriched {done} tier-A/B leads")


def cmd_brief(args):
    with store.db() as conn:
        migrate_legacy(conn)
        if args.lead:
            rows = conn.execute("SELECT * FROM businesses WHERE id=? OR source_id=?",
                                (args.lead, args.lead)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM businesses WHERE tier IN ('A','B') AND (brief_at IS NULL OR brief_at < ?)"
                + (f" LIMIT {args.limit}" if args.limit else ""), (store.now(),)).fetchall()
        out_paths = []
        for row in rows:
            if not row["scored_at"]:
                continue
            jp, mp = export_brief(conn, row)
            conn.execute("UPDATE businesses SET brief_at=? WHERE id=?", (store.now(), row["id"]))
            out_paths.append(jp)
        print(f"{len(out_paths)} briefs -> {BRIEF_DIR}/")


def cmd_brief_remove(args):
    """Delete one lead's brief folder; clears brief_at so `brief` can remake it."""
    import shutil
    with store.db() as conn:
        q = (getattr(args, "lead", None) or "").strip()
        if not q:
            print("usage: leads brief-remove <id | source_id | name-part>")
            return
        row = conn.execute(
            "SELECT id, name FROM businesses WHERE CAST(id AS TEXT)=? OR source_id=? "
            "OR name LIKE ('%'||?||'%') OR brand_key LIKE ('%'||?||'%') "
            "ORDER BY accept_score DESC LIMIT 1", (q, q, q, q)).fetchone()
        if not row:
            print(f"no lead matching '{q}'")
            return
        bdir = BRIEF_DIR / str(row["id"])
        if bdir.exists():
            shutil.rmtree(bdir)
            conn.execute("UPDATE businesses SET brief_at=NULL WHERE id=?", (row["id"],))
            log(conn, "brief", f"removed brief folder for lead {row['id']}")
            print(f"removed {bdir} and cleared brief_at for '{row['name']}' "
                  f"(re-run: leads brief \"{row['name'][:40]}\")")
        else:
            print(f"no brief folder for '{row['name']}' at {bdir} — brief_at untouched")


def cmd_socials(args):
    """Self-published social-profile hunt (stage 2.5): search-engine pass,
    name-matched, stored into `socials` per lead. Slim politeness default."""
    from .socials import find_socials
    client = Client(delay=config.RATE_LIMITS.get("search", 3.5))
    with store.db() as conn:
        rows = conn.execute(
            "SELECT id, name, city, accept_score, socials, socials_checked_at FROM businesses "
            "WHERE tier='C' AND (socials IS NULL AND socials_checked_at IS NULL) "
            "AND website_status NOT IN ('OK') ORDER BY accept_score DESC"
        ).fetchall()
        todo = rows[: min(args.limit, 15)]  # 15 queries/run: keep engines calm
        found = stored = 0

        def finish(msg):
            conn.commit()
            log(conn, "socials", msg)
            print(f"socials: {msg}")

        try:
            for row in todo:
                cands = find_socials(client, row["name"], row["city"])
                verified = [c for c in cands if c["match"] >= 0.5]
                if verified:
                    found += 1
                    socials = {}
                    for c in verified:  # strongest first already verified above
                        k = c["platform"]
                        if k and k in ("instagram", "facebook", "linktree", "whatsapp", "tiktok"):
                            socials.setdefault(k, c["url"])
                    others = [c["url"] for c in verified
                              if c["platform"] not in socials][:3]
                    if others:
                        socials.setdefault("other", others)
                    conn.execute(
                        "UPDATE businesses SET socials=?, socials_checked_at=? WHERE id=?",
                        (store.jdumps(socials), store.now(), row["id"]))
                    stored += 1
                    print(f"  [#{row['id']} {row['accept_score']:>3}] {row['name'][:38]:38}"
                          f" -> {', '.join(socials)}")
                else:
                    print(f"  [#---] {row['name'][:38]:38} -> no name-matched pages")
            finish(f"{found}/{len(todo)} with socials, {stored} stored")
        except HttpError as exc:
            # engines withheld results mid-run: nothing half-broken gets stored,
            # leads without socials stay retry-eligible for the next calm batch
            finish(str(exc)[:180])


def cmd_export(args):
    with store.db() as conn:
        where, params = ["1=1"], []
        if args.city:
            where.append("city = ?")
            params.append(args.city.title())
        if args.category:
            where.append("categories LIKE ?")
            params.append(f"%{args.category}%")
        if args.tier:
            where.append("tier = ?")
            params.append(args.tier)
        if args.min_assets:
            where.append("media_ready >= ?")
            params.append(args.min_assets)
        rows = conn.execute(
            f"SELECT * FROM businesses WHERE {' AND '.join(where)} "
            "ORDER BY accept_score DESC NULLS LAST, weakness_score DESC LIMIT 5000",
            params).fetchall()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "leads_pipeline.csv"
    import csv
    cols = ["id", "source_id", "name", "city", "area", "category", "language", "ghana_post",
            "phone", "whatsapp", "email", "website", "website_status", "weakness_score",
            "accept_score", "tier", "score_breakdown", "reason", "objection",
            "media_ready", "evidence", "source_of"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        header = [c for c in cols if c]
        w.writerow(header)
        for r in rows:
            w.writerow([str(r[c]) if c in r.keys() and r[c] is not None else "" for c in header])
    print(f"{len(rows)} rows -> {path}")


def cmd_status(args):
    with store.db() as conn:
        n = conn.execute("SELECT COUNT(*) FROM businesses").fetchone()[0]
        print(f"businesses: {n}")
        for r in conn.execute("SELECT CASE WHEN tier IS NULL THEN 'unscored' ELSE tier END t, COUNT(*) c "
                              "FROM businesses GROUP BY t ORDER BY c DESC"):
            print(f"  {r['t']:14} {r['c']}")
        for r in conn.execute("SELECT website_status s, COUNT(*) c FROM businesses GROUP BY s ORDER BY c DESC"):
            print(f"  audit:{(r['s'] or 'unknown'):12} {r['c']}")
        for r in conn.execute("SELECT source, COUNT(*) c FROM businesses GROUP BY source ORDER BY c DESC"):
            print(f"  src:{r['source']:18} {r['c']}")
        fails = conn.execute("SELECT COUNT(*) FROM scan_failures").fetchone()[0]
        print(f"scan failures logged: {fails}")


def cmd_leads(args):
    with store.db() as conn:
        country = (getattr(args, "country", None) or "").lower().strip()
        if country and not country.startswith(("gh", "ke", "ni")):
            print(f"??unknown country '{args.country}' — expected ghana | kenya | nigeria")
            return
        show_all = bool(getattr(args, "all", False))
        reset = bool(getattr(args, "reset", False))
        scope = " AND country LIKE ?" if country else ""
        scope_params = (country + "%",) if country else ()

        if reset:
            # rotate back to the start of the list: forget every lead the view
            # has already shown (country-scoped when --country is passed)
            if country:
                n = conn.execute(
                    "DELETE FROM served_leads WHERE lead_id IN "
                    "(SELECT id FROM businesses WHERE country LIKE ?)",
                    scope_params).rowcount
            else:
                n = conn.execute("DELETE FROM served_leads").rowcount
            conn.commit()
            print(f"served history cleared ({n} leads){' for ' + country if country else ''} — "
                  f"next `leads` starts a fresh pass")
            return

        # opt_out=0 is not optional: an opted-out lead must never surface in
        # the pitch view, even if its tier still reads A/B (see score, which
        # re-derives DISQUALIFIED on opt-out, and sources that never rescore).
        # served exclusion keeps the top of the list rotating: every listed
        # row is recorded, so the next run serves the next batch (--all
        # bypasses rotation for a view-only pass).
        excl = "" if show_all else " AND id NOT IN (SELECT lead_id FROM served_leads)"
        where = ["tier IN ('A','B')", "opt_out=0"]
        params = []
        if country:
            where.append("country LIKE ?")
            params.append(country + "%")
        rows = conn.execute(
            "SELECT id, name, city, country, tier, accept_score, weakness_score, website_status, phone, whatsapp "
            f"FROM businesses WHERE {' AND '.join(where)}{excl} ORDER BY accept_score DESC LIMIT ?",
            (*params, args.limit)).fetchall()
        if not rows:
            hint = f" for {args.country}" if country else ""
            print(f"no tier A/B leads yet{hint} — outreach outcomes promote tier C leads (see: outcome)")
            where_f = ["opt_out=0"] + (["country LIKE ?"] if country else [])
            rows = conn.execute(
                "SELECT id, name, city, country, tier, accept_score, weakness_score, website_status, phone, whatsapp "
                f"FROM businesses WHERE {' AND '.join(where_f)}{excl} ORDER BY accept_score DESC LIMIT ?",
                (*((country + "%",) if country else ()), args.limit)).fetchall()
        for r in rows:
            place = r["city"] if country else f"{r['city'] or ''}/{(r['country'] or '??')[:2]}".strip("/")
            print(f"[{r['tier']}-{r['accept_score']:>3}] #{r['id']} {r['name']} ({place}, w={r['weakness_score']}) "
                  f"wa={r['whatsapp'] or r['phone'] or '—'}")
        if show_all:
            return
        if not rows:
            served = conn.execute(
                f"SELECT COUNT(*) FROM served_leads WHERE lead_id IN "
                f"(SELECT id FROM businesses WHERE opt_out=0{scope})",
                scope_params).fetchone()[0]
            print(f"all {served} leads served{' for ' + country if country else ''} — "
                  f"`leads leads --reset{' --country ' + country if country else ''}` starts a new pass")
            return
        ts = store.now()
        for r in rows:
            conn.execute(
                "INSERT INTO served_leads (lead_id, ts, times) VALUES (?,?,1) "
                "ON CONFLICT(lead_id) DO UPDATE SET ts=excluded.ts, times=times+1",
                (r["id"], ts))
        conn.commit()
        fresh = conn.execute(
            f"SELECT COUNT(*) FROM businesses WHERE opt_out=0{scope} "
            f"AND id NOT IN (SELECT lead_id FROM served_leads)",
            scope_params).fetchone()[0]
        served = conn.execute("SELECT COUNT(*) FROM served_leads").fetchone()[0]
        print(f"-- {len(rows)} served · {fresh} fresh left"
              f"{' in ' + country if country else ''} · {served} total shown"
              f" · `leads leads --reset` starts over")


def cmd_optout(args):
    with store.db() as conn:
        contact = args.contact.strip()
        rows = []
        phone = None
        if contact.startswith("#") or contact.isdigit():
            rows = conn.execute("SELECT * FROM businesses WHERE id=?", (contact.lstrip("#"),)).fetchall()
        elif ":" in contact:
            rows = conn.execute("SELECT * FROM businesses WHERE source_id=?", (contact.split(":", 1)[1],)).fetchall()
        elif contact.startswith(("0", "+23")) or contact.startswith("+"):
            phone = geo.normalize_phone(contact) if geo.normalize_phone(contact) else contact
            rows = conn.execute("SELECT * FROM businesses WHERE phone_e164=?", (phone,)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM businesses WHERE name LIKE ('%'||?||'%') OR brand_key LIKE ('%'||?||'%') "
                "ORDER BY accept_score DESC", (contact, contact)).fetchall()
        if not rows and not phone:
            print(f"??no lead matches '{contact}' — nothing opted out (use #id, source:id, phone or name part)")
            return
        # keep the permanent table keyed so future scans of the same brand /
        # phone are excluded too (is_opted_out matches phone/brand/source)
        for row in rows:
            if store.is_opted_out(conn, row):
                print(f"  #{row['id']} {row['name']} — already opted out")
                continue
            conn.execute("UPDATE businesses SET opt_out=1 WHERE id=?", (row["id"],))
            bk = row["brand_key"] or store.brand_key(row["name"])
            if bk and not row["brand_key"]:
                # persist the derived key so is_opted_out matches later too
                conn.execute("UPDATE businesses SET brand_key=? WHERE id=?",
                             (bk, row["id"]))
            for col, val in (("phone_e164", row["phone_e164"]),
                             ("brand_key", bk),
                             ("source_id", str(row["source_id"]))):
                if val and not conn.execute(
                    f"SELECT 1 FROM opt_out WHERE {col}=? LIMIT 1", (val,)).fetchone():
                    conn.execute(
                        "INSERT INTO opt_out (ts, phone_e164, source_id, brand_key, reason) VALUES (?,?,?,?,?)",
                        (store.now(), val if col == "phone_e164" else None,
                         val if col == "source_id" else None, val if col == "brand_key" else None,
                         args.reason or "user requested"))
            print(f"opted out #{row['id']} {row['name']} ({row['tier'] or '?'})")
        if phone and not rows:
            conn.execute(
                "INSERT INTO opt_out (ts, phone_e164, source_id, brand_key, reason) VALUES (?,?,?,?,?)",
                (store.now(), phone, None, None, args.reason or "user requested"))
            print(f"opt-out recorded for phone {phone} (no current row matched — honored on ingest)")
        log(conn, "opt_out", contact)


def cmd_outcome(args):
    with store.db() as conn:
        rows = conn.execute("SELECT id FROM businesses WHERE source_id=?", (args.lead_id,)).fetchall()
        if not rows:
            print("no lead with that source_id")
            return
        store.record_outcome(conn, rows[0]["id"], args.action, args.notes or "", args.campaign)
        result = store.recalibrate(conn)
        print(f"logged for id {rows[0]['id']} (source_id={args.lead_id}); recalibration:", json.dumps(result))


def cmd_categories(args):
    client = Client(delay=1.0)
    cats = list_categories(client)
    (OUT_DIR.parent / "exports").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "categories.json").write_text(json.dumps(cats, indent=2, ensure_ascii=False))
    print(f"{len(cats)} categories -> exports/categories.json")


def cmd_weights(args):
    with store.db() as conn:
        store.set_weights(conn)
        for r in conn.execute("SELECT factor, value FROM weights ORDER BY value DESC"):
            print(f"  {r['factor']:10} {r['value']:.3f}")


def main():
    p = __import__("argparse").ArgumentParser(description="Ghana lead pipeline v2")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan")
    s.add_argument("--category"); s.add_argument("--city")
    s.add_argument("--country", default=None, help="ghana (default) | kenya | nigeria")
    s.add_argument("--pages", type=int, default=5); s.add_argument("--limit", type=int)
    s.add_argument("--profiles", action="store_true")
    s.add_argument("--no-second-source", action="store_true",
                   help="skip the BusinessGhana corroborating sweep")
    s.add_argument("--classifieds", action="store_true",
                   help="also pull Tonaton/Jiji consumer classifieds (noisy, opt-in)")
    s.set_defaults(func=cmd_scan)

    a = sub.add_parser("audit"); a.add_argument("--limit", type=int)
    a.add_argument("--country", default=None,
                   help="ghana | kenya | nigeria — audit only that country's pending queue")
    a.set_defaults(func=cmd_audit)
    sc = sub.add_parser("score"); sc.add_argument("--limit", type=int)
    sc.add_argument("--country", default=None,
                    help="ghana | kenya | nigeria — score only that country (with --refresh)")
    sc.add_argument("--refresh", action="store_true",
                    help="rescore every non-disqualified business (picks up new weights / pitch fields)")
    sc.set_defaults(func=cmd_score)
    m = sub.add_parser("media"); m.add_argument("--limit", type=int); m.set_defaults(func=cmd_media)
    b = sub.add_parser("brief"); b.add_argument("--lead"); b.add_argument("--limit", type=int); b.set_defaults(func=cmd_brief)
    br = sub.add_parser("brief-remove"); br.add_argument("lead", nargs="?"); br.set_defaults(func=cmd_brief_remove)
    e = sub.add_parser("export")
    e.add_argument("--city"); e.add_argument("--category"); e.add_argument("--tier")
    e.add_argument("--min-assets", type=int, default=0); e.set_defaults(func=cmd_export)
    so = sub.add_parser("socials")
    so.add_argument("--limit", type=int, default=20)
    so.set_defaults(func=cmd_socials)
    sub.add_parser("status").set_defaults(func=cmd_status)
    l = sub.add_parser("leads"); l.add_argument("--limit", type=int, default=30)
    l.add_argument("--country", default=None,
                   help="ghana (default prefix gh) | kenya | nigeria — top-lead view per country")
    l.add_argument("--all", action="store_true",
                   help="view-only pass: include leads already served")
    l.add_argument("--reset", action="store_true",
                   help="clear served history (country-scoped with --country) — start a new pass")
    l.set_defaults(func=cmd_leads)
    o = sub.add_parser("optout"); o.add_argument("contact"); o.add_argument("--reason")
    o.set_defaults(func=cmd_optout)
    oc = sub.add_parser("outcome"); oc.add_argument("lead_id"); oc.add_argument("action",
        choices=["replied", "meeting", "paid", "declined", "message_sent"]); oc.add_argument("--notes")
    oc.add_argument("--campaign", default=""); oc.set_defaults(func=cmd_outcome)
    sub.add_parser("categories").set_defaults(func=cmd_categories)
    sub.add_parser("weights").set_defaults(func=cmd_weights)

    args = p.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\ninterrupted — progress saved; rerun the same command to resume")
        sys.exit(130)


if __name__ == "__main__":
    main()
