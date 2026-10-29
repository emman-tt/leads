# Canaan Medical Centre (lead #921) — verification report
Audit date: 2026-10-22 (v2 — deeper pass) · Folder: data/briefs/921
Country: Kenya · City: Nairobi — CBD, Corner House, Mama Ngina Street

> **Headline:** real, insurer-contracted outpatient clinic that **used to have a website
> and no longer does**. `canaanhealthproviders.org` carried a "Canaan Health Providers"
> site from 2017 to at least 2021, then decayed into a redirect, and is **now unregistered**.
> The email printed on their own insurer panel therefore bounces. Genuine "no site" lead —
> the opposite of Vital Ray.

## 1. Lead Digest (as claimed)

| Field | Claimed value |
|---|---|
| Business | Canaan Medical Centre |
| Category | pharmacies |
| City / country | *null* / Kenya |
| Claimed website | `https://www.googletagmanager.com/gtag/js?id=G-Z6HX57VF8P` |
| Phone | +254203341896 |
| WhatsApp | +254711702224 |
| Email | info@canaanhealthproviders.org |
| Address | *none* |
| Assets | 0 images, 0 videos, hero-worthy 0 |
| Score / tier | 48 / 100, tier C |
| Factors | health 4 · readiness 5 · need 3 ("site ~functional") · pay 7 · reach 8 · assets 3 |
| Why-pitch | "strongest selling point: Pay and Health" |
| Outreach claims | "**Accra** pharmacies listing", "nothing behind it to browse or book — and **no site of yours**", "**MoMo** payments", "I have **already put together a free preview mockup** based on your own photos" |

## 2. Data-quality flags

1. **Website is a tracking script** — the kenyayp gtag bug (`G-Z6HX57VF8P`), same as every Kenyan lead.
2. **"WhatsApp" is the phone copied over.** `+254711702224` is a published mobile, plausibly on WhatsApp, but nothing verified it.
3. **Category wrong** — recorded `pharmacies`; it is a family-practice / outpatient clinic.
4. **Draft says Accra.** The clinic is in Nairobi CBD.
5. **Email is dead** — domain unregistered (see §4). Mail to it cannot be delivered.
6. **"site ~functional"** — there is no site at all; `need` 3/10 is inverted.
7. **Fabricated preview** — 0 assets, yet the draft claims a mockup built from "your own photos".
8. **MoMo in Kenya** — the clinic bills insurers; nothing suggests mobile-money-first.
9. **"Pay and Health"** named as the strongest selling point while health is 4/10 "unverified active".
10. **Geography blank** — city, address and coordinates null, so the summary headline prints "?".
11. **Duplicate listing already exists in the wild** — Go Africa Online carries the same clinic twice (1113448 "medical clinics", 1105226 "general practitioners"), so dedupe matters if this source is scanned again.

## 3. Verified findings

| Finding | Source | Date seen | Confidence |
|---|---|---|---|
| Clinic exists: outpatient / family practice, Corner House 1st Floor, Mama Ngina Street, Nairobi CBD | Yellow Pages Kenya 989569; africabizinfo; businesslist 38982 | 2026-10-22 | High |
| Phones: mobile **0711 702224**; landlines **341896 / 341903 / 2230697**; extra line 020 4445985; fax 020 4448770 | **Minet 2025 panel row, verbatim**; UAP Old Mutual panel; africabizinfo | 2024–2025 | High |
| Address and email as published by the clinic: "Corner Hse, 1st Floor, Mama Ngina Street … info@canaanhealthproviders.org", service type Outpatient, region Nairobi-CBD | Minet 2025 provider panel PDF (text extracted from the file itself) | 2025 | High |
| On UAP Old Mutual's health provider panel: "CANAAN MEDICAL CENTRE — Nairobi CBD — Corner Hse 1st, Floor — +254 711-702224 /20 2230697" | https://kengensrbs.co.ke/wp-content/uploads/2024/03/2.UAP_OM-Health-Provider-Panel.pdf | 2024-03 | High |
| On the Teachers Medical Scheme provider list (Nairobi-CBD, Direct) | https://collaborationkenya.minet.com/MinetKe/Teachersmedicalscheme/files/2023_07_14_01_11_14pm_ServiceProvidersList.pdf | 2023-07 | High |
| Postal: P.O. Box 48981-00100 GPO, Nairobi; listed since **4 Oct 2011** | https://www.businesslist.co.ke/company/38982/canaan-medical-centre | 2011 listing, read 2026 | Medium |
| Hours: Mon–Fri 08:00–17:00, Sat 08:00–12:00, Sun closed; wheelchair accessible, restroom | https://www.africabizinfo.com/KE/canaan-medical-centre_25-020-341896 ; goafricaonline 1113448 | 2026-10-22 | Medium |
| **Former website**: "CANAAN HEALTH PROVIDERS — we listen we care!" with nav Home / About us / News & Event / Products / Services / Portfolio / Links / Contact Us / Support. Captured 2017-05 → 2021-11 | https://web.archive.org/web/20180104141656/http://canaanhealthproviders.org/ and timemap | snapshots 2017–2021 | High |
| That site was a **vendor template that was never filled in** — pages render only the nav and the tagline, no services, no staff, no phone, no email | Archived HTML of the 2018 snapshot | 2018 snapshot | High |
| By **20 Feb 2025** the domain answered with a **302 redirect to `https://www.facebook.com/`** — no content of its own | Wayback replay headers (`x-archive-orig-location`) | 2025-02-20 | High |
| **Now unregistered**: NXDOMAIN at the .org TLD; RDAP 404 — free to register today | https://dns.google/resolve?name=canaanhealthproviders.org&type=A ; https://rdap.org/domain/canaanhealthproviders.org | 2026-10-22 | High |
| No live site under any name variant (`canaanhealthproviders.com`, `canaanmedicalcentre.co.ke/.com`, `canaanmedicalcenter.co.ke`) | DNS, all NXDOMAIN | 2026-10-22 | High |
| No Facebook, Instagram, TikTok or LinkedIn page found under the clinic's name, address or phone | Exact-name, address and phone searches; FB/IG/TikTok not reachable logged-out | 2026-10-22 | Medium |
| Reviews: 4 on KEOnline; 0 on BusinessList; 0 on Go Africa Online (two listings); "be the first" on Yellow Pages Kenya | Directory pages read directly | 2026-10-22 | Medium |
| No named doctor, director or owner published anywhere — panels list the facility, not a contact person | All of the above | 2026-10-22 | — (not found) |

