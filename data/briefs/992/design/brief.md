# Mintz Lights — design brief

Lead #992 · Nairobi, Kenya · research audit 2026-10-22 · MODE = DESIGN (no code written)
Folder: `data/briefs/992/` · Deliverables: this brief, `design-tokens.json`, `screens/`,
`motion-storyboard.md`, `asset-usage.md`, `pitch-teaser.md`, `open-questions.md`.

---

## 1. Design digest

| | |
|---|---|
| **Business** | Mintz Lights (MINTZ Lights / Mintzlights) |
| **Claimed category** | `event_organisers` — understates the business |
| **Verified category** | Event lighting design, décor & styling, furniture/tent/seating hire, truck hire and event logistics |
| **City** | Nairobi — 46 Kigwa Road, Ridgeways (physical, verified). Postal: P.O. Box 6185-00300 |
| **Language** | English. Swahili is inferred from the Nairobi customer base and **not** observed in their posts — no Swahili copy was written |
| **Audience** | Nairobi households and companies planning weddings, ruracios, birthdays, corporate events and launches; secondarily other event companies needing trucks and gear |
| **Tone** | Practical, local, unhurried. Their own public copy is "Luxury event planning & styling for birthdays, weddings, ruracios & corporate events"; the logo adds **"styled accordingly"** |
| **Trading since** | At least 2016 (planner role documented from Aug 2016; their own listing claims "over a decade"). Exact founding year not published |
| **Score / tier** | 72/100, **tier B** (research re-score from 48/C) |
| **Recommendation** | **PURSUE** — active within 21 days, no working site at all, WhatsApp verified in their own current posts, private business |

### Website status — the whole pitch

**NONE.** Four advertised addresses all return NXDOMAIN (checked 2026-10-22):

- `mintzlights.com` — the link on **their own Facebook page**
- `mintzbergevents.co.ke` — legacy domain on WorldPlaces
- `mintzlights.co.ke`
- `www.mintzlights.yellowpageskenya.com` — Yellow Pages' own "website" field

The pipeline's `website` value is a **Google Tag Manager script** (`gtag/js?id=G-Z6HX57VF8P`), and the
same container ID is recorded against leads 921 and 935. That is a shared tracking tag, not a site.
`has_website = null`, `website_status = unknown` in the dossier — both wrong in opposite directions.

Practical effect: every "website" tap from Facebook, Google or a directory dead-ends. Competitors
with price pages take the search.

### What is verified (used in the design)

- **Services:** event lighting design and installation; décor and styling (luxury / rustic / country);
  furniture and equipment hire — crate tables, director chairs, hay bales, tents, seating, carpets;
  truck hire and event logistics. Corporate events, weddings, birthdays, ruracios, product launches.
- **Payment:** Cash, M-Pesa, Cheque. Currency KES. *(The old pipeline outreach said "MoMo" — Ghana rail, wrong country. Never repeat it.)*
- **Hours:** Mon–Fri 08:00–17:00 (Fri to 18:00), Sat 08:00–13:00, Sun closed. Sources differ on
  Saturday start (08:00 vs 09:00) — the design uses 08:00 and this is flagged in `open-questions.md`.
- **Contacts:** WhatsApp **+254 757 924 836** (current, printed in every Sep–Oct 2026 post);
  office line +254 729 854 408 (listed, older, may go unanswered); **mintzlights@gmail.com**
  (current, from their own post footers); mintzbergservices@gmail.com (legacy directory email).
- **Recent, dated work** (from their page, Sep–Oct 2026): 23 Sep Garissa load-out · 25 Sep event build ·
  28 Sep Evoria SPA styling, Adyen Plaza, Ngara · 30 Sep lighting setup · 1 Oct trucks opened for hire.
- **Facebook:** active, page id 1473399672955768, last verified post 1 Oct 2026.

### Assets — what actually exists

| Asset | Reality | Use |
|---|---|---|
| Facebook avatar | 200×200 JPEG — **an event photo, not a logo**: white tent, periwinkle-blue and magenta drapes, gold chairs, flowers, lawn | Small evidence tile in the DÉCOR column, captioned as 200px preview |
| YP Kenya "logo" | 205×240 PNG — **the real mark**: script "Mintz Lights", "styled accordingly", indigo #404090, "CORPORATE EVENTS \| PARTIES \| WEDDINGS" | Design-system board only (raster, too low-res for the site) |
| Post media | Setup photos exist (lighting builds, rustic furniture, Garissa load-out, Evoria SPA) but are behind a Facebook login wall | **Not asserted.** Photo slots in the job log; shot list in `asset-usage.md` |
| Video | Two clips, 0:31 and 0:27, attributed to `@MintzLights` by a search index; platform unconfirmed | Not used |

