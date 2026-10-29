# Ghana / Kenya / Nigeria No-Website / Weak-Website Lead Pipeline

Finds businesses in **Ghana (base), Kenya and Nigeria** with **no website or a weak
website**, qualifies them, enriches them with media + contacts, and produces
per-lead dossiers (JSON + one-page summary + WhatsApp outreach draft).
Everything lives in a local **SQLite** database (`data/leads.db`) — staged,
idempotent and resumable: rerun any command and it continues where it stopped.

**$0 sources only.** robots.txt compliance, opt-out honoring and politeness
delays (1.5–41 s depending on the source) are hard rules, not preferences.

> For agent/AI session guidance (conventions, open work streams, gotchas),
> see **AGENTS.md** in this repo root.

## State snapshot (2026-10-21)

- **895 leads** in DB: 510 C · **385 disqualified** · 60 audit:NONE · 2 audit:OK · 833 audit pending
- Sources live: GhanaYello (808) · BusinessGhana (49) · YellowPagesKenya (22) · BusinessList Nigeria (16) · **ngex.com/Nigeria Galleria adapter built (fast keyword-search source, first live sweep not yet run)**
- Scoring handles all three country codes via `phone_countries` (`pipeline/geo.py`)
- 46 unit tests, all passing (`python -m unittest discover -s tests`)
- DuckDuckGo social-hunt temporarily soft-blocked (stage aborts cleanly; retry after hours-long cooldown)

## The five stages

```
1 scan    discovery per country (see sources table) -> normalize (E.164 phone,
          GPS area, language flag) -> dedupe (phone + brand + area)
          Live ticker on every scan: [scan MM:SS | source] heartbeats,
          new/dupe announcements, elapsed time.
2 audit   website check: NONE / SOCIAL_ONLY / BROKEN / WEAK / OK
          every weak flag stores evidence (metrics JSON, perf where installed)
3 score   acceptance score 0-100 -> tier A (75+) / B (55-74) / C (<55),
          six factors with one-line reasons, hard disqualifiers
4 media   tier A/B only: asset collection from their own site + official-API
          socials (tokens required). Resolution-parsed, quality-scored,
          HERO flag >=1080px. Preview-only storage.
5 brief   per-lead dossier: JSON + one-page markdown + WhatsApp outreach
          draft (language-aware, references one specific audit observation)
6 socials name-matched social-profile hunt (tier C, search-engine pass,
          15 queries/run max, aborts cleanly on engine challenge)
```

### Acceptance-score factors (0-10 each, weighted)

| Factor | Weight | Looks at |
|--------|--------|----------|
| business health | 25% | review counts, posts, directory freshness |
| digital readiness | 20% | socials, WhatsApp Business, MoMo/pay, ads |
| need signal | 20% | no booking/order flow, no CTA, unanswered questions |
| ability to pay | 15% | premium category, branches, visible prices |
| decision-maker reach | 10% | direct phone/WhatsApp vs DM/email only |
| asset availability | 10% | usable images/videos on file |

Hard disqualifiers (tier DISQUALIFIED): inactive >90d, government/NGO,
already has a strong site, no working contact channel, opted out.

Campaign learning: log outcomes (`outcome <lead> replied|meeting|paid|declined`)
and the weights table recalibrates from >=10 logged outcomes (`weights`).

## Countries & sources

| Country | Source(s) | Rate limit | Notes |
|---------|-----------|-----------|-------|
| Ghana (base) | ghana yello (category×city) + BusinessGhana national pass | 1.5s / 3.0s | default `scan`; Tonaton/Jiji opt-in `--classifieds` (Jiji robots-blocked) |
| Kenya | yellowpageskenya.com category→detail | 3.5s | `scan --country kenya --category <slug>` |
| Nigeria | **ngex.com** keyword search (default) | 4.0s | fast: `?q=<term>&place=<City>`; visible-text parse: rating, reviews, phones, address |
| Nigeria | businesslist.com.ng (deep pass) | 41.0s | robots crawl-delay 40; ~6min/category; use `scan --country nigeria --source blng` |

Category slugs live in `pipeline/config.py` (`CATEGORIES`, `COUNTRIES`,
`RATE_LIMITS`). Nigeria maps slugs→search terms in `NGEX_TERMS`
(`pipeline/sources_local.py`).

## Usage