**Beware a same-name trap:** the Teachers scheme list also contains a **"Canaan Medical Clinic" in Turkana South (Lokichar)** — a different facility. Only the Nairobi-CBD "Canaan Medical Centre" row belongs to this lead.

## 4. Website verdict: **NONE** (lapsed — it used to exist)

- **2017 – 2021:** a site lived at `canaanhealthproviders.org` under the name "Canaan Health Providers", tagline "we listen we care!". It was a cheap vendor template: the archived pages contain only the navigation and the tagline — no services, no staff names, no phone, no email, no photos.
- **2025-02-20:** the domain returned `302 → https://www.facebook.com/` (the root, not a page). Nothing of their own was served.
- **2026-10-22:** the domain is **not in the registry** — NXDOMAIN at .org, RDAP 404. It is registrable today.
- No replacement site exists under any name variant, and no social page was found.
- Practical effect: the email on their Minet panel and their Yellow Pages listing bounces, and a patient searching the clinic's name gets directory stubs only.

This is a cleaner pitch than "you have no website": they *tried* a site, it decayed, and the domain lapsed. That is a concrete, checkable story.

## 5. Asset shortlist (preview-only)

| # | URL | Type | Resolution | Quality | Tag |
|---|---|---|---|---|---|
| — | none | — | — | — | — |

**Zero assets — verified.** No live site, no socials, no logo file, no photographs. The only surviving visual is the 2017 template's text wordmark ("CANAAN HEALTH PROVIDERS"). Any design starts from scratch or from photos the clinic sends.

## 6. Score table (weights: health .25, readiness .20, need .20, pay .15, reach .10, assets .10)

| Factor | Old | New | Why it changed | Source |
|---|---|---|---|---|
| health | 4 | **6** | Real and continuously contracted: Teachers scheme 2023, UAP Old Mutual 2024, Minet 2025; listed since 2011. Capped at 6 by only 4 reviews and no social activity | three panel PDFs |
| readiness | 5 | **2** | No site, no socials, no working email — phone lines only. (The pipeline formula returns 5 purely because `whatsapp` is set, and that field is a copy of `phone`) | DNS + searches |
| need | 3 | **10** | Lapsed branded domain, dead email, template site abandoned mid-build, nothing behind the name | RDAP 404 |
| pay | 7 | **7** | Bills three insurer panels, so revenue is institutional; but a single-branch CBD clinic with no published size | panels |
| reach | 8 | **6** | Mobile + three landlines published consistently; no named person; WhatsApp unverified | Minet/UAP panels |
| assets | 3 | **1** | Nothing exists to reuse | verified |
| **Total** | **48 (C)** | **57 (B)** | | |

Confidence: **high** on website/need and on contacts, **medium** on health (2025 panel is the newest proof), **low** on pay.

## 7. Recommendation: **PURSUE** (tier B, 57)

Passes the hard filters: no site, working mobile channel, private clinic, no franchise/NGO. Score is held down by `readiness` and `assets` — exactly what the product fixes.

Caveats before outreach:
- **Medical vertical.** Keep claims to facts: location, hours, insurer panels, how to book. No health claims, and no "patients can't find you" — they are on three panels and every directory.
- **No named decision-maker.** Address the clinic; ask in the first reply who handles enquiries.
- **Design note:** the VITALRAY "patient-report / scan-viewer" medical archetype is burned in the design ledger — use a different direction (walk-in / insurance-card clarity, corner-building wayfinding), not a diagnostics dashboard.
- **Low ticket risk.** Small single-branch clinic; price accordingly.

## 8. Open questions

- Is 0711 702224 on WhatsApp? (Untested — do not assert.)
- Still trading in 2026? Newest independent proof is the 2025 Minet panel.
- Did they abandon the domain deliberately, or did a former web vendor let it go? That changes the pitch from "you need a site" to "your old one is gone".
- Who is the proprietor/medical officer? Nothing public; the first reply should ask.

## 9. Unverified / could not open

- Google Maps place page — JS shell, no listing data in HTML; the "4 reviews" figure comes from a KEOnline mirror, undated.
- Facebook / Instagram / TikTok — no account found by name, address or phone; **not found**, not proven absent. Facebook and Instagram are not readable logged-out.
- The identity behind the Feb-2025 `facebook.com` redirect — Wayback captured only the 302 and a 47-byte body; the forwarding target was the Facebook root, so no page can be inferred.
- Internet Archive's CDX index was intermittently offline (503) during this pass, so the full file list of the old site is incomplete; the 2018 and 2021 homepage snapshots were retrieved, inner pages largely were not.
- WhatsApp status of 0711 702224 — cannot be confirmed without contacting. Nothing was sent.
