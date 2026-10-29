# AGENTS.md — working on the lead pipeline in a new session

Ground rules for AI agents (and humans onboarding) doing further work in this
repo.
Read this plus `README.md` first; the pipeline state lives in `data/leads.db`
(single source of truth — never regenerate it from scratch).

## Repo map

```
leads                 zsh wrapper — entrypoint for every command (scan/audit/
                      score/media/brief/brief-remove/show/reasons/export/
                      optout/outcome/socials/briefs/status)
pipeline/config.py    countries, cities, categories, RATE_LIMITS, weights, tiers
pipeline/run.py       all CLI commands; every mutation is a cmd_* function here
pipeline/sources_local.py  parsers: ghanayello, businessghana, kenyayp, blng,
                      ngex (cards_* / *_profile_details per source)
pipeline/geo.py       multi-country phone normalization (phone_countries)
pipeline/db.py        schema + store helpers (upsert_business, find_duplicate,
                      is_opted_out, source_log_failure, set_weights …)
pipeline/scoring.py   acceptance score -> tier
pipeline/audit.py     website checks, evidence JSON
pipeline/brief.py     stage-5 dossiers (data/briefs/<lead_id>/{dossier.json,
                      summary.md, outreach.txt}; migrates legacy flat files)
pipeline/socials.py   DuckDuckGo name-matched social hunt (stage 6)
tests/                67 unit tests — keep green (`python -m unittest discover -s tests`)
data/                 leads.db (+WAL), briefs/, exports/, scan evidence
```

## Hard rules (never violate)

1. **$0 sources only.** No paid APIs, no login-bypassing, no scraping behind
   auth. Check `robots.txt` before wiring any new source; if disallowed, log
   the refusal to `scan_failures` and move on.
2. **Politeness delays** come from `config.RATE_LIMITS` — never remove or
   shortcut one to make a scan faster.
3. **Opt-out is permanent.** `store.is_opted_out` is checked before any
   insert/contact use. Never clear the opt-out table.
4. **SQLite is the single source of truth.** One writer at a time (WAL):
   "database is locked" = another scan/agent is mid-write — wait, don't
   retry-spam. Agents should not hold long transactions.
5. **No fabricated data.** Ratings, phones, reviews only from real fetched
   pages; if a source's metadata is template junk (e.g. stale JSON-LD on
   ngex.com), parse visible text instead and note it in code comments.

## Code conventions

- Every lead row has a stable **id** — all CLI views print it (`#id`), scan
  tickers announce it (`new #N (id X)`), and briefs folders are named by it.
  Reference leads by id in `brief`, `brief-remove`, `outcome`, `show`.
- `leads` rotates: every listing records its rows in `served_leads` and the
  next run serves fresh leads (score order among unserved). `--all` replays
  without marking; `--reset` clears history (country-scoped with `--country`).
  Never delete rows from `businesses` to "refresh" the view.
- CLI mutations go through `cmd_*` functions in `pipeline/run.py`; parsing
  lives in `pipeline/sources_local.py`; schema/table changes in
  `pipeline/db.py` (+ manual `ALTER TABLE` when no migration helper exists).
- Every scan loop should emit the ticker pattern: `[scan MM:SS | source]`
  boot line, per-fetch announcements, `new #N: name (phone ✓)` /
  `dupe match: backfilled …` lines, final elapsed time.
- New country: add to `config.COUNTRIES`, add phone prefix support in
  `pipeline/geo.py phone_countries`, add rate limit key, add tests.
- New source adapter: `cards_<src>(html, base)` + `<src>_profile_details()`
  in sources_local.py; wire into the country's scan dispatch; dedupe via
  `store.find_duplicate` (backfill missing fields on dupe match).
- Website extraction from directory detail pages must use `plausible_site()`
  (rejects GTM/analytics/CDN hrefs) — never the raw first external link.
  Kenya's whole queue once carried `googletagmanager.com/gtag/js` as its
  website; the same noise class can appear on any directory.

## Open work streams (pick one per session)

