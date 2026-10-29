# Mintz Lights — pitch teaser

Lead #992 · MODE = DESIGN. This is the package that goes into the WhatsApp thread, not a portfolio
page. Three static frames today; one 18-second cut once the site exists.

Everything here is aligned to `outreach_v2.txt`, with the places where that copy over-promises
called out in §5.

---

## 1. The three frames

Send in this order, as three separate images (WhatsApp compresses albums and the mono labels die).
No PDF, no link — the point is that it opens in the thread.

| # | File | Size | One-line caption to send under it |
|---|---|---|---|
| 1 | `screens/02-home-desktop.png` | 1440×3421 | **The page opens in blackout, then one beam lights the room. The three chips are the three things you sell — light, dress, move.** |
| 2 | `screens/03-home-mobile.png` | 390×3755 | **Same page on a phone, where most of your customers will see it. WhatsApp is always one tap away.** |
| 3 | `screens/04-quote-desktop.png` | 1440×1173 | **And when someone wants a price, they fill this in and it writes the WhatsApp message for them — what, where, when, guests.** |

Do **not** lead with the design-system board (`01-design-system.png`). It contains the note
`VECTOR NEEDED` next to their logo; that is a production note for us, not a message for a prospect.

---

## 2. The message

Short, specific, and it ends with a question they can answer in one word. Matches Variant A in
`outreach_v2.txt`, plus a line for the screenshots.

> Hi Mintz Lights 👋 Emmanuel here. I saw your posts from late September — the Garissa load-out and
> the lighting builds — and went looking for the site on your page. **mintzlights.com doesn't resolve
> anymore**, so anyone who taps it just hits a dead end.
>
> I build simple sites for event and décor companies in Nairobi. I mocked one up from what's already
> public — the Ridgeways address, your hours, the September jobs, and your one public photo — so you
> can see the idea. Three screenshots coming.
>
> *[send 1, 2, 3 with the captions above]*
>
> No charge to look, and nothing is published. If it's useful, the next step is you sending me five
> or six photos of real setups and I'll put them in. If it's not a priority, just say so and I won't
> come back. — Emmanuel

Why this shape:

- The dead link is **verifiable by them in one tap**, so the first line is not a pitch, it is a fact.
- "Mocked up from what's already public" is precise. It does not claim their photos are on the page.
- "Nothing is published" answers the fear that a stranger put their brand online.
- The opt-out is in the first message, per the pipeline rules.

---

## 3. The 18-second cut

For a screen recording once the page is built (or a click-through of the canvas). Vertical 1080×1920,
captions burned in, **no music** — it will be watched on mute in a workshop.

| Time | Frame | On screen | Caption |
|---|---|---|---|
| 0.0–1.2s | Black | nothing | `mintzlights.com` → `NXDOMAIN` in mono, then clears |
| 1.2–3.0s | Load | beam wipes down-right, type resolves | `EVERY TAP TODAY IS A DEAD END` |
| 3.0–5.5s | Hero | hold, live chip on LIGHT | `SO WE BUILT THE RIG INSTEAD` |
| 5.5–8.5s | Cue call | tap DRESS → beam warms, inclusions swap | `ONE TAP RE-RIGS THE PAGE` |
| 8.5–11.5s | Rig + photo tile | scroll, 200px tile passes | `LIGHT · DRESS · HIRE · MOVE` |
| 11.5–14.0s | Job log | hover lands the gel frame | `REAL JOBS. NO FAKE GALLERY.` |
| 14.0–16.8s | Quote sheet | message assembles, send pressed | `THE QUOTE WRITES ITSELF` |
| 16.8–18.0s | End card | black, wordmark + number | `MINTZ LIGHTS · +254 757 924 836` |

Rules for the cut: no zoom-punch transitions, no whoosh, no cursor circle, no fake "loading" spinner.
A lighting company's promo should feel like a cue stack, not a template ad.

---

## 4. What each frame is actually proving

| Frame | The objection it answers | The proof in the image |
|---|---|---|
| Home desktop | "We already have a Facebook page, why a site?" | A page that cannot be scrolled past in a feed: hours, address, payment rail and a quote path, all in one screen |
| Home mobile | "Our customers are on phones" | 390px layout designed separately, not a squashed desktop; sticky WhatsApp bar |
| Quote sheet | "People just call us anyway" | The call is still the goal — the form's output *is* a WhatsApp message, pre-written |

