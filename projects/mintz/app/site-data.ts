// MINTZ LIGHTS — single source of truth. Every value is real client
// material verified on 2026-10-22 in data/briefs/992/research.md
// (EvePla/Facebook mirror of page id 1473399672955768 + YP Kenya +
// apexbusinesspages) and carried verbatim onto the lead-pipeline.pen
// MINTZ artboards. Nothing invented: no photos beyond the verified
// 200×200 page avatar, no ratings, no bios, no stock faces.

export const BUSINESS = {
  name: "MINTZ LIGHTS",
  tagline: "styled accordingly.",
  area: "RIDGEWAYS, NAIROBI",
  address: "46 Kigwa Road, Ridgeways, Nairobi",
  hours: {
    hero: "MON–FRI 08:00–17:00 · SAT 08:00–13:00",
    quote: "MON–FRI 08:00–17:00 · FRI TO 18:00 · SAT 08:00–13:00",
  },
  whatsapp: "+254 757 924 836",
  waNumber: "254757924836",
  office: "+254 729 854 408",
  email: "mintzlights@gmail.com",
  facebook: "https://facebook.com/mintzlights",
  payments: ["M-PESA", "CASH", "CHEQUE"],
  // The one verified photograph: the business page's own avatar
  // (white marquee tent, periwinkle and magenta drapes, gold chairs,
  // lawn). 200×200 — used as evidence at the size it can bear.
  avatar:
    "https://graph.facebook.com/1473399672955768/picture?type=large",
} as const;

export function waLink(text: string): string {
  return `https://wa.me/${BUSINESS.waNumber}?text=${encodeURIComponent(text)}`;
}

export const WA_DEFAULT =
  "Hi Mintz Lights — I am planning an event and I would like a quote.";

export const HERO = {
  cueTag: "CUE 01 / HOUSE TO HALF",
  servicesLine: "LIGHTING · DÉCOR & STYLING · FURNITURE · TRUCK HIRE",
  proposition:
    "Event lighting, décor and rustic furniture hire out of Ridgeways — plus the trucks that get it to the venue, however far. Weddings, ruracios, birthdays, corporate.",
  micro: "M-PESA · CASH · CHEQUE",
  secondary: "SEE THE JOB LOG",
  primary: "PLAN A BUILD",
} as const;

// The cue console — the signature interaction. Three lines of the
// business, each once live at a time; whatever is live re-rigs the
// stage plot (beam angle, gel temperature) and the WhatsApp message.
export type CueKey = "LIGHT" | "DRESS" | "MOVE";

export const CUES: {
  key: CueKey;
  num: string;
  sub: string;
  angle: string;
  wash: string;
  pool: string;
  gelNote: string;
  includes: string[];
  message: string;
}[] = [
  {
    key: "LIGHT",
    num: "01 / LIGHT",
    sub: "Design + install",
    angle: "45deg",
    wash: "#E6175F",
    pool: "#E6175F",
    gelNote: "GEL 108 · 2 × LED · 45°",
    includes: ["Wedding & ruracio lighting", "Corporate stage & launch", "Dance floor, drapes, uplighting"],
    message:
      "Hi Mintz Lights — I am planning an event and I need lighting only. Could you quote?",
  },
  {
    key: "DRESS",
    num: "02 / DRESS",
    sub: "Décor, rustic, tents",
    angle: "58deg",
    wash: "#8A8CE8",
    pool: "#8A8CE8",
    gelNote: "DRAPE WASH · PERIWINKLE",
    includes: ["Luxury & rustic styling", "Crate tables & director chairs", "Tents, seating, carpets"],
    message:
      "Hi Mintz Lights — I am planning an event and I need décor and furniture. Could you quote?",
  },
  {
    key: "MOVE",
    num: "03 / MOVE",
    sub: "Trucks + load-out",
    angle: "32deg",
    wash: "#F2EFE9",
    pool: "#F2EFE9",
    gelNote: "HOT LIGHT · OPEN WHITE",
    includes: ["Truck with crew", "Same-night load-out", "Garissa & beyond runs"],
    message:
      "Hi Mintz Lights — I need trucks and load-out for an event. Could you quote?",
  },
] as const;

