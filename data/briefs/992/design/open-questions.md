# Mintz Lights — open questions

Lead #992 · MODE = DESIGN. These are for the owner (or the person who answers the WhatsApp), not
for us to guess. Each one lists what the design does **today** so the build is never blocked waiting
for an answer — the default is honest and can be swapped in one edit.

Priority: **P0** blocks the build · **P1** blocks publishing · **P2** improves it later.

---

## 1. The twelve questions

| # | Priority | Question | Why it matters | Current default in the design |
|---|---|---|---|---|
| Q1 | **P0** | **What time do you open on Saturday — 08:00 or 09:00?** | Sources disagree by an hour. Hours appear in the hero strip, the desk table and the machine-readable schema | `SAT 08:00–13:00` |
| Q2 | **P0** | **What deposit do you take, and how should a customer pay it?** Percentage or fixed? M-Pesa till/paybill, or send the number on WhatsApp? | The quote sheet and the payment rail both reference a deposit. Right now the *amount* is deliberately absent | `RATE ON REQUEST · M-PESA DEPOSIT` — no figure, no till number |
| Q3 | **P0** | **Can you send a vector logo (SVG, AI, EPS or PDF)?** And how do you write the name: *Mintz Lights*, *MINTZ Lights* or *Mintzlights*? | The only logo is a 205×240 raster. The site uses a typographic wordmark until a vector exists | Type-set wordmark in Big Shoulders; logo shown only on the internal board |
| Q4 | **P1** | **Are the five dated jobs OK to publish** — 23 Sep Garissa, 25 Sep build, 28 Sep Evoria SPA Ngara, 30 Sep lighting setup, 1 Oct trucks? And may we **name Evoria SPA**? | The job log is the page's proof. Naming a client without permission is a business risk, not a design one | Dates + place names as posted publicly; no client logos, no photos |
| Q5 | **P1** | **May we publish photos of your setups — including venues and any people in them?** | Nothing can replace the 200px tile until this is a yes. It is the single biggest upgrade to the page | One 200×200 preview tile + labelled photo slots |
| Q6 | **P1** | **What is your Instagram handle — and do you have TikTok?** | The research could not confirm either (login walls). A dead social icon is worse than none | Facebook only, linked to the verified page |
| Q7 | **P1** | **Should the office line +254 729 854 408 be shown, or WhatsApp only?** | It is an older directory number and may go unanswered; a missed call on a site is a lost job | Both numbers shown, each labelled: `WHATSAPP` and `OFFICE` |
| Q8 | **P1** | **Which map pin is right for 46 Kigwa Road?** Can you drop one in WhatsApp? | Three sources give coordinates ~1.1 km apart. A wrong pin sends guests to the wrong gate | Address written out; `PIN SENT ON WHATSAPP` — no embedded map |
| Q9 | **P2** | **Do you want prices on the site — "from KSh …" — or keep everything on request?** | Competitors rank on published price tables. This is a business decision, not ours to invent | No prices anywhere; `RATE ON REQUEST` |
| Q10 | **P2** | **Since when have you been trading?** Your listing says "over a decade"; a public planner role starts Aug 2016 | A "since" line is a trust signal, but only if it is exact. An approximate one reads as puffery | No founding year shown at all |
| Q11 | **P2** | **Do you work outside Nairobi?** Garissa suggests yes — is that normal, and is there a travel charge? | Determines whether the desk section says "Nairobi" or "Nairobi + countrywide" | Ridgeways address; no service-area claim |
| Q12 | **P2** | **Should the site have a Swahili version?** | The audience is Nairobi; their own posts are English-only, so none was written | English only |

---

## 2. What each answer changes

**Q1 — Saturday hours.** One string in `design-tokens.json` (`content.hours.sat`) and three
placements: hero strip, desk table, `OpeningHoursSpecification`. If it is 09:00, nothing reflows —
the string is shorter. **Do not** publish "08:00–13:00" and "call to confirm" together; that reads
as uncertainty about their own business.

**Q2 — deposit.** If they give a percentage, it belongs in the quote sheet's summary line, not in the
hero. If they give a till number, it becomes a mono line under the payment chips — never a "Pay now"
button, because there is no payment integration and a fake one destroys trust. If they say "send it
on WhatsApp", the current design already does the right thing and nothing changes.

**Q3 — logo.** A vector unlocks: the nav wordmark, the footer, the favicon, the OG image, and the
quote sheet header. Until then the typographic wordmark stands in. Confirm casing at the same time —
`MINTZ` in caps is how the Facebook page writes it, `Mintz Lights` is how the directories do.

**Q4 / Q5 — proof.** These two together decide whether the page ever gets a gallery. Q4 alone gets
the job log published as-is. Q5 alone gets the 200px tile replaced. Both get the job log's hover
frames filled. If Q4 is a no, the job log is date-only (`23 SEP · NAIROBI`) and loses the Garissa /
Evoria specificity that makes the page credible — worth pushing gently, once.

**Q6 — socials.** Adding an icon is trivial; adding a broken one is not. If they only have Facebook,
the footer says so and looks intentional.

**Q7 — phone.** If the office line is dead, remove it. The page currently gives it equal weight to
WhatsApp (smaller type, but present), which is one tap away from a bad first impression.

**Q8 — pin.** An embedded Google Map with the wrong coordinates is worse than no map: it looks
authoritative. The current `PIN SENT ON WHATSAPP` is a deliberate, honest fallback.

**Q9 — prices.** No design change is needed to add a price band, but it changes the whole posture:
a price table is the competitor pattern the brief explicitly avoids. If they want prices, argue for
**three starting points**, not 40 line items — and only numbers they will honour.

**Q10 — years.** "Over a decade" is their own listing's claim; using it verbatim is defensible but
vague. A year is better. If neither is confirmed, the footer stays year-free.

**Q11 — travel.** Garissa is ~370 km from Nairobi. If they travel routinely, "Nairobi · countrywide
on request" is a real differentiator for corporate clients. Do not claim it from one job.

**Q12 — Swahili.** If yes, the mono labels and the cue names need re-thinking, not translation —
`LIGHT / DRESS / MOVE` will not survive a literal translation as a three-beat. Budget it as a second
design pass, not a copy swap.

---

## 3. Already decided — no need to ask

To keep the list short, these were decided from verified material and are **not** open:

- **No reviews or rating.** The 4.6 comes from one 2025 blog post and a low-confidence mirror;
  outreach is already told not to quote it.
- **No team section.** Only a public planner role exists, no portraits, no confirmed ownership.
- **No embedded map.** See Q8.
- **No Instagram/TikTok icons until confirmed.** See Q6.
- **No prices until they say so.** See Q9.
- **No "MoMo".** Kenya is M-Pesa; the old pipeline copy was a Ghana rail.
- **No client logos.** None exist; competitors' clients are not ours to borrow.
- **No video autoplay.** The two clips are unverified and behind a login wall.

---

## 4. How to ask

One message, numbered, on WhatsApp — not a form, not an email with 12 bullets. The three P0s first,
and say the site can go live without the rest.

> Hi Mintz Lights — three quick things so the mockup becomes a real page:
> 1. Do you open 08:00 or 09:00 on Saturday?
> 2. What deposit do you take, and should the M-Pesa number be on the site or sent on WhatsApp?
> 3. Do you have a vector logo (SVG/PDF), and is it "Mintz Lights" or "MINTZ Lights"?
>
> The rest can wait — I just need those three to publish.

Then stop. Anything they answer goes into `research.json` with the date and the source
("owner, WhatsApp, 2026-10-xx") before it touches the design.
