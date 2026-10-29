import type { Metadata } from "next";
import { Fraunces, Public_Sans, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";
import { BUSINESS, LOCATIONS } from "./site-data";

const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
  weight: ["400", "600"],
  display: "swap",
});

const publicSans = Public_Sans({
  variable: "--font-public",
  subsets: ["latin"],
  display: "swap",
});

const plexMono = IBM_Plex_Mono({
  variable: "--font-plex",
  subsets: ["latin"],
  weight: ["400", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "VitalRay — Outpatient hospital, radiology & laboratory, Nairobi",
  description:
    "VitalRay Health Solutions — outpatient hospital in Nairobi (Upper Hill + Westlands). Radiology (MR, CT, X-ray, ultrasound), laboratory and day care. Colour scans, positive prints and reports your doctor can read.",
  openGraph: {
    title: "VitalRay — Your body, in sharp focus",
    description:
      "Fast, friendly service and accurate medical reports — colour and 3D scans explained in plain language, printed for your doctor. Two sites: Upper Hill + Westlands, Nairobi.",
    type: "website",
    siteName: BUSINESS.name,
  },
};

// Real facts only — both addresses, real phones, real hours as published on
// vitalray.com (contacts page).
function localBusinessJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    name: BUSINESS.name,
    description: BUSINESS.description,
    telephone: BUSINESS.tel,
    email: BUSINESS.email,
    url: "https://vitalray.com",
    location: LOCATIONS.map((l) => ({
      "@type": "Place",
      name: `${l.name}, ${l.area}`,
      address: {
        "@type": "PostalAddress",
        streetAddress: l.address,
        addressLocality: "Nairobi",
        addressCountry: "KE",
      },
    })),
    openingHoursSpecification: [
      {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        opens: "07:00",
        closes: "20:00",
      },
      {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: "Saturday",
        opens: "08:00",
        closes: "18:00",
      },
    ],
  };
}

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${fraunces.variable} ${publicSans.variable} ${plexMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <a href="#main" className="skip-link">
          SKIP TO CONTENT →
        </a>
        {children}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(localBusinessJsonLd()) }}
        />
      </body>
    </html>
  );
}