```bash
python3 -m venv .venv && pip install -r requirements.txt
ln -sf "$PWD/leads" ~/.local/bin/leads        # short wrapper (optional)

# discovery (idempotent, resumable)
leads scan --category hotels --city Kumasi --pages 1
leads scan --country kenya --category fashion
leads scan --country nigeria --category lawyers          # ngex fast pass
leads scan --country nigeria --source blng --category ... # slow 40s pass

# qualification chain
leads audit                  # website checks + evidence files
leads score                  # or: python -m pipeline.run score --refresh
leads media                  # tier A/B asset harvesting

# dossiers + inspection
leads brief "SKC"            # by name; bare `leads brief` = all A/B
leads briefs                 # list data/briefs/
leads show "SKC" / reasons "SKC"

# exports & calibration
leads export --tier C --city Accra --category hotels   # CSV
leads optout "+233..." --reason "asked to stop"
leads outcome <source_id> replied --notes "..." --campaign wave1
leads weights
```

Tests: `python -m unittest discover -s tests` (46 tests: scoring good/bad,
dedupe, phone/GhanaPost normalization, country configs, socials, sources).

Every row-referencing view prints the stable row **`#id`** (leads view,
show, reasons, socials, scan ticker `new #N (id X)`), which is also the
briefs folder name — use it for `brief`, `brief-remove` and `outcome`.

## Brief stage mechanics

- `brief --lead <id>` or fuzzy name via wrapper → **one folder per lead**:
  `data/briefs/<lead_id>/{dossier.json, summary.md, outreach.txt}`
- Legacy flat `<city>-<source_id>.{json,md}` files auto-migrate into per-lead
  id folders on the first `brief` run (idempotent)
- `dossier.json` = full dossier (assets sorted by quality/resolution with
  `hero_worthy_count`, merged contacts, brand colors/tagline)
- `summary.md` = one-pager: score factors, why-pitch, likely objection,
  outreach draft; `outreach.txt` = the message alone for copy-paste
- The outreach draft's hook comes from `first_observation()` in
  `pipeline/brief.py` — evidence-first, never generic
- `brief_at` stamped on the lead so bulk runs don't re-brief
- **Deleting a brief:** `leads brief-remove <id | source_id | "name part">`
  removes the folder and clears `brief_at` (re-run `brief` to regenerate)

## Companion: demo-site pipeline (pen.dev)

Each pitched lead gets a bespoke one-page demo design on the pen.dev canvas
(`lead-pipeline.pen`, opened with Pen Desktop). **Anti-repetition ledger:**
`~/Documents/design-log.json` — every shipped design's archetype, hero, palette,
fonts and motions are recorded there and become **banned** for the next design.
Rules of the trade:

- Read the ledger first; never reuse a listed pairing/hero/palette/motion-trio
- Build Desktop 1440 + Mobile 390 for every design; screenshot + self-critique
- Custom shader files live next to the .pen file (`contours.glsl`,
  `routedraw.glsl`, `clouds.glsl`, …); WebGL1-safe only — **no `fwidth`/extensions**,
  no ES3 syntax
- Add the new design to the ledger and extend the banned lists when done

Shipped (10): GOLDEN HOUR, MAAME., EDGE., SMARTWORLD., OCEAN BLUE, AGGDRIC.,
TIPS & TOES., VOBEA SPA · **FIELD ATLAS (SKC Travel & Tours, Akim Oda)** ·
**WINDOW SEAT (Neplink Travel Hub, Santa Maria Accra)**

## Compliance

- Contact details are business-only; sources logged per record; opt-out list
  honoured permanently at every stage
- Media is stored **preview-only** for private mockups until the owner agrees
- Data protection (Act 843 / Kenya DPA / NDPR): polite crawl rates, honest
  User-Agent, stop on 403/429/challenge; `scan_failures` table records every
  refused source instead of bypassing it

## Queries you'll want

```sql
-- Tier-A briefs not yet drafted
SELECT name, city, phone, accept_score FROM businesses
WHERE tier='A' AND brief_at IS NULL ORDER BY accept_score DESC;

-- Nigeria leads already in the pool
SELECT name, city, phone_e164, accept_score FROM businesses
WHERE country='nigeria' AND tier!='DISQUALIFIED';

-- Evidence for every weak flag
SELECT name, website, evidence FROM businesses
WHERE website_status IN ('WEAK','BROKEN');
```
