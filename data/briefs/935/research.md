# Vital Ray Medical Imaging (lead #935) — verification report
Audit date: 2026-10-22 · Folder: data/briefs/935
Country: Kenya · City: Nairobi — Upper Hill (Mayfair Centre) + Westlands (Grenadier Tower)

> **Headline:** this lead is not a "no website" opportunity. `vitalray.com` is live,
> HTTPS, mobile-ready and maintained. The pipeline's pitch premise is false, and the
> "WhatsApp" is actually the second switchboard line. Recommendation: **DROP**.

## 1. Lead Digest (as claimed)

| Field | Claimed value |
|---|---|
| Business | Vital Ray Medical Imaging |
| Category | pharmacies |
| City / country | *null* / Kenya |
| Claimed website | `https://www.googletagmanager.com/gtag/js?id=G-Z6HX57VF8P` |
| Phone | +254202731650 |
| WhatsApp | +254202731651 |
| Email | *none* |
| Address | *none* |
| Assets | 0 images, 0 videos, hero-worthy 0 |
| Score / tier | 48 / 100, tier C |
| Factors | health 4 · readiness 5 · need 3 ("site ~functional") · pay 7 ("premium category") · reach 8 · assets 3 |
| Why-pitch | "strongest selling point: Pay and Health" |
| Outreach claims | "**Accra** pharmacies listing", "nothing behind it to browse or book — and **no site of yours**", "**MoMo** payments", "I have **already put together a free preview mockup** based on your own photos" |

## 2. Data-quality flags (found before research)

1. **Wrong city, wrong country.** Draft opens "I went through **Accra** pharmacies listing" — this is a Nairobi business.
2. **Wrong category.** Recorded as `pharmacies`; it is a radiology / diagnostic-imaging centre with a laboratory and day-care unit.
3. **Website is a tracking script.** `googletagmanager.com/gtag/js` — the same container `G-Z6HX57VF8P` is also attached to leads 921 and 992.
4. **The "WhatsApp" is not a WhatsApp.** `+254202731651` is the second line of the switchboard `020 2731650/651` (a Nairobi landline pair). Real mobiles are `0705 120400` and `0737 556119`. No WhatsApp presence found anywhere.
5. **"No site of yours" is false.** `vitalray.com` has been live since at least 2016 and was still being edited in Nov 2025.
6. **Fabricated preview.** "free preview mockup based on your own photos" — assets = 0, hero-worthy = 0.
7. **MoMo in Kenya.** Their panels and site use insurance billing, M-Pesa/cash at the desk.
8. **No email recorded** although `info@vitalray.com` is published on every page.
9. **pay 7 justified by "premium category (pharmacies)"** — the category is wrong, and the justification ignores the real signals (VC backing, bank facility, insurance panels).
10. **"strongest selling point: Pay and Health"** contradicts health 4/10 "unverified active".
11. **Empty geography** — city, address, coordinates all null, so the summary headline prints "?".
12. **Name drift** — Vital Ray / VitalRay / Vitalray Health Solutions Ltd; dedupe risk against future scans.

## 3. Verified findings