**Hero-ready count: 0.** Both files are preview-only. This is the single largest constraint and it
shapes the whole design (see §3).

> Research tagged the 200×200 avatar as a "480×480 crisp logo". It is neither 480 nor a logo.
> Corrected here; the logo/photo roles are swapped relative to the research table.

### Brand

- **Mark:** script wordmark, indigo **#404090** (sampled from the file), strapline "styled accordingly",
  and the services line "CORPORATE EVENTS | PARTIES | WEDDINGS".
- **Tagline:** their own — "Luxury event planning & styling for birthdays, weddings, ruracios & corporate events".
- **Colours:** extracted (research says "not extractable" — it is, from the logo and the avatar):
  periwinkle-indigo #404090; drape periwinkle #A0B0E0; drape magenta #A02060; tent white #F0F0F0.
- **No type specification exists.** No vector logo, no brand guide.

### Competitors and the look to beat / avoid

| Competitor | How they look | What we do instead |
|---|---|---|
| **Events & Party Rentals** — ranks for "lights and chandeliers for hire in Nairobi" | White catalogue page, SEO city list (68 areas), published price table (fairy lights from KSh 2,500, chandeliers from KSh 10,000), WhatsApp button | No fake prices, no white catalogue. One lit stage + a real job log. Rates "on request" until the owner publishes them |
| **Dacia Events** | Full production house, 17-set gallery, named brand clients (Safaricom, KCB, Heineken) | We have no client logos and will not borrow any. The design sells the craft (light, rig, truck), not borrowed prestige |
| **Onyx Kenya** | Corporate AV since 2000, Riverside Drive, technical spec language | We keep the technical vocabulary where it is real (cue, gel, gobo, load-out) but never pose as a 25-year AV house |

**Must not look like:** a white rental catalogue with a price table · a wedding-Instagram grid ·
gold-on-black "luxury" bar · a generic dark site with ballroom stock photos.

---

## 2. Anti-repetition check

Checked against `~/Documents/design-log.json` (15 pages).

Last three designs: **VITALRAY** (patient report: paper/slate/teal, Fraunces + Public Sans) ·
**KENTE KINETIC** (woven colour-block, Anton + Outfit + Caveat, indigo/ivory/gold) ·
**CROSSROADS** (wayfinding planks, Staatliches + Alegreya Sans, clay/asphalt/oxide).

- **Archetype:** none of those three. New: cinematic dark, built as a **cue console** machine.
- **Hero:** no porthole, no clip-path portal, no split-flap board, no signpost planks, no dark
  "viewer" frame. New: a **lit proscenium / stage-plot panel** beside a call-sheet type column.
- **Fonts:** Big Shoulders + Big Shoulders Stencil + Hanken Grotesk + Spline Sans Mono. None in the
  banned last-five list, none reused anywhere in the log.
- **Palette:** blackout / gel magenta / tent white / periwinkle. Not in the banned palette list; the
  log's ambers, indigos, teals and clays are not repeated.
- **Motion:** beam sweep, cue re-rig cross-fade, call-sheet frame slide. No marquee, no sheen, no
  ken-burns, no gate wipe, no route draw, no stamp landings.

---

## 3. Creative brief

**The one big idea**
> **A build is a cue stack.** The page starts in blackout. You call one of three cues — LIGHT, DRESS,
> MOVE — and the stage re-rigs, because that is literally what this company does for a living.

**Feeling (3 adjectives):** backstage-calm · precise · warm-dark.

**The signature moment — THE CUE CONSOLE**
Three cues sit under the headline. Only one is ever live: its chip is wider, filled, stamped
`CUE LIVE`. Calling another cue re-lights the stage panel (angle and gel temperature shift), swaps
the inclusions for that line of work, and carries the choice into the quote sheet, where it becomes
the first line of a WhatsApp message. One gesture, three pieces of real information, zero decoration.

**Why an archetype of cinematic dark and not a photo-first site**
Selection rules say imagery decides. Here the asset count is 0 hero-ready — so photo-first,
editorial and "cinematic full-bleed" as usually executed are all off the table. But this client *makes
light for a living*: darkness is not a fallback, it is their medium. The stage panel is drawn entirely
in light (beam, haze, floor pool, lamp) and is honest about what is missing — the stage foot reads
`[ YOUR VENUE PHOTO GOES HERE ]`. The site becomes a lighting rig instead of a photo album.

**Hero composition:** the custom-metaphor slot — a **stage-plot panel** (496×596) beside the
call-sheet copy, hard seam, no floating glass, no cut-out subject. Depth comes from four real layers:
blackout ground → truss and haze → beam cone and floor pool → type and controls.

