"use client";

// The cues — three ways to book, as an accordion on tent. Row 01 rides up
// open; toggling re-allocates each row's body with a 200ms slide. The CTA
// opens WhatsApp with the cue's pre-filled ask.
import { useState } from "react";
import { waLink } from "./site-data";
import { THE_CUES } from "./site-data";

export default function CuesSection() {
  const [open, setOpen] = useState(0);

  return (
    <section id="cues" aria-label="Three ways to book" className="bg-tent text-blackout md:px-[56px] md:py-[56px]">
      <div className="flex flex-col justify-between gap-14 md:flex-row md:gap-[56px]">
        {/* left rail */}
        <div className="flex w-full shrink-0 flex-col gap-3.5 px-5 md:w-[380px] md:px-0">
          <p className="font-mono text-[10px] tracking-[1.8px] text-geldeep">
            {THE_CUES.label}
          </p>
          <h2 className="font-display text-[clamp(36px,4.4vw,46px)] font-extrabold leading-[0.95] tracking-[-0.5px]">
            {THE_CUES.title}
          </h2>
          <p className="text-[14px] leading-[1.55] text-inkmute">
            {THE_CUES.body}
          </p>
          <p className="mt-1 border border-geldeep px-[10px] py-[7px] font-mono text-[8px] tracking-[1.3px] text-geldeep">
            {THE_CUES.rateTag}
          </p>
        </div>

        {/* rows */}
        <div className="min-w-0 flex-1 px-5 pb-16 md:px-0 md:pb-0">
          {THE_CUES.rows.map((row, i) => {
            const on = open === i;
            return (
              <div key={row.n} className="border-t border-blackout last:border-b">
                <button
                  type="button"
                  aria-expanded={on}
                  onClick={() => setOpen(on ? -1 : i)}
                  className="flex w-full items-center justify-between gap-4 py-4 text-left"
                >
                  <span className="flex items-baseline gap-4">
                    <span className="font-mono text-[9px] tracking-[1.4px] text-geldeep">
                      {row.n}
                    </span>
                    <span className="font-display text-[28px] font-extrabold leading-none tracking-[0.3px] md:text-[32px]">
                      {row.title}
                    </span>
                  </span>
                  <span
                    className={`text-[16px] leading-none text-blackout transition-transform duration-200 ${
                      on ? "rotate-45" : "rotate-0"
                    }`}
                    aria-hidden
                  >
                    +
                  </span>
                </button>

                <div
                  className={`grid transition-all duration-200 ease-out ${
                    on ? "grid-rows-[1fr] opacity-100" : "grid-rows-[0fr] opacity-0"
                  }`}
                >
                  <div className="overflow-hidden">
                    <div className="flex flex-col gap-3 pb-4">
                      <p className="max-w-[560px] text-[14px] leading-[1.55] text-inkmute">
                        {row.body}
                      </p>
                      <ul className="flex flex-wrap gap-x-6 pt-1">
                        {row.includes.map((inc) => (
                          <li
                            key={inc}
                            className="flex items-center gap-2 border-b border-rule-dark px-1.5 py-1.5 font-mono text-[8.5px] tracking-[1.1px] text-blackout"
                          >
                            <span className="text-geldeep">✓</span>
                            {inc}
                          </li>
                        ))}
                      </ul>
                      <div className="flex flex-wrap items-center gap-2.5 pt-1.5">
                        <a
                          href={waLink(
                            `Hi Mintz Lights — ${row.title
                              .toLowerCase()
                              .replace("+", "and")} — could you quote? `
                          )}
                          className="flex items-center gap-2 bg-blackout px-4 py-3 font-mono text-[9px] tracking-[1.4px] text-tent hover:bg-geldeep"
                        >
                          {THE_CUES.cta} →
                        </a>
                        <p className="font-mono text-[8px] tracking-[1.2px] text-inkmute">
                          {THE_CUES.ctaNote}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