| Finding | Source | Date seen | Confidence |
|---|---|---|---|
| Legal entity **VitalRay Health Solutions Ltd**, trading as VitalRay Medical Imaging; private Level-4 outpatient facility (MFL 26795) | https://hosi.co.ke/hospitals/vitalray-health-solutions/ ; https://kmhfr.health.go.ke | 2026-10-22 | High |
| Two branches: Ground Floor, Mayfair Centre, Ralph Bunche Rd, Upper Hill; Ground Floor, Grenadier Tower, Woodvale Grove, Westlands. P.O. Box 12981-00100 | https://vitalray.com/find-us-in-here-westlands-and-upperhill/ | 2026-10-22 | High |
| Hours: Mon–Fri 07:00–20:00, Sat 08:00–18:00, Sun & PH closed | same + https://jubileeinsurance.com/ke/wp-content/uploads/2025/05/JHIL-2025-Panel.pdf | 2026-10-22 | High |
| Website **live**: HTTPS 200, mobile viewport, WordPress ("better-health" theme), 13 reachable pages | https://vitalray.com/ | 2026-10-22 | High |
| Services: MRI, CT, ultrasound, digital X-ray, ECG/echo, laboratory, day-care/oncology support | https://vitalray.com/radiology-mri-ctscan-xray-ultrasound/ | 2026-10-22 | High |
| Insurance panels: APA, Old Mutual, Jubilee, CIC, Sanlam, Madison, Heritage, GA, First Assurance, Minet/AON, Henner, Takaful + NHIF/SHA | https://vitalray.com/ | 2026-10-22 | High |
| Listed on Jubilee 2025 panel and CIC Afya Bora 2026 panel as an imaging provider | Jubilee JHIL-2025-Panel.pdf; https://ke.cicinsurancegroup.com/wp-content/uploads/2026/08/AFYA-BORA-PROVIDER-PANEL-2026-1.pdf | 2025 / 2026-08 | High |
| ~37 employees (LinkedIn; Tracxn as of Jul 2026); estimates elsewhere range 17–55 | LinkedIn company page; https://tracxn.com/d/companies/vitalray | 2026-09-10 | Medium |
| VC-backed (AAIC / Asia Africa Investment & Consulting); Japanese bank facility Apr 2024 | https://aaicinvestment.com/ ; https://prtimes.jp/main/html/rd/p/000000046.000115382.html | 2024-04-15 | High |
| Leadership: **Dr. Unni Miyengi** — CEO & Chief Radiologist since Mar 2014; **Reuben Warriah** named as representative/founder | https://linkedin.com/in/dr-unni-miyengi-85a26a4 ; AAIC portfolio page; PR Times | 2026-08-29 / 2024 | Medium (two names; ownership split not public) |
| Founded 2012 (Tracxn) vs 2014 (PR Times, LinkedIn) — **disputed** | both above | — | Low |
| Google rating **3.4 / 35 reviews**; recurring complaints about waiting times and communication, mixed positives on report quality | https://on-mend.com/providers/profiles/hospitals/vitalray-health-solutions-nairobi-kenya | updated 2026-06-30 | Medium |
| Site maintained: careers page edited 2025-11-28, TLS certificate renewed Aug 2026 (Google Trust Services) | sitemap `lastmod`; `openssl s_client` | 2026-10-22 | High |
| The "Book an appointment" page has **no booking form** — it tells patients to walk in or phone | https://vitalray.com/patients-portal/book-appointment/ | 2026-10-22 | High |
| Contact page has a message form only; no WhatsApp link anywhere on the site | https://vitalray.com/find-us-in-here-westlands-and-upperhill/ | 2026-10-22 | High |
| Broken nav items: "Mayfair Centre" is `href="#"`; "Grenadier Tower" is `tel:GRENADIER TOWER, WESTLANDS` | site markup | 2026-10-22 | High |
| Content stale: blog sitemap last updated **2021-01-05**; most pages 2021 | https://vitalray.com/sitemap_index.xml | 2026-10-22 | High |

## 4. Website verdict: **OK** (live, but not strong)

- HTTPS ✓ (valid cert), mobile viewport ✓, fast (1.1–1.7 s to first byte on repeat fetch), 13/13 checked URLs return 200 or a clean 301.
- Clear contact path ✓ (two branches, phones, email, hours), insurance and billing pages ✓, downloadable forms ✓.
- Weaknesses: no online booking (CTA lands on a "call us" page), dead blog since 2021, broken location links in the header, dated 2015–2021 theme, ~400 px service tiles that cannot be used as hero images.
- No `wa.me` / WhatsApp link anywhere; the numbers are landline + mobile voice lines.

**Net:** they do not need a website. They could use a booking funnel — a different, larger engagement than the pipeline's one-pager.

## 5. Asset shortlist (preview-only, all from their own site)

