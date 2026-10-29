import { BUSINESS, HERO } from "./site-data";

// Footer — stencil mark, the three verified links, the legal line.
export default function Footer() {
  return (
    <footer className="flex flex-col gap-[26px] border-t border-rule-light bg-blackout px-5 pb-[26px] pt-[40px] md:px-[56px]">
      <div className="flex flex-wrap items-center justify-between gap-6">
        <p className="font-stencil text-[clamp(28px,3vw,40px)] font-extrabold leading-none tracking-[1px] text-tent">
          {BUSINESS.name}
        </p>
        <div className="flex gap-[22px]">
          <a
            href={BUSINESS.facebook}
            className="font-mono text-[8.5px] tracking-[1.4px] text-haze hover:text-gelhi"
          >
            FACEBOOK
          </a>
          <a
            href={`https://wa.me/${BUSINESS.waNumber}`}
            className="font-mono text-[8.5px] tracking-[1.4px] text-haze hover:text-gelhi"
          >
            WHATSAPP
          </a>
          <a
            href={`mailto:${BUSINESS.email}`}
            className="font-mono text-[8.5px] tracking-[1.4px] text-haze hover:text-gelhi"
          >
            EMAIL
          </a>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="font-mono text-[8px] tracking-[1.3px] text-haze">
          © 2026 {BUSINESS.name} · 46 KIGWA ROAD, RIDGEWAYS, NAIROBI
        </p>
        <p className="font-mono text-[8px] tracking-[1.3px] text-peri">
          {HERO.servicesLine}
        </p>
      </div>
    </footer>
  );
}
