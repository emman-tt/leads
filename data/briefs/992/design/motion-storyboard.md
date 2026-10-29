# Mintz Lights — motion storyboard

Lead #992 · MODE = DESIGN · companion to `brief.md` and `design-tokens.json`.
Six annotated frames. Three moves carry the design; everything else is ambient or feedback.
**No WebGL, no video, no parallax on type.** All motion is CSS clip-path, transform and opacity.

---

## 0. Motion principles

1. **Light does the moving.** The beam, the lamp core and the floor pool are the only elements
   allowed to travel a long distance. Type does not float, rise, or fade up in sequence.
2. **One reveal, not eleven.** The load is a single wipe. Sections below the fold do not animate in.
   Scrolling is reading, not a performance.
3. **Cue changes are cuts, not transitions.** Calling a cue is a 480ms re-rig with three
   simultaneous property changes — the same way a lighting desk snaps to a new stack.
4. **Nothing loops near text.** Ambient drift is a background layer at ≤0.8 opacity, 24s, and it
   never touches a glyph.
5. **Reduced motion is a first-class version**, not a fallback: same information, same hierarchy,
   zero travel.

**Token reference**

| Token | Value | Used for |
|---|---|---|
| `beam` | `cubic-bezier(0.16, 1, 0.30, 1)` | the load wipe, cue re-rig |
| `type` | `cubic-bezier(0.22, 1, 0.36, 1)` | the stencil word's gel shift |
| `ui` | `cubic-bezier(0.4, 0, 0.2, 1)` | chips, nav, sticky bar, focus |
| `exit` | `cubic-bezier(0.4, 0, 1, 1)` | outgoing panel content |
| `micro` 120 · `quick` 200 · `base` 320 · `cue` 480 · `load` 1400 | ms | — |

---

## Frame 01 — BLACKOUT (t = 0 → 120ms)

The page's first paint is the design's ground state: `#0B0B12`, no beam, no type.

| Layer | State at t=0 |
|---|---|
| Ground | `blackout` flat, full viewport |
| Truss + haze | 1px rules at 12% tent, haze band at opacity 0 |
| Beam cone | `clip-path` closed to a 1px line at the lamp origin (x 38%, y 22% of the stage panel) |
| Floor pool | opacity 0 |
| Type column | present in the DOM, inside the same clip as the beam → **invisible but not `opacity:0`** |
| Nav | fully rendered (it is above the clip), logo + 4 links + phone pill |

Why this order: the LCP element is the H1 text, but the first *painted* state is the black ground.
The nav and the phone pill are legible within 120ms, so the page is never a blank screen — it is a
dark room with the desk lamp already on.

**Do not:** fade the whole page in from black. That is a different, slower idea and it delays the
one thing worth waiting for.

---

## Frame 02 — LAMP STRIKE (120ms → 1400ms)

The signature load. One wipe, executed by the beam itself.

```
 t  120 ──────────────────────────────────────────────── 1400
     │ lamp core on  │  beam sweep  │  type cleared  │  settle
     │   0→240ms     │  240→1180ms  │   1180→1400    │
```

| # | Element | Property | From → To | Duration | Easing | Delay |
|---|---|---|---|---|---|---|
| 1 | Lamp core (radial) | opacity + scale | 0 / 0.86 → 1 / 1 | 240ms | `beam` | 0 |
| 2 | Beam cone | `clip-path` diagonal edge | line at lamp → past stage foot | 940ms | `beam` | 120 |
| 3 | Beam cone | opacity | 0 → 0.9 | 240ms | `beam` | 120 |
| 4 | Haze band | opacity | 0 → 0.55 | 600ms | `beam` | 300 |
| 5 | Floor pool | opacity + 28px x-shift | 0 / −28px → 1 / 0 | 720ms | `beam` | 420 |
| 6 | Stencil word (`LIGHT`) | colour | `tent` → `gel` | 600ms | `type` | 900 |
| 7 | Supporting copy | opacity | 0 → 1 | 200ms | `ui` | 1000 |
| 8 | Cue console | opacity | 0 → 1 | 200ms | `ui` | 1080 |

The wipe edge is a **45° diagonal travelling down-right from the lamp**, not a horizontal curtain.
Everything inside it — headline, stage plot, cue chips — is revealed by the same edge, so the page
reads as one lit object rather than a stack of animated blocks.

Frame 02 detail: the stencil word is the last thing to resolve, and it resolves by *changing colour*,
not by moving. Light passing through a gobo cuts the letter; the colour shift is that cut. This is
the only colour animation on type in the entire site.

**Total load choreography: 1.4s.** After 1400ms nothing else on the page is moving except the haze.

---

## Frame 03 — CUE LIVE (rest state)

