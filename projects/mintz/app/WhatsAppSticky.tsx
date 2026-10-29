import { waLink } from "./site-data";
import { WhatsAppGlyph } from "./TopBar";

// Static mobile dock — a 44px+ tap target that never goes away on phones.
export default function WhatsAppSticky() {
  return (
    <a
      href={waLink("Hi Mintz Lights — I am planning an event and I would like a quote.")}
      aria-label="WhatsApp Mintz Lights on +254 757 924 836"
      className="fixed bottom-4 right-4 z-50 flex h-13 w-13 items-center justify-center rounded-full bg-gelfill shadow-[0_8px_30px_rgba(0,0,0,0.55)] md:hidden"
    >
      <WhatsAppGlyph className="h-6 w-6" />
    </a>
  );
}