| # | URL | Type | Resolution | Quality | Tag |
|---|---|---|---|---|---|
| 1 | https://vitalray.com/wp-content/uploads/2019/06/vhslogo.png | logo | 744×300 | clean, transparent-safe, no watermark | logo |
| 2 | https://vitalray.com/wp-content/uploads/2021/01/vitalray_slider1a.jpg | banner | 1900×600 | sharp, wide | hero-worthy |
| 3 | https://vitalray.com/wp-content/uploads/2021/01/vitalray-slider2.jpg | banner | 1900×600 | sharp, wide | hero-worthy |
| 4 | https://vitalray.com/wp-content/uploads/2021/01/vitalray-slider3.jpg | banner | 1900×600 | sharp, wide | hero-worthy |
| 5 | https://vitalray.com/wp-content/uploads/2021/01/vitalray-slider5.jpg | banner | 1900×600 | sharp, wide | hero-worthy |
| 6 | https://vitalray.com/wp-content/uploads/2021/02/radiology-services4.jpg | service tile | 400×400 | too small for hero | product/service |
| 7 | https://vitalray.com/wp-content/uploads/2021/02/laboratory-services4.jpg | service tile | ~400 px | too small | product/service |
| 8 | https://vitalray.com/wp-content/uploads/2021/02/Day-care-services4.jpg | service tile | ~400 px | too small | product/service |

`vitalray-slider4` timed out twice mid-download — **unverified**. No videos found. No team or facility photography is published; no Instagram/TikTok located; the Facebook page (`/VitalRayHealthSolutions`) shows a 2018 post in search results but is not reachable without login.

## 6. Score table (weights: health .25, readiness .20, need .20, pay .15, reach .10, assets .10)

| Factor | Old | New | Why it changed | Source |
|---|---|---|---|---|
| health | 4 | **9** | Two branches, ~37 staff, insurer panels in 2025 and 2026, bank facility 2024, site maintained | panels, Tracxn, PR Times |
| readiness | 5 | **8** | Full site, email, portal pages, billing/insurance info — missing only online booking and WhatsApp | vitalray.com |
| need | 3 | **4** | Real but narrow gap: no booking flow, stale blog, broken nav | booking page, sitemap |
| pay | 7 | **9** | VC-backed, insurance-billed revenue, bank financing — the strongest payer in the folder | AAIC, PR Times |
| reach | 8 | **5** | No WhatsApp; switchboard gatekeeps; CEO identified but no direct channel | site, LinkedIn |
| assets | 3 | **5** | Logo + four 1900×600 banners usable now; nothing current | site |
| **Total** | **48 (C)** | **70 (B)** | | |

Confidence: **high** on health/readiness/need, **medium** on pay (estimates) and reach (no reply test).

## 7. Recommendation: **DROP**

- The core pitch ("no site of yours") is factually wrong; sending it would burn the lead immediately.
- They already have a structured, maintained, multi-page site with insurance-specific content — a one-page template would be a downgrade, and they have in-house ICT staff (a GM of ICT is listed publicly).
- No verified WhatsApp: the recorded "WhatsApp" is switchboard extension 651. A cold call to a diagnostic centre's front desk is a low-yield channel.
- Healthcare marketing is regulated; handmade one-pagers for a Level-4 facility carrying insurer panels is not a credible offer.
- The only honest angle is a **booking / report-request funnel** rebuild at a professional-services price — that is a different pipeline product. If that product exists later, re-open as a new opportunity, not this one.

Not a DQ on inactivity (they are active) — a DQ on **fit**: they already have a working site and a real web owner.

## 8. Open questions

- Which of the two founders (Warriah / Miyengi) actually owns the web budget?
- Was the site built in-house or by an agency still on retainer? (A GM of ICT + Ninja Forms plugin activity in Oct 2026 suggests in-house.)
- Is the Westlands branch still trading? It appears in site copy and PitchBook, but no recent independent mention was found.

## 9. Unverified / could not open

- `facebook.com/VitalRayHealthSolutions` — logged-out fetch blocked; only a 2018 post visible via search index. No current post dates.
- Instagram / TikTok — no handle found for VitalRay; searched by name and location, nothing attributable.
- `vitalray-health-solutions.business.site` — dead (HTTP 404), still cited by on-mend.com as the booking portal.
- Google Maps place page — JS shell, no listing data in HTML; rating/review count taken from on-mend (3.4 / 35).
- `vitalray-slider4.jpg` — download timed out twice; dimensions not confirmed.
- Revenue figure ($9.2 M, datanyze/rocketreach) — third-party estimate, **not** a published number. Not used in scoring.
- No prices are published for any scan or lab test — "not found" after checking radiology, laboratory, billing and insurance pages.
