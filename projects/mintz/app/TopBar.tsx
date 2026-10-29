import Link from "next/link";
import { BUSINESS } from "./site-data";

const NAV = [
  { label: "THE CUES", href: "/#cues" },
  { label: "THE RIG", href: "/#rig" },
  { label: "JOB LOG", href: "/#joblog" },
  { label: "THE DESK", href: "/#desk" },
] as const;

// Topbar — wordmark, the address as wayfinding, four mono links, and the
// WhatsApp pill that carries the number the client actually answers.
export default function TopBar({ activePlan = false }: { activePlan?: boolean }) {
  return (
    <header className="sticky top-0 z-50 flex h-[58px] w-full flex-none items-center justify-between border-b border-rule-light bg-blackout px-4 md:h-[72px] md:px-[56px]">
      <div className="flex items-center gap-3.5">
        <p className="font-display text-[17px] leading-none font-bold tracking-[2px] text-tent md:text-[22px]">
          {BUSINESS.name}
        </p>
        <span className="hidden h-4 w-px bg-rule-chip md:block" aria-hidden />
        <p className="hidden font-mono text-[9.5px] tracking-[1.4px] text-haze md:block">
          {BUSINESS.area}
        </p>
      </div>

      <nav className="hidden items-center gap-[26px] lg:flex" aria-label="Site">
        {NAV.map(({ label, href }) => (
          <a
            key={label}
            href={href}
            className="font-mono text-[10px] tracking-[1.4px] text-tent hover:text-gelhi"
          >
            {label}
          </a>
        ))}
        <Link
          href="/quote"
          className={`font-mono text-[10px] tracking-[1.4px] hover:text-gelhi ${
            activePlan ? "text-gelhi" : "text-tent"
          }`}
        >
          PLAN A BUILD
        </Link>
      </nav>

      <a
        href={BUSINESS.whatsapp ? `https://wa.me/${BUSINESS.waNumber}` : "#"}
        className="flex flex-none items-center gap-[7px] rounded-none bg-gelfill px-3 py-[9px] font-mono text-[10px] tracking-[1px] text-tent transition-colors hover:bg-gel md:px-[14px]"
        aria-label={`WhatsApp Mintz Lights — ${BUSINESS.whatsapp}`}
      >
        <WhatsAppGlyph className="h-3 w-3" />
        <span className="hidden sm:inline">{BUSINESS.whatsapp}</span>
        <span className="sm:hidden">0757…836</span>
      </a>
    </header>
  );
}

export function WhatsAppGlyph({ className = "h-3 w-3" }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" className={className} fill="currentColor" aria-hidden>
      <path d="M12 2.4A9.6 9.6 0 0 0 3.6 16.4L2.4 21.6l5.3-1.2A9.6 9.6 0 1 0 12 2.4Zm0 17.3a7.7 7.7 0 0 1-3.9-1.07l-.28-.16-3.1.7.7-3-.18-.3A7.7 7.7 0 1 1 12 19.7Zm4.36-5.66c-.24-.12-1.4-.69-1.62-.77-.22-.08-.38-.12-.54.12-.16.24-.62.77-.76.93-.14.16-.28.18-.52.06a6.34 6.34 0 0 1-1.86-1.15 6.9 6.9 0 0 1-1.28-1.6c-.14-.24-.02-.37.1-.49.11-.11.24-.28.36-.42.12-.14.16-.24.24-.4.08-.16.04-.3-.02-.42-.06-.12-.54-1.3-.74-1.78-.2-.47-.4-.4-.54-.41h-.46c-.16 0-.42.06-.64.3-.22.24-.84.82-.84 2 0 1.18.86 2.32.98 2.48.12.16 1.7 2.6 4.12 3.64.58.25 1.03.4 1.38.51.58.19 1.1.16 1.52.1.46-.07 1.4-.57 1.6-1.13.2-.54.2-1.01.14-1.11-.06-.1-.22-.16-.46-.28Z" />
    </svg>
  );
}
