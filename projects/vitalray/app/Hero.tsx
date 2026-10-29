import Image from "next/image";
import { BUSINESS, HERO } from "./site-data";

// Hero — "YOUR BODY, IN SHARP FOCUS." Copy column on paper; on the right the
// patient-report viewer: the client's real CT scan in a deep frame with mono
// annotations, exactly as burned on the lead-pipeline canvas.
export default function Hero() {
  return (
    <section
      id="top"
      aria-label="VitalRay outpatient hospital"
      className="w-full bg-paper px-5 pt-24 pb-14 md:grid md:grid-cols-2 md:items-start md:gap-[34px] md:px-[50px] md:pt-[120px] md:pb-14"
    >
      <div className="flex flex-col gap-4 md:gap-4">
        <p className="font-mono text-[10px] tracking-[1.4px] text-teal">
          {HERO.eyebrow}
        </p>
        <h1 className="max-w-[560px] font-display text-[clamp(40px,4.4vw,62px)] leading-[1.05] font-semibold whitespace-pre-line text-ink">
          {HERO.headline}
        </h1>
        <p className="max-w-[540px] text-[15px] leading-[1.55] text-ink md:text-[15.5px]">
          {HERO.sub}
        </p>
        <div className="flex flex-wrap items-center gap-3.5 pt-1">
          <a
            href={BUSINESS.portal.book}
            className="block flex-none rounded-[3px] bg-teal px-6 py-[13px] text-[13px] font-bold text-paper transition-colors hover:bg-[#0c5a61]"
          >
            BOOK AN APPOINTMENT →
          </a>
          <a
            href={BUSINESS.portal.insurance}
            className="text-[12.5px] font-semibold text-teal hover:underline"
          >
            insurance patients welcome ↗
          </a>
        </div>

        {/* three-fact strip */}
        <div className="mt-6 flex max-w-[560px] flex-col gap-4 rounded-[3px] border border-line px-4 py-3 sm:flex-row sm:justify-between md:mt-2">
          {HERO.stats.map((s) => (
            <div key={s.t} className="flex w-full flex-col gap-0.5 sm:w-[170px]">
              <p className="font-display text-[20px] font-semibold text-teal">
                {s.t}
              </p>
              <p className="text-[9.5px] leading-[1.35] text-ink">{s.s}</p>
            </div>
          ))}
        </div>
      </div>

      {/* the viewer */}
      <div className="relative mt-10 h-[320px] w-full overflow-hidden rounded-[3px] bg-deep md:mt-0 md:h-[520px] md:w-full">
        <Image
          src={HERO.viewerImg}
          alt="CT imaging at VitalRay Health Solutions"
          fill
          sizes="(min-width: 768px) 40vw, 100vw"
          className="object-cover opacity-90 [transform:scale(0.98)]"
        />
        <p className="absolute left-3 top-3 font-mono text-[9px] text-glow md:left-[44px] md:top-[44px] md:text-[10px]">
          {HERO.viewerAnn1}
        </p>
        <span className="absolute right-3 top-3 rounded-[2px] bg-glow px-2.5 py-[7px] font-mono text-[8.5px] font-bold text-deep md:right-[44px] md:text-[9.5px]">
          {HERO.viewerTag}
        </span>
        <p className="absolute bottom-3 left-3 font-mono text-[8.5px] text-glow md:bottom-[26px] md:left-[44px] md:text-[9px]">
          {HERO.viewerAnn2}
        </p>
      </div>
    </section>
  );
}