// Hero fact strip (published hours; the road; the WhatsApp line).
export const HERO_FOOT = [
  { key: "OPEN", val: BUSINESS.hours.hero },
  { key: "ROAD", val: "46 KIGWA ROAD, RIDGEWAYS" },
  { key: "SAY HI", val: `WHATSAPP ${BUSINESS.whatsapp}` },
] as const;

// The rig — four lines of the business (real service range).
export const RIG = [
  {
    col: "01 / LIGHT",
    accent: "gelhi" as const,
    title: "LIGHT DESIGN & INSTALL",
    body: "Gels, gobo cuts, dimming and a rig hung with time to focus it — not an hour before guests.",
    list: ["WEDDINGS & RURACIOS", "CORPORATE & LAUNCHES", "STAGE, DANCE FLOOR, DRAPES"],
    foot: "ASK FOR THE LIGHTING CUES →",
  },
  {
    col: "02 / DRESS",
    accent: "peri" as const,
    title: "DÉCOR & STYLING",
    body: "Luxury, rustic or country — drapes, centrepieces and a room that reads as one idea.",
    photoCaption: "FROM YOUR PAGE · 200PX · PREVIEW",
    foot: "EVORIA SPA FIT-OUT · NGARA",
  },
  {
    col: "03 / HIRE",
    accent: "peri" as const,
    title: "FURNITURE & TENTS",
    ledger: [
      ["CRATE TABLES", "DIRECTOR CHAIRS", "HAY BALES"],
      ["SEATING", "CARPETS", "TENTS"],
    ],
    body: "Priced by the item and the day. Delivered, set, and collected by our own crew.",
    foot: "BY ITEM · BY DAY",
  },
  {
    col: "04 / MOVE",
    accent: "peri" as const,
    title: "TRUCKS & LOAD-OUT",
    body: "Truck hire with or without crew. We have run gear to Garissa and back to Ridgeways inside one week.",
    timeline: [
      ["LOAD-IN", "CREW + TRUCK"],
      ["LOAD-OUT", "SAME NIGHT"],
      ["GARISSA RUN", "SEP 2026"],
    ],
    foot: "ASK FOR A TRUCK",
  },
] as const;

// Job log — five real dated rows (the client's public posts,
// 23 Sep – 1 Oct 2026). Photo slots stay open on purpose: their feed
// photos are login-walled.
export const JOB_LOG = {
  head: { range: "SEP – OCT 2026", places: "NAIROBI · GARISSA" },
  columns: ["DATE", "WHERE", "WHAT", "STATUS"],
  rows: [
    { date: "23 SEP", where: "GARISSA", what: "Load-out and the long run home", status: "LOAD-OUT" },
    { date: "25 SEP", where: "NAIROBI", what: "Event build, start to last chair", status: "BUILT" },
    { date: "28 SEP", where: "EVORIA SPA, NGARA", what: "Styling fit-out, Adyen Plaza", status: "FITTING" },
    { date: "30 SEP", where: "NAIROBI", what: "Lighting rig, hung and focused", status: "BUILT" },
    { date: "01 OCT", where: "RIDGEWAYS", what: "Trucks opened for hire", status: "HIRE" },
  ],
  noteTag: "PHOTO SLOTS OPEN",
  note: "Five frames from your September albums turn this log into the gallery. Send them on WhatsApp and we will place them.",
} as const;

// The cues — three ways to book (accordion).
export const THE_CUES = {
  label: "04 / THE CUES",
  title: "THREE WAYS TO BOOK",
  body: "Every event is quoted per room, per date. Send the venue and the guest count — we come back with a number, not a brochure.",
  rateTag: "RATE ON REQUEST · M-PESA DEPOSIT",
  rows: [
    {
      n: "01",
      title: "LIGHTING ONLY",
      body: "A rig designed for the room, hung and focused with the venue empty. Gels and gobos cut to your colours.",
      includes: ["Wedding & ruracio lighting", "Corporate stage & launch", "Dance floor, drapes, uplighting"],
    },
    {
      n: "02",
      title: "STYLING + HIRE",
      body: "Décor and rustic furniture from our own yard — crate tables, director chairs, hay bales, tents, seating and carpets.",
      includes: ["Rustic furniture & drapes", "Tents, seating, carpets", "Delivered, set, collected"],
    },
    {
      n: "03",
      title: "FULL PRODUCTION",
      body: "Lighting plus décor plus trucks — one crew carrying the build from load-in to the last chair packed away.",
      includes: ["One crew, whole build", "Trucks + load-out included", "From Ridgeways to Garissa"],
    },
  ],
  cta: "ASK FOR A QUOTE",
  ctaNote: "Replies Mon–Fri, 08:00–17:00",
} as const;

