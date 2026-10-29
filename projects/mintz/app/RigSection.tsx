import Image from "next/image";
import { RIG } from "./site-data";

// The rig — four bare columns of what the business carries, separated by
// vertical rules. The DRESS column carries the one verified photograph
// (the client's own page avatar) as evidence, at the size it can bear.
export default function RigSection() {
  return (
    <section id="rig" className="py-16">
      <header className="flex flex-wrap items-end justify-between gap-4 px-5 pb-[30px] md:px-[56px]">
        <div className="flex flex-col gap-2">
          <p className="font-mono text-[10px] tracking-[1.8px] text-gelhi">02 / THE RIG</p>
          <h2 className="font-display text-[clamp(36px,4.4vw,46px)] font-extrabold leading-[0.95] tracking-[-0.5px] text-tent">
            WHAT WE BRING
          </h2>
        </div>
        <p className="flex items-center gap-2.5 pb-1.5 font-mono text-[9px] tracking-[1.4px] text-haze">
          FOUR LINES, ONE CREW ·{" "}
          <span className="text-peri lg:hidden">SWIPE</span>
          <span className="text-peri hidden lg:inline">DRAG</span>
        </p>
      </header>

      <div
        className="overflow-x-auto border-y border-rule-light scroll-smooth md:overflow-visible"
        role="group"
        aria-label="The rig columns"
      >
        <div className="grid min-w-[720px] grid-cols-4 md:min-w-0">
          <RigColumn col={RIG[0]} pad />
          <RigColumn col={RIG[1]} pad photo />
          <RigColumn col={RIG[2]} pad />
          <RigColumn col={RIG[3]} />
        </div>
      </div>
    </section>
  );
}

type RigCol = (typeof RIG)[number];

function RigColumn({
  col,
  pad = false,
  photo = false,
}: {
  col: RigCol;
  pad?: boolean;
  photo?: boolean;
}) {
  const numColor = col.accent === "gelhi" ? "text-gelhi" : "text-peri";
  return (
    <div
      className={`flex min-h-[348px] flex-col gap-2.5 border-b border-rule-light md:min-w-0 md:border-b-0 ${
        pad ? "border-r border-rule-light px-5 pt-5 pb-1 md:px-5 md:pt-5" : "px-5 pt-5 pb-1"
      }`}
    >
      <p className={`font-mono text-[9px] tracking-[1.6px] ${numColor}`}>{col.col}</p>
      {photo && (
        <figure className="w-[132px]">
          <Image
            src="https://graph.facebook.com/1473399672955768/picture?type=large"
            alt="Mintz Lights — white marquee tent with periwinkle and magenta drapes and gold chairs, from the client's own page"
            width={200}
            height={200}
            unoptimized
            className="h-[132px] w-[132px] object-cover ring-1 ring-rule-chip"
          />
          <figcaption className="pt-1 font-mono text-[7.5px] tracking-[1px] text-haze">
            {"photoCaption" in col ? col.photoCaption : ""}
          </figcaption>
        </figure>
      )}
      <h3 className="font-display text-[30px] font-extrabold leading-[0.95] tracking-[0.3px] text-tent">
        {col.title}
      </h3>
      <p className="text-[13px] leading-[1.5] text-haze">{col.body}</p>

      {"list" in col && col.list && (
        <ul className="flex flex-col pt-1.5">
          {col.list.map((item) => (
            <li
              key={item}
              className="flex items-center justify-between border-b border-rule-light py-[7px]"
            >
              <span className="font-mono text-[8.5px] tracking-[1.1px] text-tent">
                {item}
              </span>
              <span className={numColor}>✓</span>
            </li>
          ))}
        </ul>
      )}

      {"ledger" in col && col.ledger && (
        <div className="flex gap-[18px] pt-1.5">
          {col.ledger.map((group) => (
            <ul key={group[0]} className="flex flex-1 flex-col">
              {group.map((item) => (
                <li key={item} className="border-b border-rule-light py-1.5">
                  <span className="font-mono text-[8.5px] tracking-[1.1px] text-tent">
                    {item}
                  </span>
                </li>
              ))}
            </ul>
          ))}
        </div>
      )}

      {"timeline" in col && col.timeline && (
        <ul className="flex flex-col pt-1.5">
          {col.timeline.map(([k, v]) => (
            <li
              key={k}
              className="flex items-center justify-between border-b border-rule-light py-1.5"
            >
              <span className="font-mono text-[8.5px] tracking-[1.1px] text-peri">
                {k}
              </span>
              <span className="font-mono text-[8.5px] tracking-[1.1px] text-tent">
                {v}
              </span>
            </li>
          ))}
        </ul>
      )}

      <p className="mt-auto pt-2 font-mono text-[8.5px] tracking-[1.1px] text-peri">
        {col.foot}
      </p>
    </div>
  );
}
