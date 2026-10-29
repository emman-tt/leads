# Mintz Lights (lead #992) — verification report
Audit date: 2026-10-22 · Analyst: research pass · Folder: data/briefs/992
Country: Kenya · City: Nairobi (Ridgeways / Kigwa Road)

## 1. Lead Digest (as claimed by the pipeline)

| Field | Claimed value |
|---|---|
| Business | Mintz Lights |
| Category | event_organisers |
| City / country | Nairobi, Kenya |
| Claimed website | `https://www.googletagmanager.com/gtag/js?id=G-Z6HX57VF8P` |
| Phone | +254729854408 |
| WhatsApp | +254757924836 |
| Email | mintzbergservices@gmail.com |
| Address | "P.O.Box: 6185 - 00300 Nairobi" |
| Socials | none recorded (`socials: {}`) |
| Assets | 0 images, 0 videos, hero-worthy 0 (preview-only) |
| Score / tier | 48 / 100, tier C |
| Factors | health 4 (thin activity data) · readiness 5 (1 channel, funnel incomplete) · need 3 ("site ~functional") · pay 7 ("premium category") · reach 8 (phone/WhatsApp on listing) · assets 3 (too few images) |
| Why-pitch | "strongest selling point: Pay and Health" |
| Objection | "no time on the phone — send WhatsApp proof (screenshots)" |
| Outreach claims | "nothing behind your listing to browse or book", "no site of yours", "WhatsApp booking, **MoMo** payments", "I have **already put together a free preview mockup based on your own photos**" |

## 2. Data-quality flags found (before research)

1. **Website is a tracking script, not a site.** The URL is a Google Tag Manager `gtag/js` file. The same container ID `G-Z6HX57VF8P` is also recorded as the "website" of leads 921 and 935 — a shared tag, wrongly attributed to the business.
2. **Yellow Pages' own "website" field is a dead directory subdomain**: `www.mintzlights.yellowpageskenya.com` does not resolve (NXDOMAIN).
3. **Fabricated preview claim.** `assets = 0`, `hero_worthy_count = 0`, yet the draft says a mockup "based on your own photos" already exists. Not supported by the data.
4. **Wrong payment rail.** "MoMo" is Ghana; Kenya is **M-Pesa** — and every listing/payment field for this business says Cash / M-Pesa / Cheque.
5. **Garbled sentence**: "customers find your event organisers listing on Nairobi" — not a sentence, and not true (they have an active Facebook page, not just a listing).
6. **Self-contradictory scoring.** `need = 3` justified by "site ~functional" while `has_website = null`, `website_status = unknown`; `reason` names "Health" as a selling point while health is the weakest-but-one factor and described as "unverified active".
7. **Category drift**: recorded as `event_organisers`; the business is event lighting / décor / styling **plus equipment and truck hire**.
8. **Address incomplete**: dossier carries only the postal address; the physical address (46 Kigwa Road, Ridgeways) was missing. Map pins in source listings disagree by ~1.1 km.
9. **Email out of date**: `mintzbergservices@gmail.com` (directory) vs `mintzlights@gmail.com` used in the business's own posts since September 2026.
10. **Two different numbers**, neither labelled: which one is WhatsApp was unknown.

## 3. Verified findings

| Finding | Source (URL) | Date seen | Confidence |
|---|---|---|---|
| Business exists and is active: "Luxury event planning & styling for birthdays, weddings, ruracios & corporate events", 46 Kigwa Road, Ridgeways, Nairobi; call/WhatsApp +254 757 924 836; mintzlights@gmail.com | EvePla mirror of the Facebook page (posts 21/09–01/10/2026) — https://www.evepla.com/KE/Nairobi/1473399672955768/MINTZ-Lights ; original page facebook.com/mintzlights (id 1473399672955768) | 2026-10-22 | High |
| Recent activity: near-daily posts, incl. 1 Oct truck-hire announcement, 30 Sep lighting-setup post, 28 Sep Evoria SPA (Ngara) styling job, 25 Sep event build, 23 Sep load-out for a **Garissa** event | EvePla mirror, ibid. | posts dated 21/09–01/10/2026 | High |
| Service range: event lighting design, décor/styling, rustic furniture hire (crate tables, director chairs, hay bales), tents/seating/carpets, and trucks for event logistics | YP Kenya profile; EvePla mirror posts | 2026-10-22 | High |
| Payment modes published: Cash, M-Pesa, Cheque | https://www.yellowpageskenya.com/business-category/events/business-details/2852069-mintz-lights | 2026-10-22 | High |
| Hours: Mon–Fri 08:00–17:00 (Fri to 18:00), Sat 08:00–13:00, Sun closed | YP Kenya + https://www.apexbusinesspages.com/listing/mintz-lights/ | 2026-10-22 | Medium (sources differ on Sat start: 08:00 vs 09:00) |
| Rating 4.6 stars, described as a top event-management company in Kigwa near Garden Estate | https://www.beyondforest.org/post/garden-estate-nairobi | 2025-01-15 | Medium (old, single source) |
| "4 reviews" on Google-derived listing, phone ending 924*** (matches +254 757 924 836) | https://www.keonline.biz/business/207628-mintslights | undated (seen 2026-10-22) | Low |
| Public business role: **Lucy Mburu**, Event Planner at Mintz lights since Aug 2016 ("over a decade" matches YP copy) | https://linkedin.com/in/lucy-mburu-20b0ba65 | 2026-10-15 | Medium — business role only; ownership **not** publicly stated |
| Business's own public image: page avatar/logo (480×480 JPEG, HTTP 200) | https://graph.facebook.com/1473399672955768/picture?type=large | 2026-10-22 | High |
| Directory-uploaded logo, 205×240 | https://api.yellowpageskenya.com/images/KEN/logos/23043.WebP | 2026-10-22 | Medium (likely same mark, lower res) |