export const TAGLINE = {
  micro: "WEDDINGS · RURACIOS · CORPORATE · BIRTHDAYS",
  line: "STYLED ACCORDINGLY.",
  place: "RIDGEWAYS / NAIROBI",
} as const;

// The desk — the yard, its hours and how to reach it.
export const DESK = {
  label: "05 / THE DESK",
  title: "COME TO KIGWA ROAD",
  address: "46 Kigwa Road, Ridgeways, Nairobi",
  note: "Visits by arrangement — the truck is usually out on a build. WhatsApp first and we will tell you when the yard is open.",
  hours: [
    { day: "MON – THU", val: "08:00 – 17:00" },
    { day: "FRIDAY", val: "08:00 – 18:00" },
    { day: "SATURDAY", val: "08:00 – 13:00" },
    { day: "SUNDAY", val: "CLOSED" },
  ],
  contacts: [
    { k: "WHATSAPP", v: BUSINESS.whatsapp },
    { k: "OFFICE", v: BUSINESS.office },
    { k: "EMAIL", v: BUSINESS.email },
  ],
  pin: {
    label: "THE YARD",
    copy: "Off Kigwa Road, Ridgeways. We send the exact pin on WhatsApp before a visit — the truck is often out.",
  },
  card: {
    label: "SEND THIS ON WHATSAPP",
    body: "Hi Mintz Lights — I am planning a ruracio on 14 Feb at a home in Karen, about 180 guests. We need lighting and rustic furniture. Could you quote?",
    meta: [
      { k: "REPLACE", v: "DATE · VENUE · GUESTS" },
      { k: "ATTACH", v: "ONE PHOTO OF THE ROOM" },
      { k: "DEPOSIT", v: "M-PESA, ON CONFIRMATION" },
    ],
    cta: "OPEN WHATSAPP",
  },
} as const;

// Job-log hover slots / quote drop zones are honest empty frames.
export const SLOT = "PHOTO SLOT";

// Quote sheet (tier-B inner page) — the form that writes the WhatsApp
// message. Field placeholders come from the design; nothing is submitted
// anywhere but WhatsApp.
export const QUOTE = {
  kicker: "QUOTE SHEET / 01",
  h1a: "TELL US THE",
  h1b: "ROOM.",
  body: "One message: what you are planning, where, when, how many, and one photo of the space. We reply with a rate for that room — not a brochure.",
  meta1: "SHEET 01 — QUOTE REQUEST",
  meta2: "REPLIES MON–FRI 08:00–17:00",
  rows: [
    { n: "01", label: "WHAT ARE WE DOING?", note: "PICK ANY — MOST BUILDS ARE TWO OR THREE" },
    { n: "02", label: "WHERE?", note: "HOME, HOTEL, CHURCH, HALL — AND THE AREA" },
    { n: "03", label: "WHEN?", note: "DATE AND CALL TIME, EVEN IF IT IS NEXT YEAR" },
    { n: "04", label: "HOW MANY GUESTS?", note: "A RANGE IS FINE" },
    { n: "05", label: "SHOW US THE ROOM", note: "ONE PHOTO IS ENOUGH — DAYLIGHT IF YOU HAVE IT" },
  ],
  chips: ["LIGHT", "DRESS", "FURNITURE", "TRUCK"],
  drop: "DROP A PHOTO OF THE SPACE — JPG / HEIC · UP TO 5MB",
  prevLabel: "YOUR MESSAGE, AS IT STANDS",
  prevNote: "Opens WhatsApp with the message written. You can edit it before sending.",
  sendCta: "SEND ON WHATSAPP",
  things: {
    label: "BEFORE YOU SEND",
    title: "FIVE THINGS, THEN WE QUOTE",
    items: [
      "WHAT YOU ARE PLANNING",
      "THE VENUE AND AREA",
      "DATE AND CALL TIME",
      "GUEST COUNT",
      "ONE PHOTO OF THE ROOM",
    ],
    deskLabel: "THE DESK",
  },
} as const;