This is a state, not a transition, but it defines what the next frame interrupts.

- Three chips in a reserved 482px track: live chip **186px** + two idle at **140px** + 2×8px gaps.
  The track width never changes, so the CTA below never shifts (CLS = 0).
- Live chip: `gel-fill` `#C2104F`, tent label, `CUE LIVE` stamp at mono 8, tracking +0.16em,
  top-right inside the chip, 1px tent rule at 24% above it.
- Idle chip: `struck` fill, 1px `rule-dark`, tent label at 70% opacity.
- No pulse, no breathing, no blinking dot. **A live cue is steady** — that is what "live" means on a desk.

---

## Frame 04 — THE CUE CALL (480ms)

The signature interaction. Trigger: tap/click a cue chip, or `←`/`→` between chips with
`Enter`/`Space` to call. The cue also pre-selects the matching service on the quote sheet, which
then allows any combination (the sheet is multi-select; a real build is often two or three).

| # | Element | Property | From → To | Duration | Easing | Delay |
|---|---|---|---|---|---|---|
| 1 | Outgoing chip | width | 186 → 140 | 200ms | `ui` | 0 |
| 2 | Outgoing chip | fill / stamp | `gel-fill` → `struck`, stamp 1→0 | 200ms | `ui` | 0 |
| 3 | Incoming chip | width | 140 → 186 | 200ms | `ui` | 60 |
| 4 | Incoming chip | fill / stamp | `struck` → `gel-fill`, stamp 0→1 | 200ms | `ui` | 60 |
| 5 | Beam cone | rotate around lamp origin | 0° → +4° (LIGHT) / −5° (DRESS) / 0° (MOVE) | 480ms | `beam` | 0 |
| 6 | Beam hue | colour stop | `#E6175F` ↔ `#8A8CE8` lerp | 480ms | `beam` | 0 |
| 7 | Floor pool | translateX | 0 → +34px / −30px / 0 | 480ms | `beam` | 0 |
| 8 | Lamp core | scale | 1 → 1.06 → 1 | 480ms | `beam` | 0 |
| 9 | Outgoing inclusions | opacity | 1 → 0 | 120ms | `exit` | 0 |
| 10 | Outgoing inclusions | translateY | 0 → −4px | 120ms | `exit` | 0 |
| 11 | Incoming inclusions | opacity | 0 → 1 | 200ms | `ui` | 140 |
| 12 | Incoming inclusions | translateY | 6px → 0 | 260ms | `beam` | 140 |
| 13 | H1 stencil word | colour | stays `gel` (no change) | — | — | — |

Rules that keep this from becoming a toy:

