// VITALRAY HEALTH SOLUTIONS — single source of truth. Every value below is
// real, fetched from vitalray.com (home, contacts and radiology pages) or
// verbatim from the client's own testimonials. Nothing invented: no ratings,
// no bios, no stock faces. Phone numbers exactly as the client lists them.

export const BUSINESS = {
  name: "VitalRay Health Solutions",
  brandShort: "VITALRAY",
  description:
    "Outpatient hospital in Nairobi — fast, friendly service and accurate medical reports.",
  // working hours from vitalray.com contacts page (verbatim)
  hours: "MON–FRI 7.00AM–8.00PM · SAT 8.00AM–6.00PM",
  phones: [
    { label: "Office", display: "+254 (20) 2731 650/1", tel: "+254202731650" },
    { label: "Mobile", display: "+254 737 556 119", tel: "+254737556119" },
    { label: "Mobile", display: "+254 705 120 400", tel: "+254705120400" },
  ],
  phoneDisplay: "+254 737 556119",
  tel: "+254737556119",
  email: "info@vitalray.com",
  waLink: "https://wa.me/254737556119",
  portal: {
    book: "https://vitalray.com/patients-portal/book-appointment/",
    reports: "https://vitalray.com/patients-portal/view-medical-reports/",
    billing: "https://vitalray.com/patients-portal/billing-information/",
    insurance: "https://vitalray.com/patients-portal/insurance-information/",
  },
  site: "vitalray.com",
} as const;

export const LOCATIONS = [
  {
    name: "MAYFAIR CENTRE",
    area: "UPPER HILL",
    address:
      "Ground Floor, Mayfair Centre, Ralph Bunche Road — Upper Hill, Nairobi",
    // real vitalray.com photography (their own uploads, hotlinked in the demo)
    img: "https://vitalray.com/wp-content/uploads/2021/01/vitalray-slider3.jpg",
  },
  {
    name: "GRENADIER TOWER",
    area: "WESTLANDS",
    address:
      "Ground Floor, Grenadier Tower, Woodvale Grove — Westlands, Nairobi",
    img: "https://vitalray.com/wp-content/uploads/2021/01/vitalray-slider2.jpg",
  },
] as const;

// The four service desks, descriptions drawn from the client's own service
// pages. Card photos are vitalray.com uploads (their CMS file names kept —
// odd where the client's CMS is odd, they are still the real photos).
export const SERVICES = [
  {
    code: "RADIOLOGY",
    title: "Radiology",
    desc: "MR, CT, X-ray and ultrasound — colour scans and positive prints your specialist can actually explain from.",
    url: "https://vitalray.com/radiology-mri-ctscan-xray-ultrasound/",
    img: "https://vitalray.com/wp-content/uploads/2021/02/radiology-services4.jpg",
    big: true,
  },
  {
    code: "LABORATORY",
    title: "Laboratory",
    desc: "Clinical labs on-site; results join your report without a second visit.",
    url: "https://vitalray.com/laboratory/",
    img: "https://vitalray.com/wp-content/uploads/2021/02/laboratory-services4.jpg",
    big: false,
  },
  {
    code: "DAY CARE",
    title: "Day care",
    desc: "Day procedures and monitoring with a seat that goes home the same evening.",
    url: "https://vitalray.com/day-care/",
    img: "https://vitalray.com/wp-content/uploads/2021/02/oncology-service4.jpg",
    big: true,
  },
  {
    code: "OTHER SERVICES",
    title: "Other services",
    desc: "Consults, monitoring and support services around imaging.",
    url: "https://vitalray.com/other-services/",
    img: "https://vitalray.com/wp-content/uploads/2021/02/Day-care-services4.jpg",
    big: false,
  },
] as const;

// Journey steps: real photography from the client's radiology booking flow.
export const JOURNEY = [
  {
    n: "01",
    title: "BOOK OR WALK IN",
    desc: "Call, book online, or WhatsApp — both sites take evening slots, so work doesn't swallow the appointment.",
    img: "https://vitalray.com/wp-content/uploads/2021/01/vitalray-slider4.jpg",
  },
  {
    n: "02",
    title: "SCAN + LAB",
    desc: "Radiology and laboratory on one floor; colour scans and 3D where the question needs them.",
    img: "https://vitalray.com/wp-content/uploads/2021/01/ULTRASOUND-VITALRAY-HEALTH.jpg",
  },
  {
    n: "03",
    title: "REPORT + PRINTS",
    desc: "Accurate reports — plus prints you bring home to the family or the specialist.",
    img: "https://vitalray.com/wp-content/uploads/2021/01/MRI-VITALRAY-HEALTH.jpg",
  },
] as const;

// Insurance partners, exactly the client's partner list (vitalray.com →
// Insurance Companies), trimmed to the short names the design uses.
export const INSURERS = [
  "APA",
  "OLD MUTUAL",
  "JUBILEE",
  "MINET AON",
  "SHA",
  "CIC GENERAL",
  "SANLAM",
  "HERITAGE",
  "TAKAFUL",
  "SEDGWICK",
  "PACIS",
  "GA",
  "MADISON",
  "FIRST ASSURANCE",
  "AFRICA MEDILINK",
  "HENNER GMC",
] as const;

// Testimonials — named, verbatim (lightly shortened to fit the band; the
// client's own words, no edits to meaning). Source: vitalray.com home page.
export const TESTIMONIALS = [
  {
    quote:
      "With VitalRay for 6 years — their evening hours keep the patient out of a second sick-day, colour scans interpret easily, and they are the only centre giving positive prints: useful when I explain pathology to the patient.",
    name: "Prof. J.A.O Mulimba — Consultant Orthopaedic and Trauma Surgeon",
  },
  {
    quote:
      "When we send patients to VitalRay the feedback is very positive: friendly reception, highly professional procedures, and costs easy on the pocket. The centre is impressively clean.",
    name: "Dr. Lorraine Maveke",
  },
  {
    quote:
      "I referred my first patient in 2014 — probably the best 3D images and best reports I have ever received.",
    name: "Dr. Eric Kahugu",
  },
] as const;

// Hero — headline and sub copy from the pen design (founded on the client's
// home welcome paragraph). Imaging photo is the client's real CT upload.
export const HERO = {
  eyebrow: "OUTPATIENT HOSPITAL · RADIOLOGY · LABORATORY · DAY CARE",
  headline: "YOUR BODY,\nIN SHARP\nFOCUS.",
  sub: "Fast, friendly service and accurate medical reports — colour and 3D scans explained in plain language, printed for your doctor.",
  viewerImg:
    "https://vitalray.com/wp-content/uploads/2021/01/CT-SCAN-VITALRAY-HEALTH.jpg",
  viewerAnn1: "CT · ULTRASOUND · 3D IMAGING",
  viewerTag: "COLOUR & 3D SCANS ON PREMISES",
  viewerAnn2: "UPPER HILL + WESTLANDS · WALK-INS WELCOME",
  stats: [
    {
      t: "PRINTS",
      s: "positive prints your specialist can actually explain from — referral doctors swear by them",
    },
    {
      t: "EVENING",
      s: "hours that keep working people off sick-days",
    },
    {
      t: "2 SITES",
      s: "Upper Hill + Westlands, walk-ins welcome",
    },
  ],
} as const;
