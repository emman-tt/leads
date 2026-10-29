from __future__ import annotations

"""SQLite store: schema + connection helpers. Single file DB = source of truth."""
import json
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS businesses (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    source            TEXT NOT NULL DEFAULT 'ghanayello',
    source_id         TEXT,
    name              TEXT NOT NULL,
    slug              TEXT,
    profile_url       TEXT,
    brand_key         TEXT,              -- normalized name for de-dup across branches
    city              TEXT,
    region            TEXT,
    address           TEXT,
    phone             TEXT,
    whatsapp          TEXT,
    website           TEXT,
    has_website       INTEGER,           -- flag taken from the directory card
    website_status    TEXT DEFAULT 'unknown',  -- none | ok | weak | dead | error
    weakness_score    INTEGER,           -- 0 (strong) .. 100 (weak) / 100 for missing site
    weakness_flags    TEXT,              -- json list of strings
    email             TEXT,
    emails            TEXT,              -- json list found on their website
    established_year  INTEGER,
    employees         TEXT,
    description       TEXT,
    categories        TEXT,              -- json list of category slugs
    rating            REAL,
    reviews_count     INTEGER,
    photos_count      INTEGER,
    latitude          REAL,
    longitude         REAL,
    logo_url          TEXT,
    images            TEXT,              -- json list of image urls
    videos            TEXT,              -- json list of video urls
    socials           TEXT,              -- json {facebook,instagram,twitter,linkedin,tiktok,youtube,...}
    socials_checked_at TEXT,             -- last time the socials hunt ran for this lead
    country           TEXT DEFAULT 'ghana',  -- ghana | kenya | nigeria
    discovered_at     TEXT,
    profile_fetched_at TEXT,
    website_checked_at TEXT,
    UNIQUE (source, source_id)
);
CREATE INDEX IF NOT EXISTS idx_status   ON businesses (website_status);
CREATE INDEX IF NOT EXISTS idx_score    ON businesses (weakness_score);
CREATE INDEX IF NOT EXISTS idx_city     ON businesses (city);
CREATE INDEX IF NOT EXISTS idx_brand    ON businesses (brand_key);
CREATE TABLE IF NOT EXISTS run_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      TEXT,
    action  TEXT,
    details TEXT
);
CREATE TABLE IF NOT EXISTS outreach_log (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        TEXT,
    lead_id   INTEGER,
    action    TEXT,          -- message_sent | replied | meeting | paid | declined | opt_out
    notes     TEXT,
    campaign  TEXT
);
CREATE TABLE IF NOT EXISTS opt_out (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          TEXT,
    phone_e164  TEXT,
    source_id   TEXT,
    brand_key   TEXT,
    reason      TEXT
);
CREATE TABLE IF NOT EXISTS served_leads (
    lead_id  INTEGER PRIMARY KEY,
    ts       TEXT,
    times    INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS assets (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id      INTEGER,
    url          TEXT,
    poster_url   TEXT,
    platform     TEXT,
    type         TEXT,       -- image | video
    res_w        INTEGER,
    res_h        INTEGER,
    bytes        INTEGER,
    quality      INTEGER,    -- 0..10
    tags         TEXT,       -- json list: hero-worthy|product|team|interior|testimonial
    preview_only INTEGER DEFAULT 1,
    created_at   TEXT
);
CREATE TABLE IF NOT EXISTS scan_failures (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    ts     TEXT,
    source TEXT,
    url    TEXT,
    error  TEXT
);
CREATE TABLE IF NOT EXISTS weights (
    factor TEXT PRIMARY KEY,
    value  REAL
);
"""

EXTRA_COLUMNS = {
    "area": "TEXT", "ghana_post": "TEXT", "language": "TEXT",
    "phone_e164": "TEXT", "source_of": "TEXT", "area_key": "TEXT",
    "dedupe_key": "TEXT", "dedupe_key_np": "TEXT", "signals": "TEXT", "evidence": "TEXT",
    "accept_score": "INTEGER", "tier": "TEXT", "score_breakdown": "TEXT",
    "reason": "TEXT", "objection": "TEXT", "media_ready": "INTEGER",
    "scored_at": "TEXT", "media_at": "TEXT", "brief_at": "TEXT",
    "opt_out": "INTEGER DEFAULT 0",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA)
    _migrate(conn)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _migrate(conn: sqlite3.Connection) -> None:
    """Idempotent column/table migration for schema evolution."""
    cols = {r[1] for r in conn.execute("PRAGMA table_info(businesses)")}
    for name, typedef in EXTRA_COLUMNS.items():
        if name not in cols:
            try:
                conn.execute(f"ALTER TABLE businesses ADD COLUMN {name} {typedef}")
            except sqlite3.OperationalError as exc:
                print("migrate skipped", name, exc)
    conn.commit()


def source_log_failure(conn, source: str, url: str, error: str) -> None:
    conn.execute("INSERT INTO scan_failures (ts, source, url, error) VALUES (?,?,?,?)",
                 (now(), source, url, error))


def set_weights(conn):
    from . import config
    for factor, value in config.WEIGHTS.items():
        conn.execute("INSERT OR IGNORE INTO weights (factor, value) VALUES (?,?)",
                     (factor, value))


def get_weights(conn) -> dict:
    rows = conn.execute("SELECT factor, value FROM weights").fetchall()
    return {r["factor"]: r["value"] for r in rows} or dict()


def dedupe_key(phone_e164: str | None, name: str, area: str | None) -> str:
    import hashlib
    normalized_name = (name or "").lower().strip().replace(".", " ")
    parts = [phone_e164 or "-", " ".join(normalized_name.split()), (area or "").lower().strip()]
    return hashlib.md5("|".join(parts).encode()).hexdigest()[:16]


def recalculate_dedupe_keys(conn) -> int:
    """Backfill dedupe keys for rows inserted before dedupe existed."""
    fixed = 0
    for row in conn.execute(
            "SELECT id, phone_e164, name, area, dedupe_key, dedupe_key_np FROM businesses").fetchall():
        want = dedupe_key(row["phone_e164"], row["name"], row["area"])
        want_np = dedupe_key(None, row["name"], row["area"])
        if row["dedupe_key"] != want or row["dedupe_key_np"] != want_np:
            conn.execute("UPDATE businesses SET dedupe_key=?, dedupe_key_np=? WHERE id=?",
                         (want, want_np, row["id"]))
            fixed += 1
    return fixed


def is_opted_out(conn, row) -> bool:
    if row["opt_out"]:
        return True
    q = conn.execute(
        "SELECT 1 FROM opt_out WHERE phone_e164=? OR brand_key=? OR source_id=? LIMIT 1",
        (row["phone_e164"] or "", row["brand_key"] or "", str(row["source_id"] or "")),
    ).fetchone()
    return bool(q)


def find_duplicate(conn, row) -> sqlite3.Row | None:
    """Empirical dedupe: same normalized phone + name-ish brand + area.
    A phoneless caller still matches on name+area (dedupe_key_np)."""
    phone_key = dedupe_key(row.get("phone_e164"), row.get("name"), row.get("area"))
    key = phone_key if row.get("phone_e164") else dedupe_key(None, row.get("name"), row.get("area"))
    return conn.execute(
        "SELECT * FROM businesses WHERE dedupe_key=? OR dedupe_key_np=? LIMIT 1",
        (key, key)).fetchone()


def record_outcome(conn, lead_id: int, action: str, notes: str = "", campaign: str = "") -> None:
    conn.execute(
        "INSERT INTO outreach_log (ts, lead_id, action, notes, campaign) VALUES (?,?,?,?,?)",
        (now(), lead_id, action, notes, campaign))


def recalibrate(conn) -> dict:
    """Nudge weights toward factors present on CONVERTED leads, away on declines.
    Simple, auditable learning: only campaigns with >=10 outcomes apply a shift."""
    weight_rows = dict(get_weights(conn))
    outcomes = conn.execute(
        """SELECT o.action, b.score_breakdown FROM outreach_log o
           JOIN businesses b ON b.id = o.lead_id
           WHERE b.score_breakdown IS NOT NULL""").fetchall()
    from .db import jloads
    if len(outcomes) < 10:
        return {"changed": False, "reason": f"only {len(outcomes)} logged outcomes; need >=10"}
    shifts = {}
    for r in outcomes:
        factors = jloads(r["score_breakdown"], {})
        sign = 1.0 if r["action"] in ("paid", "meeting", "replied") else (-1.0 if r["action"] == "declined" else 0.0)
        if not sign:
            continue
        for factor in weight_rows:
            raw = factors.get(factor)
            if not isinstance(raw, dict) or "score" not in raw:
                continue
            f = raw["score"] / 10.0
            shifts[factor] = shifts.get(factor, 0.0) + sign * 0.005 * (f - 0.5)
    for factor, shift in shifts.items():
        new_v = max(0.05, min(0.45, weight_rows[factor] + shift))
        if abs(new_v - weight_rows[factor]) > 1e-9:
            conn.execute("UPDATE weights SET value=? WHERE factor=?", (new_v, factor))
        weight_rows[factor] = new_v
    return {"changed": True, "weights": weight_rows}


def log(conn: sqlite3.Connection, action: str, details: str = "") -> None:
    conn.execute(
        "INSERT INTO run_log (ts, action, details) VALUES (?,?,?)",
        (now(), action, details),
    )


def jloads(raw, default=None):
    if isinstance(raw, (list, dict)):   # already decoded
        return raw
    if not raw:
        return default if default is not None else []
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return default if default is not None else []


def jdumps(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def evidence_of(val) -> dict:
    """Evidence is stored as {"flags": [...], "metrics": {...}}; older audit
    runs stored a bare flag list — normalize to the dict shape."""
    ev = jloads(val, {})
    if isinstance(ev, list):
        return {"flags": ev, "metrics": {}}
    return ev if isinstance(ev, dict) else {}


def brand_key(name: str) -> str:
    """Normalize a business name so multi-branch brands collapse together."""
    cleaned = (name or "").lower()
    cleaned = re.sub(r"\([^)]*\)", " ", cleaned)      # strip "(Osu)" style branch notes
    cleaned = "".join(ch for ch in cleaned if ch.isalnum() or ch.isspace())
    words = [w for w in cleaned.split() if w not in {"limited", "ltd", "gh", "ghana", "co",
                                                     "osu", "tema", "spintex", "madina",
                                                     "east", "legon", "adenta", "dansoman"}]
    return " ".join(words).strip()


def upsert_business(conn: sqlite3.Connection, row: dict) -> int:
    """Insert or update a business keyed on (source, source_id). Returns the row id."""
    table_cols = {r[1] for r in conn.execute("PRAGMA table_info(businesses)")}
    row = {k: v for k, v in row.items() if k in table_cols and k != "id"}
    row.setdefault("source", "ghanayello")
    if not row.get("dedupe_key"):  # dedupe keys computed unless caller supplies one
        row["dedupe_key"] = dedupe_key(row.get("phone_e164"), row.get("name"), row.get("area"))
        row["dedupe_key_np"] = dedupe_key(None, row.get("name"), row.get("area"))
    row["discovered_at"] = row.get("discovered_at") or now()
    cols = list(row.keys())
    values = []
    for c in cols:
        v = row[c]
        if isinstance(v, (list, dict)):
            v = jdumps(v)
        values.append(v)
    placeholders = ",".join("?" for _ in cols)
    updates = ",".join(f"{c}=excluded.{c}" for c in cols if c not in ("source", "source_id"))
    cur = conn.execute(
        f"INSERT INTO businesses ({','.join(cols)}) VALUES ({placeholders}) "
        f"ON CONFLICT(source, source_id) DO UPDATE SET {updates}",
        values,
    )
    return cur.lastrowid


def get_business(conn: sqlite3.Connection, source_id: str) -> sqlite3.Row:
    return conn.execute(
        "SELECT * FROM businesses WHERE source_id = ? AND source = 'ghanayello'",
        (str(source_id),),
    ).fetchone()


def export_rows(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM businesses ORDER BY weakness_score DESC, reviews_count DESC"
    ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        for col in ("emails", "images", "videos", "weakness_flags", "categories"):
            d[col] = jloads(d.get(col))
        d["socials"] = jloads(d.get("socials"), {})
        out.append(d)
    return out