- The three cue labels never move position on screen — only their widths inside the reserved track.
- The beam moves **at most 5°**. It is a re-rig, not a screensaver.
- The inclusions panel crossfades in place at a fixed height (the tallest cue's row count) so the
  page below does not jump.
- The chosen cue is written to `#cue=light|dress|move` (replaceState, no history spam) and to the
  quote sheet's first line, so the interaction has a consequence beyond itself.
- `aria-live="polite"` announces: *"Cue 2, Dress. Styling and hire selected."* Focus stays on the
  chip that was pressed.

**Mobile:** identical timings, different control. The console becomes a stacked cue list — three
full-width 60px rows with 6px gaps, the live row filled and stamped, idle rows `struck` with a `+`.
The stage panel sits above it at full width, so the re-rig is visible without scrolling. Rows never
reorder and the row heights never change, so the CTA below stays put.

---

## Frame 05 — GEL FRAME ON THE JOB LOG (200ms)

The job log is a call-sheet table with five dated rows and no photographs. Hover or keyboard-focus
on a row lands a 96×96 gel frame from the row's right edge — the gallery that does not exist,
expressed as an interaction instead of a fake image.

| # | Element | Property | From → To | Duration | Easing |
|---|---|---|---|---|---|
| 1 | Gel frame | translateX | +24px → 0 | 200ms | `ui` |
| 2 | Gel frame | opacity | 0 → 1 | 160ms | `ui` |
| 3 | Row ground | background | transparent → `#F2EFE90A` | 120ms | `ui` |
| 4 | Row date rule | scaleY | 0 → 1 (2px, `gel-deep`) | 200ms | `ui` |
| 5 | Status chip dot | colour | `peri` → `gel-deep` | 120ms | `ui` |

The frame is **empty by design**: 1px `gel-deep` border, 45° hatch at 8%, and mono micro
`PHOTO SLOT` centred. It is not an image placeholder pretending to be an image; it is a labelled
slot. On touch devices there is no hover — the frame is always visible at 64×64, `PHOTO SLOT`
shrunk to `SLOT`.

**Focus parity:** the same states fire on `:focus-visible`, so keyboard users get the identical
reveal. No hover-only content anywhere on the page.

---

## Frame 06 — QUOTE SHEET ASSEMBLY (320ms per line)

The quote sheet's only motion is the message writing itself into the preview panel. It is the one
place a visitor sees exactly what they are about to send.

| # | Moment | Property | Spec |
|---|---|---|---|
| 1 | A field completes | preview line background | `gel` at 8% → transparent, 320ms `ui` |
| 2 | A field completes | preview line text | 120ms opacity swap, no per-character typing |
| 3 | Service chip toggled (field 1) | first line text + beam hue in preview | 320ms `ui` |
| 4 | Photo attached | 1px border → 1px `gel-deep`, caption swaps to filename | 200ms `ui` |
| 5 | Send pressed | button translateY 0 → 1px, 120ms `micro`; then border of preview → `gel-deep` | 120 + 320ms |
| 6 | Send success | mono line `OPENING WHATSAPP…` fades in | 200ms |
| 7 | Validation error | field outline 1px `gel-label`; message below at 12px | instant, no shake |

No typewriter effect. A typewriter makes a 6-line message take four seconds and reads as a gimmick;
a line flash says "this line is now part of your message" in a third of a second.

---

## Ambient track (the only loop)

- **Haze drift:** one 24s loop, `opacity 0.55 → 0.8 → 0.55`, background-position drift of 18px,
  `ease-in-out`. Applied to the haze band only. Never to text, never to the stage plot's type.
- **No** second ambient loop. No floating particles: dust motes in a beam is the single most
  over-used "atmospheric" move on the web and it would read as decoration, not lighting.
- The loop pauses when the tab is hidden (`document.visibilityState`), and is removed entirely under
  reduced motion.

---

## Reduced motion version

`@media (prefers-reduced-motion: reduce)` — the design must still feel deliberate, not stripped.

| Element | Motion version | Reduced version |
|---|---|---|
| Load | 1.4s beam wipe | 200ms opacity on the whole stage panel; beam static at 45°, full opacity |
| Stencil word | gel colour shift | gel from first paint |
| Cue call | 480ms re-rig | 200ms opacity crossfade of beam + inclusions; no rotation, no hue lerp |
| Inclusions | 4px rise, 260ms | instant swap |
| Gel frame | 24px slide | appears at 120ms opacity, no travel |
| Accordion | height 320ms | instant open/close |
| Haze | 24s drift | static band |
| Sticky mobile bar | slides up 200ms | present from first paint |
| Smooth scroll | `scroll-behavior: smooth` | `auto` |

Also honour `prefers-reduced-transparency` (beam at 0.5 opacity flat) and `prefers-contrast: more`
(beam removed entirely; 1px tent rules at 40%).

---

## Implementation notes

- **No JS animation library.** The load is a CSS `clip-path` transition on a class added on
  `DOMContentLoaded`; the cue call is a data-attribute swap (`[data-cue="dress"]`) that CSS keys off.
  Budget: **< 4KB of JS** for cues, accordion, quote sheet and sticky bar.
- **Animate only `transform`, `opacity`, `clip-path`.** Never `width` on the chips — use a fixed
  482px track and `flex-basis` transitions inside it, or a `scaleX` on a background layer.
- **`will-change`** on the beam cone only, removed after load (`transitionend`).
- **Fonts:** subset Big Shoulders / Stencil to the glyphs used; `font-display: swap`; preload the
  display face only. A late display font must not reflow the hero — reserve line boxes with
  `size-adjust` on the fallback.
- **Gradients, not images:** beam, lamp, floor pool, haze are four CSS gradients. Total image weight
  on the home page is one 200×200 JPEG (preview tile).
- **Test matrix:** Safari 16+ (clip-path on gradients is the risk), Chrome 110+, Firefox 110+,
  Android Chrome on a 360px viewport, iOS Safari with reduced motion on.
- **LCP target** < 2.5s on Slow 4G; **CLS** 0 (the cue track and inclusions panel are the two
  places it would come from); **INP** < 200ms.

---

## QA checklist

- [ ] Load wipe completes in 1.4s and never blocks interaction (chips are tappable during it).
- [ ] All three cues are reachable by keyboard; the stamp state is announced.
- [ ] No layout shift when the live chip changes between LIGHT / DRESS / MOVE.
- [ ] Cue choice appears as line 1 of the WhatsApp message and survives a page reload via the hash.
- [ ] Job-log frame appears on focus, not only hover.
- [ ] Reduced motion: every section readable with animation off; no element stuck at `opacity: 0`.
- [ ] Haze loop stops on tab hide.
- [ ] No animation runs on a `prefers-reduced-motion` device on first paint.