**Motion trio:** masked beam wipe on load · cue re-rig cross-fade · call-sheet gel-frame slide.
Ambient: slow haze drift. Details in `motion-storyboard.md`.

**What this must NOT look like**
- The competitor pattern: white page, 40-item rental grid, "from KSh 2,500" table.
- A wedding content page: blush, script fonts, confetti, emoji.
- The Ghana portfolio pattern already in the log: gold-on-black, heritage cloth, gold sheen.
- Generic "luxury dark" with a stock ballroom photo and a centred headline.

---

## 4. Design system

Full tokens in `design-tokens.json`. Summary:

**Colour** — brand-derived, not invented: the logo gives #404090; their own event photo gives the
magenta and periwinkle. The accent is split into three steps because a single magenta cannot pass
AA both as small text on light and as small text on dark.

| Token | Hex | Role | Share | Contrast |
|---|---|---|---|---|
| `blackout` | `#0B0B12` | page ground, stage dark | 58% | 17.1:1 with tent |
| `struck` | `#14141F` | panels, preview panel, sticky bar | 18% | 16.0:1 with tent |
| `tent` | `#F2EFE9` | neutral light band, cards | 16% | 17.1:1 with blackout |
| `gel` | `#E6175F` | **large** display type only (H1 accent, ≥54px) | 4% | 4.1:1 on blackout (AA large) |
| `gel-fill` | `#C2104F` | control fills carrying small white text (CTA, pill, band) | — | 5.26:1 with tent |
| `gel-label` | `#FF5D8F` | small mono labels on dark | — | 6.74:1 on blackout |
| `peri` | `#8A8CE8` | soft secondary, rules, small labels on dark | 3% | 5.46:1 on blackout |
| `peri-deep` | `#404090` | brand ink, labels on light | — | 7.77:1 on tent |
| `haze` | `#A9ABB6` | body text on dark | — | 8.58:1 on blackout |
| `ink-mute` | `#57545E` | body text on light | — | 6.45:1 on tent |

No gradients except light itself (beam, lamp glow, floor pool, haze band). No shadows. No purple-blue
gradient anywhere.

**Type** — one superfamily for display, one grotesque for text, one mono for data:

- Display **Big Shoulders** 800, tracking −0.02em, line-height 0.86–0.95.
- Accent **Big Shoulders Stencil** 800 — *one word per headline*. The stencil is the gobo: light
  passes through the letter, which is why only the verb is cut (LIGHT / DRESS / MOVE / ROOM).
- Body **Hanken Grotesk** 400/500/600, 13–19px, line-height 1.5–1.6.
- Data **Spline Sans Mono** 400/500, 7.5–11px, tracking +0.1em — cues, dates, hours, payments.
- Scale: hero **88** desktop / **54** mobile · section **46** / 34 · row **30** / 26 · sub **20** / 16 ·
  body **17** / 13 · caption **12** / 11 · mono **10** / 8.
  *Optical note:* Big Shoulders is ~0.68× the width of a normal grotesque at the same size, so 88
  reads like ~60 — inside the pipeline's readability floor while still carrying the room.

**Shape, texture, icon**
- Radius 0 everywhere, 1px only on the lamp body. No pills except the WhatsApp control (999px).
- Rules: 1px at 12% white on dark, 1px at 12% ink on tent; 2px only under the job-log header.
- Texture: one haze gradient band; a 200×200 photo used as evidence, never as decoration.
- Icons: Lucide line, 1.5px, 10–16px, only inside mono labels or CTAs. No emoji, no filled sets.

**Components:** nav (wordmark · 4 links · phone pill) · buttons (tent solid / black solid / gel-fill
WhatsApp / 1px outline) · cue chip (idle 140px, live 186px with `CUE LIVE`) · job-log row with status
chip · accordion row with +/− · WhatsApp message card · photo drop · sticky mobile bar · footer.

---

## 5. Screens

Exported at 1×: `screens/02-home-desktop.png` (1440×3421), `screens/03-home-mobile.png` (390×3755),
`screens/04-quote-desktop.png` (1440×1173), `screens/05-quote-mobile.png` (390×1353),
`screens/01-design-system.png` (1440×1249). Frame-by-frame specs in `screens/README.md`.

**Home — section order** (deliberately not the order of any previous design):

1. **Topbar** — wordmark, Ridgeways, four links, WhatsApp pill with the real number.
2. **Hero** — `CUE 01 / HOUSE TO HALF`, H1 *WE LIGHT IT. / WE DRESS IT. / WE MOVE IT.*, one-sentence
   proposition, cue console, primary CTA + job-log link + payment rail, stage plot, hours/road/contact strip.