**Disputed / stale points:** three different coordinates for the same business (−1.2257,36.8510 / −1.2215,36.8614 / −1.22569,36.8513); two email addresses; two phone numbers (0757 924 836 is the one used in current posts, 0729 854408 is the older directory line); WorldPlaces still advertises `mintzbergevents.co.ke`.

## 4. Website verdict: **NONE**

- `mintzlights.com` — listed as the website on their own Facebook page and on goafricaonline — **NXDOMAIN** (Google DNS status 3, A and NS both empty), 2026-10-22. Confidence: High.
- `mintzbergevents.co.ke` — the older domain on WorldPlaces — **NXDOMAIN**. High.
- `mintzlights.co.ke` (`www.`) — **NXDOMAIN**. High.
- `www.mintzlights.yellowpageskenya.com` (YP's "website" field) — **NXDOMAIN**. High.
- No live site, so no HTTPS/mobile/booking path to assess. The only presence is social + directory listings, and every one of those links is dead.
- Practical effect: anyone tapping "website" from Facebook, Google or a directory hits a dead end. That is the pitch.

## 5. Asset shortlist (preview-only)

| # | URL | Platform | Type | Res | Quality | Tag |
|---|---|---|---|---|---|---|
| 1 | https://graph.facebook.com/1473399672955768/picture?type=large | Facebook | logo/avatar | 480×480 | crisp graphic, no watermark, below 1080 hero floor | logo |
| 2 | https://api.yellowpageskenya.com/images/KEN/logos/23043.WebP | YP Kenya | logo | 205×240 | low-res duplicate | logo |

**No hero-worthy images could be verified.** Their Facebook page clearly posts setup photos (lighting builds, rustic furniture, Garissa load-out, Evoria SPA), but post media is not reachable without logging in — see Unverified. Two short videos attributed to handle `@MintzLights` (0:31 and 0:27, one posted hours before crawl) surfaced only through a search index — platform unconfirmed.

## 6. Score table (weights: health .25, readiness .20, need .20, pay .15, reach .10, assets .10)

| Factor | Old | New | Why it changed | Source |
|---|---|---|---|---|
| health | 4 | **8** | Posts almost daily to 1 Oct 2026; active client work; 10+ years trading | EvePla/FB mirror |
| readiness | 5 | **7** | WhatsApp + current email + active page; still no site, no price list, no booking form | FB posts, DNS |
| need | 3 | **9** | Both domains they advertise are dead; no site at all; directory links broken | DNS checks |
| pay | 7 | **6** | Real corporate/rental work (Garissa, SPA fit-out, truck hire) implies budget, but no published pricing to confirm | EvePla posts |
| reach | 8 | **9** | WhatsApp number in every post with "call/DM to book" | FB posts |
| assets | 3 | **2** | Only a 480×480 logo verified; photos exist but are locked behind login | graph.facebook.com |
| **Total** | **48 (C)** | **72 (B)** | | |

Confidence in the new total: **medium-high** — health, need and reach are high-confidence; assets is low-confidence (understates real photo inventory), pay is medium.

## 7. Recommendation: **PURSUE** (tier B, 72/100)

Passes all hard disqualifiers: active within 21 days, no strong existing site, working WhatsApp, private business (not government/NGO/franchise). The only thing standing between them and tier A is verified imagery — their own Facebook feed is the source, and that is exactly what the first reply should unlock.

**Open questions:** who owns the business (publicly only Lucy Mburu's planner role is documented); whether `mintzlights.com` was cancelled deliberately; whether they want truck hire marketed separately; do they answer WhatsApp from the 0757 line during weekday hours only.

## 8. Unverified / could not open

- `facebook.com/mintzlights` — HTTP 400 to non-logged-in clients. Post text read via EvePla mirror; post images not retrievable. Reason: login wall.
- Instagram `instagram.com/mintzlights` — HTTP 200 but generic login page; API returned 401. Existence of the handle **not confirmed**.
- TikTok `@mintzlights` — profile HTML blocked; oEmbed 400. Handle **not confirmed**.
- `vanlett.com/h/eventplanner` — blocked by Anubis bot-check (HTTP 511 on mirror fetch). The `@MintzLights` video snippet came from the search index only.
- `kenya.worldplaces.me` review page — HTTP 511 to automated fetch.
- Google Maps place page — JavaScript shell, no listing data in HTML; rating/review count therefore taken from secondary mirrors (4.6 / 4 reviews).
- No pricing, packages or client list published anywhere; nothing invented here.