The design deliberately does **not** answer "how much". No price is published anywhere reachable, so
the sheet says `RATE ON REQUEST · M-PESA DEPOSIT` and the reply is a conversation, which is how they
already work.

---

## 5. Claims audit — outreach vs. what was designed

The v2 outreach was written before the design existed. Four lines need adjusting if they are reused
verbatim; none of them are dishonest, but three would be over-claimed by the screenshots.

| Outreach line | Status | Why | Say instead |
|---|---|---|---|
| "mintzlights.com doesn't load / no longer resolves" | ✅ Supported | All four domains NXDOMAIN, checked 2026-10-22 | Keep as is |
| "the work looks good" (re: photo posts) | ✅ Supported | Posts are visible via the mirror and are clearly setup photos | Keep — it is about the posts, not the site |
| "gallery" | ⚠️ **Over-claims** | The design has **no gallery** — no retrievable images. It has a job log and labelled photo slots | "a job log with photo slots that fill as you send me pictures" |
| "three packages (lighting, décor/rustic furniture, truck + logistics)" | ⚠️ **Reframe** | The design has three **cues**, not priced packages. Calling them packages invites "how much" | "three ways to book — lighting only, styling and hire, or full production" |
| "M-Pesa deposit note" | ✅ Supported | M-Pesa is on their own listing; the *amount* is a placeholder | "M-Pesa deposit note" is fine |
| "46 Kigwa Road with a map pin" | ⚠️ **Not built** | Three sources give coordinates ~1.1 km apart. A pin would be a guess | "46 Kigwa Road, with the pin sent on WhatsApp" |
| "one clean page" | ⚠️ Minor | It is a home page **plus a quote sheet** | "one page and a quote sheet" |
| "three different numbers / old P.O. Box" | ⚠️ **Check the adjective** | Two numbers are verified; "old" P.O. Box is not established — the box may still be current | "the directories still show a P.O. Box and a second number" |
| "using your own photos" | ⚠️ **Careful** | Only a 200px event photo is reachable. The site currently shows **one** of their photos and a labelled slot for the rest | "using what's already public, plus slots for the photos you send" |
| "4.6 rating" | ❌ **Never** | One 2025 neighbourhood blog, low-confidence mirror, 4 reviews | Do not mention |
| "MoMo" | ❌ **Wrong country** | Kenya rail is M-Pesa; their listing confirms cash / M-Pesa / cheque | "M-Pesa" |
| "fast on mobile data" | ⏳ **Unproven until build** | Design intent: one 200px image, four CSS gradients, <4KB JS | Say "built to be light on data" only after the build is measured |

---

## 6. Likely replies

| They say | Reply |
|---|---|
| "How much for the site?" | Give the price for the build, not for their event. Never quote event pricing — that is their business, not ours |
| "Can you use the photos on our page?" | "Yes — send me the originals on WhatsApp rather than screenshots, and I'll pick the best six. I won't pull them off Facebook." |
| "We already have someone doing it." | "No problem. Want me to send the draft anyway so you have something to compare?" Then stop. One ask, no second pitch |
| "Remove the prices / we don't want a quote form." | Easy — the cue accordion and the WhatsApp card both stand on their own. The quote sheet is a second page, not a dependency |
| "Can you add our Instagram?" | "Send me the handle — I couldn't confirm it from outside" (it is unverified; see `open-questions.md`) |
| Silence after 3 days | Use the day-3 follow-up from `outreach_v2.txt` verbatim. One line, one question |

---

## 7. Do-not-send list

- `01-design-system.png` — internal production notes, `VECTOR NEEDED`, contrast ratios.
- `design-tokens.json`, `brief.md`, `motion-storyboard.md` — these describe the machine; they are not
  the pitch.
- Any image of a venue or event that is not theirs.
- Any figure: price, rating, review count, years in business, number of events, crew size.
- The words "award-winning", "best in Nairobi", "one-stop shop", "unforgettable" — banned in the
  tokens for a reason.
- A promise that the site is live. It is a mockup, and the message says so.
