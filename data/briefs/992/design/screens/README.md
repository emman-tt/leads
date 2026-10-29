# Screens — frame specs

Lead #992 · MINTZ Lights. Five PNGs exported from the canvas at **1×** on 2026-10-22.
These are design references, not responsive breakpoints: the desktop and mobile frames were laid out
separately, not scaled from each other.

| File | Frame | Canvas id | Size | What it is |
|---|---|---|---|---|
| `01-design-system.png` | `MINTZ — Design System` | `c4eHo` | 1440×1249 | Palette, type scale, components, rules, real logo specimen |
| `02-home-desktop.png` | `MINTZ — Desktop` | `H7nwxd` | 1440×3421 | Home, full page |
| `03-home-mobile.png` | `MINTZ — Mobile` | `CI4wW` | 390×3755 | Home, full page |
| `04-quote-desktop.png` | `MINTZ — Quote Desktop` | `LLAAR` | 1440×1173 | Quote sheet (tier-B inner page) |
| `05-quote-mobile.png` | `MINTZ — Quote Mobile` | `nZ8kj` | 390×1353 | Quote sheet, mobile |

Canvas: `~/.pencil/documents/9079b90a-9936-43f2-8b48-2708aa0a0129/lead-pipeline.pen`.

> **Board revision.** The design-system board was re-synced to the shipped tokens during the final
> pass: the type scale row now reads **88 / 46 / 30 / 20 / 17 / 13 / 10** with line-heights
> 0.86 / 0.95 / 1.0 / 1.4 / 1.55 / 1.5 / 1.3. The earlier board carried a pre-tone-down scale
> (132/64/40) that did not match the screens. `design-tokens.json` remains authoritative if the two
> ever disagree again.

---

## 01 — Design system (1440×1249)

A working board, not a client deliverable. Five bands:

1. **Header** — wordmark, strapline, board title, lead id + date.
2. **Palette** — five 232×168 chips: BLACKOUT, STRUCK, TENT, GEL, PERI, with hex, role, share and
   measured contrast. The three gel steps (`gel`, `gel-fill`, `gel-label`) are documented in tokens;
   the board shows the electric `gel` only because it is the light colour.
3. **Type** — the *gobo* specimen `WE LIGHT IT.` at 88px with `LIGHT` in Big Shoulders Stencil, then
   the seven-row scale table. One stencil word per headline; everything operational is Hanken;
   numbers, dates and prices are Spline Sans Mono.
4. **Components** — nav specimen (wordmark, three links, WhatsApp pill), three buttons, the cue chip
   pair (LIGHT live / DRESS idle), and the WhatsApp message card.
5. **Rules** — SHAPE, ICON, NEVER, plus the **real logo** at native 205×240 with
   `Real mark, 205×240. Preview only.` It appears here and nowhere on the site.

Build notes: chips are square (radius 0); the only pill is WhatsApp; no shadows anywhere.

---

## 02 — Home desktop (1440×3421)

Content width 1328, page padding 56. Eight bands, in order:

| # | Band | Height (approx) | Contents |
|---|---|---|---|
| 1 | Topbar | 72 | `MINTZ LIGHTS` + `RIDGEWAYS, NAIROBI`, links THE CUES / THE RIG / JOB LOG / THE DESK, gel phone pill `0757 924 836` |
| 2 | Hero | 1090 | `CUE 01 / HOUSE TO HALF`, H1 `WE LIGHT IT. / WE DRESS IT. / WE MOVE IT.` (stencil verbs), 3-line proposition, cue console, `PLAN A BUILD ↗` + `SEE THE JOB LOG`, payment rail, stage-plot panel 496×596, strip: `OPEN MON–FRI 08:00–17:00 · SAT 08:00–13:00` / `ROAD 46 KIGWA ROAD, RIDGEWAYS` / `SAY HI WHATSAPP +254 757 924 836` |
| 3 | The rig | 545 | `02 / THE RIG` + `WHAT WE BRING`, `FOUR LINES, ONE CREW. DRAG →`. Four bare columns with vertical rules, unequal widths: LIGHT (340) / DRESS (310, holds the 200×200 photo) / FURNITURE & TENTS (360) / TRUCKS & LOAD-OUT (318) |
| 4 | Job log | 620 | Light band. `03 / JOB LOG` + `RECENTLY RIGGED`, `SEP – OCT 2026 / NAIROBI · GARISSA`. Five rows at 70px: 23 SEP Garissa LOAD-OUT · 25 SEP Nairobi BUILT · 28 SEP Evoria SPA Ngara FITTING · 30 SEP Nairobi BUILT · 01 OCT Ridgeways HIRE. `PHOTO SLOTS OPEN` note underneath |
| 5 | The cues | 660 | `04 / THE CUES` + `THREE WAYS TO BOOK` left, `RATE ON REQUEST · M-PESA DEPOSIT`; right, three-row accordion — LIGHTING ONLY open (inclusions, `ASK FOR A QUOTE ↗`, reply-hours note), STYLING + HIRE, FULL PRODUCTION closed |
| 6 | Tagline band | 163 | Full-bleed `gel-fill` `#C2104F`, `STYLED ACCORDINGLY.` in display, `RIDGEWAYS / NAIROBI` right |
| 7 | The desk | 640 | `05 / THE DESK` + `COME TO KIGWA ROAD`; address, hours table (Mon–Thu / Fri / Sat / Sun), payment chips, both numbers labelled, email, yard note (`PIN SENT ON WHATSAPP`), prefilled WhatsApp card with REPLACE / ATTACH / DEPOSIT rows |
| 8 | Footer | 150 | Wordmark, FACEBOOK / WHATSAPP / EMAIL, legal line, service line |

