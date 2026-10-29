# Mintz Lights — asset usage

Lead #992 · MODE = DESIGN. Every asset below was checked on 2026-10-22.
**Hero-ready count: 0.** Both files that exist are preview-only until the owner approves publication.

---

## 1. What exists

| # | File | Source | Real size | What it actually is | Status | Where it may appear |
|---|---|---|---|---|---|---|
| A1 | `mintz-avatar.jpg` | `graph.facebook.com/1473399672955768/picture?type=large` | **200×200** JPEG | An **event photo**, not a logo: white marquee tent, periwinkle and magenta drapes, gold Chiavari chairs, white flowers, lawn | Preview only | One 200×200 evidence tile in **DRESS** (home, desktop + mobile) with its size caption |
| A2 | `mintz-yp.webp` | `api.yellowpageskenya.com/images/KEN/logos/23043.WebP` | **205×240** WebP | The **real mark**: indigo script "Mintz Lights", strapline *styled accordingly*, line "CORPORATE EVENTS \| PARTIES \| WEDDINGS" | Preview only | **Design-system board only.** Never in the site header or hero |
| A3 | Facebook post media | Page id 1473399672955768, posts 21 Sep – 1 Oct 2026 | unknown | Setup photos do exist (lighting builds, rustic furniture, Garissa load-out, Evoria SPA styling) | **Not retrievable** — login wall | Nowhere. Slots only |
| A4 | Video, two clips | Attributed `@MintzLights` by a search index | 0:31 / 0:27 | Platform unconfirmed (likely TikTok) | Unverified | Nowhere |

### Two corrections carried from research

1. Research recorded A1 as a **"480×480 crisp logo"**. It is a 200×200 JPEG **event photo**.
   The hero floor is 1080px; at 200px this cannot be a background, a hero, or a card image.
2. Research recorded A2 as a "low-resolution duplicate of the logo". It is the **only real logo**
   in existence. It is still only 205×240, so it is unusable as site furniture — a raster script
   mark at 240px tall next to 72px nav type would disintegrate.

> Neither file is in the hero. That is deliberate, not an oversight: the hero is drawn in light
> (see `brief.md` §3), and the one real photograph is used as *evidence* at the size it can bear.

---

## 2. Placement map

| Screen | Slot | Asset | Treatment | Caption |
|---|---|---|---|---|
| DS board | Logo specimen | A2 | 205×240 at 1×, on `tent`, 1px rule, 3 swatches sampled beside it | `CLIENT MARK · 205×240 · RASTER · VECTOR NEEDED` |
| DS board | Ground / palette | — | Colour chips only | hex + contrast ratio |
| Home desktop | **DRESS** column | A1 | 200×200, radius 0, no filter, no overlay, 1px `rule-dark` frame, sits below the inclusions list | `FROM YOUR PAGE · 200PX · PREVIEW` |
| Home mobile | **DRESS** column | A1 | same 200×200, left-aligned, caption wraps to two lines | same |
| Home desktop/mobile | Stage foot | — | `[ YOUR VENUE PHOTO GOES HERE ]` — designed placeholder, 1px dashed tent at 24% | — |
| Home desktop/mobile | Job log | — | Five rows; hover/focus lands an empty 96×96 `PHOTO SLOT` frame | `PHOTO SLOT` |
| Quote sheet | Photo field | — | 96px drop zone, `1px ink 25%`, mono `ADD ONE PHOTO (OPTIONAL)` | filename after attach |
| Footer | Socials | — | Facebook only (verified). No Instagram/TikTok glyph until handles are confirmed | — |

**Total published image weight on the home page: one 200×200 JPEG.** The rest is type, rules and
four CSS gradients.

### Why the logo stays on the board

The mark is a script wordmark with a thin-stroke flourish. At 205×240, downscaled into a 72px nav,
the hairline strokes alias into mush and the strapline becomes a grey smudge. The board shows it
honestly at native size with the note that a vector is required. The site's wordmark is set in
Big Shoulders — a deliberate typographic stand-in, **not** a redrawing of their logo.

---

## 3. Shot list (what to ask the owner for)

Nine frames. Ask for originals, not screenshots of Facebook. Order = impact.

