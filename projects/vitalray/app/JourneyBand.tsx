import Image from "next/image";
import { JOURNEY } from "./site-data";
import Reveal from "./Reveal";

// Journey band — "From walk-in to printed report." Three steps, each with a
// real photo from the client's imaging flow, then a numbered ledger row.
export default function JourneyBand() {
  return (
    <section
      id="journey"
      aria-label="From walk-in to printed report"
      className="w-full bg-paper px-5 py-14 md:px-[50px]"
    >
      <Reveal className="mx-auto flex max-w-[1180px] flex-col gap-4.5">
        <h2
          data-rise
          className="font-display text-[clamp(22px,2.4vw,27px)] font-semibold text-ink"
        >
          From walk-in to printed report
        </h2>
        <div className="grid gap-3 md:grid-cols-3 md:gap-3">
          {JOURNEY.map((j) => (
            <div
              key={j.n}
              data-rise
              className="flex flex-col overflow-hidden rounded-[3px] border border-line bg-paper"
            >
              <div className="relative h-[150px] w-full overflow-hidden bg-deep md:h-[170px]">
                <Image
                  src={j.img}
                  alt={`Step ${j.n} — ${j.title.toLowerCase()}`}
                  fill
                  sizes="(min-width: 768px) 33vw, 100vw"
                  className="object-cover"
                />
              </div>
              <div className="flex flex-col gap-1.5 px-3.5 py-3">
                <div className="flex items-baseline gap-2.5">
                  <span className="font-display text-[20px] font-semibold text-teal">
                    {j.n}
                  </span>
                  <span className="text-[11px] font-bold tracking-[1.2px] text-ink">
                    {j.title}
                  </span>
                </div>
                <p className="text-[11.5px] leading-[1.5] font-semibold text-ink">
                  {j.desc}
                </p>
              </div>
            </div>
          ))}
        </div>
      </Reveal>
    </section>
  );
}
