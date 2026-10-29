import type { Metadata } from "next";
import {
  Big_Shoulders,
  Big_Shoulders_Stencil,
  Hanken_Grotesk,
  Spline_Sans_Mono,
} from "next/font/google";
import "./globals.css";
import { BUSINESS } from "./site-data";

const shoulders = Big_Shoulders({
  variable: "--font-shoulders",
  subsets: ["latin"],
  weight: ["500", "700", "800"],
  display: "swap",
});

const stencil = Big_Shoulders_Stencil({
  variable: "--font-stencil",
  subsets: ["latin"],
  weight: ["800"],
  display: "swap",
});

const hanken = Hanken_Grotesk({
  variable: "--font-hanken",
  subsets: ["latin"],
  display: "swap",
});

const splineMono = Spline_Sans_Mono({
  variable: "--font-spline",
  subsets: ["latin"],
  weight: ["400", "700"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Mintz Lights — Event lighting, décor & truck hire, Nairobi",
  description:
    "Mintz Lights, Ridgeways, Nairobi — event lighting design & install, décor and rustic furniture hire, and the trucks that carry it. Weddings, ruracios, birthdays, corporate. WhatsApp +254 757 924 836.",
  openGraph: {
    title: "Mintz Lights — We light it. We dress it. We move it.",
    description:
      "Event lighting, décor and rustic furniture hire out of Ridgeways, Nairobi — plus the trucks that get it to the venue. One crew: lighting, dressing, moving.",
    type: "website",
    siteName: "Mintz Lights",
  },
};

// Real facts only — verified in data/briefs/992/research.md (client's own
// social posts + directories). Kitchen-table details the client publishes:
// address, hours, payments, the two phone lines.
function localBusinessJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    name: "Mintz Lights",
    description:
      "Event lighting, décor and rustic furniture hire, plus truck hire — Nairobi.",
    telephone: "+254757924836",
    email: BUSINESS.email,
    url: "https://facebook.com/mintzlights",
    address: {
      "@type": "PostalAddress",
      streetAddress: "46 Kigwa Road, Ridgeways",
      addressLocality: "Nairobi",
      addressCountry: "KE",
    },
    openingHoursSpecification: [
      {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday"],
        opens: "08:00",
        closes: "17:00",
      },
      {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: "Friday",
        opens: "08:00",
        closes: "18:00",
      },
      {
        "@type": "OpeningHoursSpecification",
        dayOfWeek: "Saturday",
        opens: "08:00",
        closes: "13:00",
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
      className={`${shoulders.variable} ${stencil.variable} ${hanken.variable} ${splineMono.variable} h-full antialiased`}
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