| # | Shot | Why it earns its place | Framing | Where it lands |
|---|---|---|---|---|
| S1 | **The room, lit, before guests** — wide, full rig visible | This is the hero the site cannot currently show. One good frame changes the page | 3:2 landscape, 2400px wide, tripod, no people, lights at show level | Stage plot / hero band |
| S2 | **Beam on a drape** — gel colour against fabric, haze visible | Proves they design light, not just hang it | 3:2, expose for the highlight, let the room fall dark | Rig — LIGHT column |
| S3 | **Table styling** — crate table, director chairs, hay bale, linen | Proves the DRESS claim with their actual inventory | 3:2 and 4:5 crop, daylight or warm interior | Rig — DRESS column (replaces A1 at full size) |
| S4 | **Tent exterior at dusk** — marquee glowing from inside | The one image that sells "we bring the venue" | 3:2, blue hour, 10 min window | Job log / quote page header |
| S5 | **Load-out** — truck, crates, dawn, Garissa-type job | Truck hire is a real differentiator; nobody else shows the 5am | 3:2, available light, motion allowed | Job log row / MOVE column |
| S6 | **Hands at work** — rigging a clamp, taping a cable, no faces | Craft without needing model releases | 4:5 or 1:1, close, shallow depth | Cue accordion / detail strip |
| S7 | **Rig detail** — cable run, dimmer, gel frame stack | Technical credibility for corporate buyers | 1:1 macro, hard side light | DS board / job log hover frame |
| S8 | **Vertical venue frame** — the same room, portrait | Mobile hero and quote page need a 4:5, not a crop of a 3:2 | 4:5, 1600px tall | Mobile stage / quote |
| S9 *(optional)* | **10–12s clip of one cue change** — lights go from house to show | The signature moment, filmed. Only if they will shoot it | vertical + horizontal, locked-off, no music | Ambient slot — **not autoplay with sound** |

**Brief to send them (short version):** *"Phone camera is fine if it's recent. Landscape, hold still,
turn the room lights down but leave the event lights on. Send the originals on WhatsApp — don't
send screenshots, they lose the detail. No people's faces unless you have their OK."*

---

## 4. AI image policy

The design currently uses **zero generated imagery**, and the shipped site should stay that way for
anything that represents their work.

- **Never** publish a generated image as a photograph of a Mintz Lights event.
- **Never** put a generated venue in the hero, the job log, or the quote page.
- A generated frame may be used **only** in an internal concept deck, watermarked
  `AI CONCEPT — NOT A MINTZ JOB`, and never sent to the client without that label visible.
- If they ask for "something in the hero now", the answer is the designed placeholder plus S1 —
  not a stock ballroom.

For reference, the three concepts that were considered and **not** built (kept here so nobody
re-proposes them as a shortcut):

1. *"Nairobi garden wedding at dusk, festoon strings, long tables"* — generic, and it would read as
   a stock photo of somebody else's wedding.
2. *"Rigging crew silhouette against a magenta beam"* — attractive, but it implies a crew size and
   a scale of production that is not verified.
3. *"Corporate launch, uplights on a hotel ballroom wall"* — the exact stock image every AV company
   in Nairobi already uses.

Each of these would have made the site look busier and less true.

---

## 5. Technical spec for incoming files

| | Requirement |
|---|---|
| Minimum | 1600px on the long edge; 2400px preferred for S1/S4 |
| Format | JPEG or HEIC original; we export AVIF + WebP at q60–70 |
| Colour | sRGB. Do not send WhatsApp-compressed forwards |
| Weight | ≤ 180KB per delivered image after export; ≤ 60KB for the 200px tile |
| Ratios | 3:2 (landscape), 4:5 (portrait), 1:1 (detail) — crop in-camera where possible |
| Treatment | **None.** No filters, no vignettes, no fake haze, no colour grading beyond white balance |
| Metadata | Strip GPS/EXIF on export (client venues are private homes) |
| Alt text | Describe the job, not the file: *"Tent and draped tables lit for an evening event in Ridgeways"* — never "image1" or keyword stuffing |
| Loading | `loading="lazy"` below the fold, explicit `width`/`height`, `srcset` at 400/800/1200/1600 |

---

## 6. Permission and provenance

- **A1 and A2 are published by the business** on its own Facebook page and its Yellow Pages
  listing. That is not the same as permission to republish. Both stay in *preview* until the owner
  says yes in writing (WhatsApp is fine — screenshot it into the lead folder).
- **Client venues:** Evoria SPA (Adyen Plaza, Ngara) and the Garissa job are named in the job log
  as **dates and places only**, no photographs. Publishing a photo of a client's venue needs that
  client's OK, not just Mintz's.
- **People:** no faces without a release. S6 (hands) is specified that way on purpose.
- **Client logos:** none exist in the research and none may be borrowed from competitors
  (Safaricom / KCB / Heineken appear on Dacia's site, not Mintz's).
- **Never** pull images from the Facebook page by scraping behind the login wall. If the owner
  sends them, they are licensed for this use; if we take them, they are not.

---

## 7. Fill order when the owner sends photos

1. **S1** → stage foot placeholder. Removes the largest honesty caveat on the page.
2. **S3** → replaces A1 in DRESS at 640×480. The 200px preview disappears.
3. **S4** → job log hover frame becomes a real 96×96 crop (still no gallery claim).
4. **S2 / S5** → LIGHT and MOVE columns get one image each.
5. **S8** → mobile stage panel.
6. **S9** → only then consider a moving hero. Not before.

Until step 1 happens, the placeholder stays visible. A labelled empty slot is worth more than a
borrowed photograph.
