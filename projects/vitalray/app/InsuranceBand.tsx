import { INSURERS } from "./site-data";
import Reveal from "./Reveal";

// Insurance band — the real partner list on ink. Small mono chips, tight.
export default function InsuranceBand() {
  return (
    <section
      aria-label="Insurance partners"
      className="w-full bg-ink px-5 py-9 md:px-[50px] md:py-[36px]"
    >
      <Reveal className="mx-auto flex max-w-[1180px] flex-col gap-3">
        <h2
          data-rise
          className="font-display text-[clamp(18px,1.9vw,22px)] font-semibold text-paper"
        >
          insurers you already carry
        </h2>
        <ul className="flex flex-wrap gap-2">
          {INSURERS.map((name) => (
            <li
              key={name}
              data-rise
              className="rounded-[2px] border border-glow/60 bg-deep px-3 py-2 font-mono text-[9px] text-glow"
            >
              {name}
            </li>
          ))}
        </ul>
      </Reveal>
    </section>
  );
}
