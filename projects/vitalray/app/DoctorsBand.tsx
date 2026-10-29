import { TESTIMONIALS } from "./site-data";
import Reveal from "./Reveal";

// Doctors band — named testimonials on deep. Quote cards sit on ink with a
// glow hairline, set in Fraunces. Quotes verbatim from the client's record.
export default function DoctorsBand() {
  return (
    <section
      id="doctors"
      aria-label="What the doctors who refer say"
      className="w-full bg-deep px-5 py-14 md:px-[50px] md:py-[54px]"
    >
      <Reveal className="mx-auto flex max-w-[1180px] flex-col gap-4.5 md:gap-[18px]">
        <h2
          data-rise
          className="font-display text-[clamp(22px,2.4vw,27px)] font-semibold text-paper"
        >
          What the doctors who refer say
        </h2>
        <p
          data-rise
          className="font-mono text-[9.5px] text-glow"
        >
          named testimonials from vitalray.com — verbatim, no edits
        </p>
        <div className="flex flex-col gap-3.5">
          {TESTIMONIALS.map((t) => (
            <figure
              key={t.name}
              data-rise
              className="flex max-w-[1080px] flex-col gap-2 rounded-[3px] border border-glow/70 bg-ink px-5 py-4.5 md:px-5 md:py-[18px]"
            >
              <blockquote className="font-display text-[16px] leading-[1.42] text-paper md:text-[20px]">
                “{t.quote}”
              </blockquote>
              <figcaption className="text-[10.5px] font-bold text-glow">
                {t.name}
              </figcaption>
            </figure>
          ))}
        </div>
      </Reveal>
    </section>
  );
}
