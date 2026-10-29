# vitalray — demo site for VitalRay Health Solutions (Nairobi)

Built from the burned "patient report" design on the
`lead-pipeline.pen` canvas (VITALRAY — Desktop `PK0ez` / Mobile `l9ry1`).

Same structure as `projects/neplink`: Next 16 (webpack), Tailwind v4,
GSAP + ScrollTrigger, Lenis smooth scroll, flat `app/` components.

## Facts policy

Everything on the page is real client material fetched from
vitalray.com (home, contacts, radiology pages):

- Hours: Mon–Fri 7.00AM–8.00PM · Sat 8.00AM–6.00PM
- Phones: +254 (20) 2731 650/1, +254 737 556 119, +254 705 120 400
- Both sites: Mayfair Centre (Ralph Bunche Rd, Upper Hill) /
  Grenadier Tower (Woodvale Grove, Westlands) — ground floors
- Testimonials: named doctors, verbatim (lightly shortened), no additions
- Insurers: the client's 16-partner list
- Photography: VitalRay's own uploads, hotlinked (their CMS file names
  are odd where their CMS is odd — e.g. `CT-SCAN-VITALRAY-HEALTH.jpg`
  is an MRI room; they are still the real photos)

No ratings, reviews, bios or stock faces were invented. The single
source of truth for copy is `app/site-data.ts`.

## Run

```
npm run dev        # :3000
```
