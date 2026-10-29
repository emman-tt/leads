import Image from "next/image";
import { SERVICES } from "./site-data";

// Services — "Four desks, one waiting room." Asymmetric register: Radiology
// and Day care hold the tall slots, Laboratory and Other services sit lower
// — all four photos are the client's own uploads.
export default function ServicesGrid() {
  const [radiology, laboratory, dayCare, other] = SERVICES;
  return (
    <section
      id="services"
      aria-label="Services"
      className="w-full bg-paper px-5 py-14 md:px-[50px] md:py-[52px]"
    >
      <div className="mx-auto flex max-w-[1180px] flex-col gap-4">
        <h2 className="font-display text-[clamp(22px,2.4vw,27px)] font-semibold text-ink">
          Four desks, one waiting room.
        </h2>
        <div className="grid gap-3.5 md:grid-cols-2">
          {/* left column: tall cards */}
          <div className="flex flex-col gap-3.5">
            <ServiceCard s={radiology} imgH="h-[220px] md:h-[300px]" tall />
            <ServiceCard s={other} imgH="h-[170px] md:h-[210px]" />
          </div>
          {/* right column */}
          <div className="flex flex-col gap-3.5">
            <ServiceCard s={laboratory} imgH="h-[170px] md:h-[210px]" />
            <ServiceCard s={dayCare} imgH="h-[220px] md:h-[300px]" tall />
          </div>
        </div>
      </div>
    </section>
  );
}

function ServiceCard({
  s,
  imgH,
  tall = false,
}: {
  s: (typeof SERVICES)[number];
  imgH: string;
  tall?: boolean;
}) {
  return (
    <a
      href={s.url}
      className="group flex flex-col overflow-hidden rounded-[3px] border border-line bg-paper transition-colors hover:border-teal/60"
    >
      <div className={`relative w-full overflow-hidden bg-deep ${imgH}`}>
        <Image
          src={s.img}
          alt={`${s.title} at VitalRay`}
          fill
          sizes="(min-width: 768px) 50vw, 100vw"
          className={`object-cover transition-transform duration-500 group-hover:scale-[1.02] ${
            tall ? "" : "opacity-95"
          }`}
        />
      </div>
      <div className="flex flex-col gap-1.5 px-4 py-3.5 md:px-4 md:py-3.5">
        <p className={`font-display font-semibold text-ink ${tall ? "text-[19px] md:text-[22px]" : "text-[17px] md:text-[18px]"}`}>
          {s.title}
        </p>
        <p className="text-[12px] leading-[1.5] font-semibold text-ink">
          {s.desc}
        </p>
      </div>
    </a>
  );
}
