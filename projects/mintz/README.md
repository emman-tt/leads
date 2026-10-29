# Mintz Lights — demo site

Tier-B demo build for lead **#992, Mintz Lights** (Nairobi, Kenya — event
lighting, décor, rustic furniture + truck hire). Built from the signed-off
**cue-console** design on the `lead-pipeline.pen` canvas (MINTZ — Desktop
`H7nwxd`, Mobile `CI4wW`, Quote Desktop `LLAAR`, Quote Mobile `nZ8kj`,
Design System `c4eHo`) with the verified research dossier in
`data/briefs/992/`.

## Run

```sh
npm install
npm run dev        # http://localhost:3000
npm run build && npm start
```

## Facts policy — read before editing copy

Every customer-facing fact is real client material, verified on
2026-10-22 (see `data/briefs/992/research.md` / `research.json` and the
client's own public posts):

- **Contact**: WhatsApp +254 757 924 836 (current), office +254 729 854 408
  (older line), mintzlights@gmail.com, Facebook facebook.com/mintzlights.
- **Address / hours**: 46 Kigwa Road, Ridgeways, Nairobi; Mon–Thu
  08:00–17:00, Fri to 18:00, Sat 08:00–13:00, Sun closed.
- **Payments**: M-PESA · cash · cheque.
- **Job log**: the five dated rows are the client's own public posts,
  23 Sep – 1 Oct 2026 (Garissa load-out, builds, the Evoria SPA fit-out in
  Ngara, trucks opened for hire).
- **The one photo** (`BUSINESS.avatar`) is the client's own page avatar,
  hotlinked at 200×200 — evidence-sized on purpose.

Never add: invented ratings, testimonials, bios, faces, or stock
photography. The stage plot is CSS gradients because the client had zero
hero-ready photos — don't fill the "photo slot" frames with fake images.
The dead domains (mintzlights.com, mintzbergevents.co.ke) are NXDOMAIN;
do not link to them.

## Structure

Rosait-style flat `app/`, colocated components, single source of truth in
`app/site-data.ts`. Stack: Next 16 (webpack), Tailwind v4, GSAP +
ScrollTrigger + Lenis (`SmoothScroll`, `Reveal`); all entrance/wipe
motion is skipped under `prefers-reduced-motion`.

- `/` — cue-console home: hero console (click LIGHT/DRESS/MOVE → 480ms
  beam re-rig on the CSS stage plot), the rig, job log, the cues
  accordion, tagline band, the desk, footer.
- `/quote` — the quote sheet: a form that writes the WhatsApp message and
  opens `wa.me` with it prefilled. Nothing is submitted anywhere else.

Fonts: Big Shoulders + Big Shoulders Stencil (display), Hanken Grotesk
(body), Spline Sans Mono (labels) — loaded via `next/font`.