1. **Grow non-Ghana pools** — run remaining Kenya/Nigeria categories:
   `leads scan --country kenya --category fashion`, `--country nigeria …`.
2. **ngex live proof (Nigeria)** — `leads scan --country nigeria --category
   lawyers` runs the new fast keyword-search source; first sweep was never
   executed (DB was write-locked that day). Verify scores ingest rating +
   reviews_count, then grow categories.
3. **brands dedupe pass** — fuzzy-brand collapse before any outreach: e.g.
   "Pizza Man – Chicken Man" vs "Pizzaman Chickenman" share one WhatsApp
   number but sit as two rows. Implement normalized brand match on
   phone_e164 similarity, merge rows carefully (keep evidence from both).
4. **Ghana enrichment pass** — Ghana leads can't rise past the old health
   ceiling because review counts came only from NG/KE sources; consider a
   review-count backfill sweep for GhanaYello profiles.
5. **socials retry** — `leads socials --limit 15` after the DuckDuckGo
   cooldown (previous burst → 202 challenge; stage aborts cleanly). Wait
   hours between attempts.
6. **audit backlog** — 833 leads with audit:unknown; run `leads audit`
   batches to lock "no website / thin presence" evidence (this is what
   moves C→B eligibility).
7. **Design demos** — bespoke pen.dev pages for chosen leads (see below).
8. **Housekeeping bugs** (quick wins):
   - `leads` wrapper lines 7–8: header-continuation lines lost their `#`
     prefix → "--country: command not found" noise on every run.
   - `cmd_brief --lead` matches only `id`/`source_id`; wrapper bridges fuzzy
     names, but direct CLI use with a name fails (`??no-match`).

## The design (pen.dev) stream

- Canvas: Pen Desktop app → `lead-pipeline.pen`
  (`~/.pencil/documents/<doc-hash>/lead-pipeline.pen`). Open the app first —
  agents must not launch it.
- **Anti-repetition ledger** `~/Documents/design-log.json`: every shipped
  design's archetype/hero/palette/fonts/motions + banned lists. Read it
  before designing; append the new design and extend every banned list after.
- Workflow per design: pull the lead's row read-only (`SELECT *` with
  `mode=ro`) → concept brief → 1440 desktop + 390 mobile artboards →
  screenshots + self-critique per section → fix in place (never delete/rebuild)
  → log to ledger.
- Shaders live beside the .pen file; **WebGL1-safe only**: no `fwidth`
  (needs an extension), no ES3; premultiplied-alpha care for transparent
  fills; `@resolution`/`@time` annotations for uniforms.
- Stock assets: use the tool's `Generate("stock", id, query)`; if pending
  placeholders stall, copy a loaded sibling's image fill instead of waiting.
- Current pipeline status: 15 ledger pages. Single-page designs (SKC/
  CROSSROADS/VITALRAY artboards) + one full-site system: KENTE KINETIC (Can
  Do, 5 screens × desktop/mobile + DS board + motion storyboard). Travel
  archetypes burned — cinematic night, FIELD ATLAS, WINDOW SEAT, CROSSROADS,
  KENTE KINETIC; travel leads need a 5th fresh archetype. VITALRAY (medical
  imaging, Nairobi #935) burned the "patient-report / scan-viewer" medical
  archetype — medical/clinic leads need a different one.
- Readability floor (2026-10-21 tone-down pass): new designs launch at the
  reduced scale — desktop headline ≤ 68, CTA ≤ 50, quote ≤ 30, stats/section
  titles ≤ 27; remember stained-glass rule: accents muted (see ledger
  `readability_pass`/`readability_baked` notes).

## Session etiquette

- Keep heavy network work bounded: a scan run is naturally slow (blng = 41 s
  per request); prefer starting it and reporting time expectations rather
  than sitting idle.
- Don't touch `data/exports/` or `data/briefs/` contents by hand; they're
  re-generable artifacts.
- Run the test suite after any change to pipeline/ files. Tests must pass.
