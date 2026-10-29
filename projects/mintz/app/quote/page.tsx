import TopBar from "../TopBar";
import SmoothScroll from "../SmoothScroll";
import Footer from "../Footer";
import WhatsAppSticky from "../WhatsAppSticky";
import QuoteSheet from "../QuoteSheet";
import { waLink } from "../site-data";

// Quote sheet — a tier-B inner page. The form writes the message; the
// send opens WhatsApp with it written, editable before sending.
export const metadata = {
  title: "Plan a build — Mintz Lights",
  description:
    "Tell Mintz Lights what you are planning, where, when, how many, and one photo of the space. The reply is a rate for that room — not a brochure. WhatsApp +254 757 924 836.",
};

export default function QuotePage() {
  return (
    <>
      <SmoothScroll />
      <main id="main" className="relative">
        <TopBar activePlan />
        <QuoteSheet />
        <div className="border-t border-rule-light bg-blackout px-5 py-5 md:px-[56px]">
          <a
            href={waLink("Hi Mintz Lights — I am planning an event and I would like a quote.")}
            className="font-mono text-[10px] tracking-[1.4px] text-peri hover:text-gelhi"
          >
            OR JUST MESSAGE THE DESK DIRECTLY →
          </a>
        </div>
        <Footer />
      </main>
      <WhatsAppSticky />
    </>
  );
}