3. **The rig** — four **bare columns with vertical rules** (not cards): LIGHT / DRESS / HIRE / MOVE,
   each with real inclusions. The only photo on the page sits in DRESS with its 200px caption.
4. **Job log** — a light call-sheet table of five dated jobs; status chips LOAD-OUT / BUILT / FITTING /
   HIRE; `PHOTO SLOTS OPEN` note instead of a fake gallery.
5. **The cues** — sticky title left, three-row accordion right. Lighting only / Styling + hire / Full
   production. **No prices** — `RATE ON REQUEST · M-PESA DEPOSIT` instead.
6. **Tagline band** — full-bleed gel with their own logo line, *STYLED ACCORDINGLY.*
7. **The desk** — address, hours table, payment chips, both numbers labelled, current email, yard/pin
   note, and the **prefilled WhatsApp card** (ruracio example, editable fields).
8. **Footer** — wordmark, socials, legal line, service line.

**Quote sheet (tier-B inner page)** — the second page the outreach promises: a numbered quote sheet
(what / where / when / guests / one photo) that assembles a WhatsApp message live in a dark preview
panel, with the send button and the desk details. Mobile version stacks the same sheet with a
single-button sticky bar.

**Sections deliberately skipped:** reviews (4.6 from one 2025 blog, 4 reviews on a low-confidence
mirror — not publishable), team (no named staff except a public planner role, no portraits), gallery
(no verified images), map (three conflicting coordinates ~1.1 km apart), prices (none published),
Instagram/TikTok (handles unconfirmed).

**Conversion path:** WhatsApp everywhere, in their real format — `wa.me/254757924836` with the message
pre-written. Mobile carries a fixed two-button bar (WhatsApp / Plan a build), so the path never scrolls
away. M-Pesa appears as the deposit rail, never as a fake "pay now".

---

## 6. Self-critique

**Pass 1 — five flaws found**

1. **Three identical cue chips** — the exact banned pattern, in miniature. Fixed: the live chip is
   186px and taller with a `CUE LIVE` stamp; idle chips are 140px.
2. **Rig cards had ~90px of dead space** at the bottom of a 392px box. Fixed by deleting the boxes:
   four bare columns, unequal widths (340 / 310 / 360 / 318), equal rule heights.
3. **Job-log header collapsed** into `DATEWHEREWHAT` — text cells ignore width without a fixed frame.
   Fixed with fixed-width cell frames; verified at 1×.
4. **Magenta failed AA for small text** (3.93:1 on both grounds) and every small gel label inherited
   the failure. Fixed by splitting the accent into label / light / fill steps and re-checking all pairs.
5. **Research mislabelled the assets** — the "480×480 logo" is a 200×200 event photo. Fixed: the photo
   becomes evidence in DÉCOR, the real logo appears only on the system board, and neither is in the hero.

**Pass 2 — five more**

6. The hero's left column ended 100px above the stage base, leaving a flat void. Added the stage foot
   (`THE ROOM IS YOURS. WE JUST SET THE LIGHT.`) and the floor line so the eye travels down the beam.
7. The job log read as a plain table. Added status chips and a hover spec that lands a 96×96 gel frame
   from the row — turns the missing gallery into an interaction.
8. Mobile H1 at 58px sat ~5px from the edge on a 390 screen. Reduced to 54.
9. The quote page was a generic form. Rebuilt as a **quote sheet** with a live message preview — the
   only place on the site where the visitor sees exactly what they are about to send.
10. The tagline band read "hot pink event page". Darkened the fill to #C2104F so the electric magenta
    stays where light belongs — in the beam and the display type.

**Divergence check:** can a stranger confuse this with the last three? VITALRAY is pale paper and
clinical; KENTE is flat woven colour blocks; CROSSROADS is clay and signposts. This is blackout,
one beam, condensed type and a cue console. No shared archetype, hero, palette, pairing or motion.
Could it be any business's site? No: the cue names, the inclusions, the Garissa/Garden Estate/Evoria
references, the truck column and the M-Pesa rail are this company's facts only.

---

## 7. Honesty register

- Every price, rating, review, staff name, client logo and photograph of their work is **absent or
  visibly marked as a slot**. Nothing was invented.
- `[ YOUR VENUE PHOTO GOES HERE ]` is a designed placeholder, not a claim.
- `RATE ON REQUEST` is true: no pricing is published anywhere reachable.
- "STYLED ACCORDINGLY." is their own logo strapline — the only borrowed copy, and it is theirs.
- The 4.6 rating is **not** shown. It comes from one 2025 neighbourhood blog post and a low-confidence
  mirror; outreach is instructed not to quote it as current.
- M-Pesa, cash and cheque are from their own listing; the deposit *amount* is a placeholder.
- Hours show 08:00 Saturday; sources disagree by an hour (flagged).
