import Image from "next/image";
import { BUSINESS, LOCATIONS } from "./site-data";
import Reveal from "./Reveal";

// Locations band — the two real sites, each with its own photograph and a
// call + WhatsApp pair. Phone/WhatsApp route the desk, not a form.
export default function LocationsBand() {
  return (
    <section
      id="locations"
      aria-label="Locations"
      className="w-full bg-paper px-5 py-12 md:px-[50px] md:py-[48px]"
    >
      <Reveal className="mx-auto grid max-w-[1180px] gap-3.5 md:grid-cols-2">
        {LOCATIONS.map((l) => (
          <div
            key={l.name}
            data-rise
            className="flex flex-col overflow-hidden rounded-[3px] border border-line bg-paper"
          >
            <div className="relative h-[180px] w-full overflow-hidden bg-deep md:h-[190px]">
              <Image
                src={l.img}
                alt={`VitalRay — ${l.name}, ${l.area}`}
                fill
                sizes="(min-width: 768px) 50vw, 100vw"
                className="object-cover"
              />
            </div>
            <div className="flex flex-col gap-2 px-[18px] py-4">
              <p className="font-display text-[20px] md:text-[22px] font-semibold text-ink">
                {l.name}
              </p>
              <p className="max-w-[600px] text-[13px] leading-[1.5] font-semibold text-ink">
                {l.address}
              </p>
              <div className="flex flex-wrap gap-3.5 pt-1">
                <a
                  href={`tel:${BUSINESS.tel}`}
                  className="block flex-none rounded-[3px] bg-teal px-4 py-[10px] text-[11px] font-bold text-paper transition-colors hover:bg-[#0c5a61]"
                >
                  CALL {BUSINESS.phoneDisplay}
                </a>
                <a
                  href={BUSINESS.waLink}
                  className="block flex-none rounded-[3px] bg-paper px-4 py-[10px] text-[11px] font-bold text-teal ring-1 ring-teal transition-colors hover:bg-glow/30"
                >
                  WHATSAPP THE DESK
                </a>
              </div>
            </div>
          </div>
        ))}
      </Reveal>
    </section>
  );
}
