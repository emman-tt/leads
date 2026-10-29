import Link from "next/link";
import { BUSINESS, LOCATIONS } from "./site-data";

// Topbar — brand pin + the two site names as its wayfinding, book button.
// Stays a server component.
export default function TopBar() {
  return (
    <header className="absolute inset-x-0 top-0 z-50 flex h-20 w-full flex-none items-center justify-between border-b border-line bg-paper px-5 md:h-16 md:px-[50px]">
      <Link href="/" className="flex items-center gap-2.5" aria-label={`${BUSINESS.name} — home`}>
        <span className="h-[26px] w-[14px] bg-teal" aria-hidden />
        <span className="font-display text-[17px] font-semibold text-ink md:text-[22px]">
          {BUSINESS.brandShort}
        </span>
      </Link>

      <span className="hidden flex-col items-start gap-0.5 font-mono text-[9.5px] leading-[1.5] text-teal lg:flex">
        <span>{LOCATIONS[0].name} · {LOCATIONS[0].area}</span>
        <span>{LOCATIONS[1].name} · {LOCATIONS[1].area}</span>
      </span>

      <a
        href={BUSINESS.portal.book}
        className="block flex-none rounded-[3px] bg-teal px-3 py-2 text-[10px] font-bold text-paper transition-colors hover:bg-[#0c5a61] md:px-[18px] md:py-[10px] md:text-[11px]"
      >
        BOOK AN APPOINTMENT
      </a>
    </header>
  );
}