**Hero detail.** The stage panel is a drawing, not a photo: truss, haze, beam cone, floor pool, lamp,
a `LIVE / RIG / RIDGEWAYS` annotation strip, and the two lines that make the missing asset honest —
`THE ROOM IS YOURS. WE JUST SET THE LIGHT.` and `[ YOUR VENUE PHOTO GOES HERE ]`. The panel is the
only element on the page with a gradient, and every gradient in it is light.

**Caption under the photo:** `FROM YOUR PAGE · 200PX · PREVIEW` — the size is stated on purpose.

---

## 03 — Home mobile (390×3755)

Designed at 390, content width 350, page padding 20. Same band order, different machines:

- Topbar collapses to wordmark + a 40×40 gel phone button. No hamburger — there are only four
  in-page links, so a sheet would be ceremony.
- H1 at 54px, three lines, `LIGHT / DRESS / MOVE` in stencil. The verb column is the only thing
  that stays wide; nothing is centred.
- **Cue console becomes a stacked list**: three 60px rows with 6px gaps. Live row = `gel-fill`,
  `CUE LIVE` at right, service line beneath the label. Idle rows = `struck`, `+` at right. The
  stage panel sits above the list.
- `PLAN A BUILD` and the job-log link stack; `M-PESA · CASH · CHEQUE` stays one line at 8px mono.
- The rig is four stacked blocks separated by 1px rules, photo tile still 200×200 and left-aligned.
- Job log keeps the table but drops the WHAT column to a second line inside each row.
- Cues: the title becomes a normal heading (no sticky), accordion rows full width.
- Tagline band at 54px over two lines: `STYLED / ACCORDINGLY.`
- Desk: hours become a two-column list; the WhatsApp card follows it.
- **Sticky bar** (56px, `struck`): WHATSAPP (gel) + PLAN A BUILD (tent outline). In the full-page
  export it is drawn at the bottom; in use it is fixed.

---

## 04 — Quote desktop (1440×1173)

`QUOTE SHEET / 01` → H1 `TELL US THE ROOM.` (`ROOM` stencil, gel). One sentence of instruction.
Two columns: form left (848), preview right (452).

**Form** — five numbered fields, values in the mock are examples, not data:

1. `WHAT ARE WE DOING?` — four multi-select chips: LIGHT / DRESS / FURNITURE / TRUCK. Note:
   *pick any — most builds are two or three*. This is deliberately **not** the same control as the
   hero's three exclusive cues: the hero preselects a starting point, the sheet lets a real job be
   a combination.
2. `WHERE?` — venue type + area (`e.g. Karen / Ngara`).
3. `WHEN?` — date + call time (`14 February 2027`, `e.g. guests at 16:00`).
4. `HOW MANY GUESTS?` — a range is fine.
5. `SHOW US THE ROOM` — 96px drop zone, `JPG / HEIC · UP TO 5MB`.

**Preview** — `YOUR MESSAGE, AS IT STANDS`, dark `struck` panel, the message in 17px body, then a
mono WHAT / WHERE / WHEN / PHOTO key-value block, then the full-width `SEND ON WHATSAPP` button and
`Opens WhatsApp with the message written. You can edit it before sending.`

**Below** — `BEFORE YOU SEND` / `FIVE THINGS, THEN WE QUOTE` with the five numbers repeated, the desk
hours and rail at right, then the footer.

Note the absence: no price field, no budget field, no calendar widget, no CAPTCHA. The sheet asks
only what they need to answer once.

---

## 05 — Quote mobile (390×1353)

Same five fields, stacked; chips wrap 2×2; the preview moves **below** the form and is labelled
`YOUR MESSAGE, AS IT STANDS`. The `SEND ON WHATSAPP` button is repeated in a single-button sticky
bar at the bottom (56px), so the action is always reachable while typing.

The FAQ strip collapses to five numbered lines at 8px mono — labels only, no descriptions.

---

## States not visible in a static export

Build these against the motion storyboard; none of them are new inventions:

- **Cue live variants** — DRESS (beam warms, pool shifts left, inclusions = styling/hire) and
  MOVE (beam returns, pool centres, inclusions = trucks/logistics).
- **Cue chip focus** — 2px `gel-label` ring, 2px offset, on both dark and gel fills.
- **Job-log hover/focus** — 96×96 `PHOTO SLOT` frame slides 24px from the row edge; status dot
  turns `gel-deep`.
- **Accordion open/closed** — plus→minus, 320ms height; only one row open at a time.
- **Photo drop** — empty, drag-over (`gel-deep` 1px), attached (filename caption).
- **Quote validation** — missing field = 1px `gel-label` outline + 12px message; no shake.
- **WhatsApp sent** — mono `OPENING WHATSAPP…` under the button for 1.5s.
- **Reduced motion** — see `motion-storyboard.md` §Reduced.

---

## Re-exporting

From the canvas (paths are absolute; export writes into a folder named after the target, so export
to a temp path first and move the inner file):

```js
Export(["c4eHo"], "png", "/tmp/mintz/ds.png", { scale: 1 });
Export(["H7nwxd"], "png", "/tmp/mintz/home-d.png", { scale: 1 });
Export(["CI4wW"],  "png", "/tmp/mintz/home-m.png", { scale: 1 });
Export(["LLAAR"],  "png", "/tmp/mintz/quote-d.png", { scale: 1 });
Export(["nZ8kj"],  "png", "/tmp/mintz/quote-m.png", { scale: 1 });
```

At 2× the desktop home is 2880×6842 — fine for print, too heavy for a chat thread. Keep the 1× set
for the pitch.
