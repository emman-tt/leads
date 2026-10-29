import { TAGLINE } from "./site-data";

// Tagline band — the client's own strapline set big, in stencil, on the
// gel-fill control color. One band, no photo.
export default function TaglineBand() {
  return (
    <section
      aria-label={TAGLINE.line}
      className="w-full bg-gelfill px-5 py-10 md:px-[56px] md:py-[38px]"
    >
      <p className="font-mono text-[8.5px] tracking-[1.6px] text-tent">
        {TAGLINE.micro}
      </p>
      <p className="mt-1 font-stencil text-[clamp(52px,8vw,88px)] font-extrabold leading-[0.9] tracking-[-1px] text-tent">
        {TAGLINE.line}
      </p>
      <p className="mt-1 font-mono text-[9px] tracking-[1.6px] text-tent">
        {TAGLINE.place}
      </p>
    </section>
  );
}
