"use client";

// Hero — the cue console. Three lines of the business (LIGHT / DRESS /
// MOVE) sit as chips; one is live at a time and whatever is live re-rigs
// the stage plot on the right over 480ms: beam angle, gel temperature,
// floor pool. The stage is drawn entirely in CSS gradients — the client
// had zero hero-ready photographs, so light is the hero.
import { useState } from "react";
import Link from "next/link";
import { gsap } from "gsap";
import { CUES, HERO, HERO_FOOT, type CueKey } from "./site-data";

export default function Hero() {
  const [live, setLive] = useState<CueKey>("LIGHT");
  const cue = CUES.find((c) => c.key === live)!;

  // 480ms re-rig: beam angle + gel temperature + the floor pool color.
  const reRig = (key: CueKey) => {
    if (key === live) return;
    setLive(key);
    const next = CUES.find((c) => c.key === key)!;
    const plot = document.documentElement;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      plot.style.setProperty("--beam-angle", next.angle);
      plot.style.setProperty("--beam-wash", next.wash);
      plot.style.setProperty("--beam-pool", next.pool);
      return;
    }
    gsap.to(plot, {
      duration: 0.48,
      ease: "power2.inOut",
      "--beam-angle": next.angle,
      onComplete: () => {
        plot.style.setProperty("--beam-wash", next.wash);
        plot.style.setProperty("--beam-pool", next.pool);
      },
    });
  };

  return (
    <section
      id="top"
      aria-label="Mintz Lights — event lighting, décor and truck hire"
      className="pt-0 md:px-[56px]"
    >
      <div className="px-5 pb-[26px] pt-7 md:px-0 md:pt-[34px]">
        <p className="font-mono text-[10px] tracking-[1.8px] text-gelhi">
          {HERO.cueTag}
        </p>
        <p className="mt-1 font-mono text-[10px] tracking-[1.8px] text-haze">
          {HERO.servicesLine}
        </p>
      </div>

      <div className="flex flex-col gap-7 md:flex-row md:gap-[28px]">
        <div className="flex flex-col gap-[22px] px-5 md:w-[58%] md:px-0">
          {/* H1 — Big Shoulders with the stencil “gobo” word */}
          <div className="flex flex-col gap-0.5">
            {CUES.map((c) => (
              <p key={c.key} className="flex items-end leading-[0.84]">
                <span className="font-display text-[clamp(56px,8vw,88px)] font-extrabold tracking-[-2px] text-tent">
                  WE&nbsp;
                </span>
                <span
                  className={`font-stencil text-[clamp(56px,8vw,88px)] font-extrabold tracking-[-1.2px] ${
                    live === c.key ? "text-gel" : "text-gel/45"
                  }`}
                >
                  {c.key}
                </span>
                <span className="font-display text-[clamp(56px,8vw,88px)] font-extrabold tracking-[-1.2px] text-tent">
                  &nbsp;IT.
                </span>
              </p>
            ))}
          </div>

          <p className="max-w-[520px] text-[16px] leading-[1.55] text-haze md:text-[17px]">
            {HERO.proposition}
          </p>

          {/* cue console */}
          <div className="flex gap-[8px]" role="group" aria-label="What to build first">
            {CUES.map((c) => {
              const on = live === c.key;
              return (
                <button
                  key={c.key}
                  type="button"
                  aria-pressed={on}
                  onClick={() => reRig(c.key)}
                  className={`flex flex-col gap-[5px] px-3 py-[11px] text-left transition-colors duration-200 md:w-[150px] ${
                    on
                      ? "flex-1 bg-gelfill md:flex-none md:w-[186px]"
                      : "border border-rule-chip bg-struck hover:border-gelhi/60"
                  } ${c.key === "LIGHT" ? "md:w-[186px] md:flex-1" : ""}`}
                >
                  <span
                    className={`font-mono text-[9px] whitespace-nowrap tracking-[1.4px] ${
                      on ? "text-tent" : "text-peri"
                    }`}
                  >
                    {c.num}
                  </span>
                  <span
                    className={`text-[12px] leading-[1.2] ${
                      on ? "text-tent" : "text-haze"
                    }`}
                  >
                    {c.sub}
                  </span>
                  {on && (
                    <span className="flex items-center gap-1.5 pt-[7px]">
                      <span className="font-mono text-[8px] tracking-[1.4px] text-tent/70">
                        CUE LIVE
                      </span>
                      <span
                        className="h-[7px] w-[7px] animate-pulse bg-tent"
                        aria-hidden
                      />
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* includes row — what this cue carries */}
          <div className="flex flex-col" aria-live="polite">
            <p className="sr-only">Included in this cue</p>
            <div className="grid grid-cols-3 gap-[8px]">
              {cue.includes.map((inc) => (
                <p
                  key={inc}
                  className="border border-rule-light bg-struck/60 px-2 py-[7px] font-mono text-[7.5px] tracking-[1px] text-tent md:text-[8px]"
                >
                  {inc.toUpperCase()}
                </p>
              ))}
            </div>
          </div>

          {/* CTA row */}
          <div className="flex flex-wrap items-center gap-3 pt-1.5">
            <Link
              href="/quote"
              className="flex flex-none items-center gap-2.5 bg-tent px-[18px] py-4 font-mono text-[11px] tracking-[1.5px] text-blackout transition-colors hover:bg-gelhi"
            >
              {HERO.primary} →
            </Link>
            <a
              href="#joblog"
              className="flex flex-none items-center gap-2 border border-rule-chip px-[18px] py-[15px] font-mono text-[10.5px] tracking-[1.4px] text-tent hover:border-gelhi"
            >
              {HERO.secondary}
            </a>
            <p className="font-mono text-[9px] tracking-[1.2px] text-haze">
              {HERO.micro}
            </p>
          </div>
        </div>

        {/* stage plot — CSS-only rig room */}
        <div className="px-5 md:w-[42%] md:px-0">
          <div
            className="stage-plot relative h-[340px] w-full overflow-hidden border border-rule-light bg-struck md:h-[596px]"
            aria-label={`Stage plot — ${cue.sub}`}
            role="img"
          >
            {/* ground gradient into blackout */}
            <div
              className="absolute inset-0"
              style={{
                background: "linear-gradient(180deg, #1C1C29 0%, #0B0B12 100%)",
              }}
            />
            {/* truss */}
            <div className="absolute inset-x-0 top-[54px] h-[3px] bg-tent/12" />
            <div className="absolute left-1/2 top-[50px] flex -translate-x-1/2 gap-[46px]">
              {[0, 1, 2, 3, 4].map((i) => (
                <span key={i} className="h-[6px] w-px bg-tent/16" aria-hidden />
              ))}
            </div>
            {/* lamp */}
            <div className="absolute left-[38%] top-[62px]">
              <span className="block h-[3px] w-5 bg-tent/24" aria-hidden />
              <span className="absolute left-1/2 top-[3px] h-[8px] w-[60px] -translate-x-1/2 rounded-[1px] bg-tent" aria-hidden />
              <span
                className="absolute -top-1 left-1/2 h-[54px] w-[124px] -translate-x-1/2"
                aria-hidden
                style={{
                  background:
                    "radial-gradient(64px 30px at 50% 0%, rgba(242,239,233,0.8) 0%, rgba(230,23,95,0) 100%)",
                }}
              />
            </div>
            {/* beam cone + floor pool + haze */}
            <div className="beam-cone" aria-hidden />
            <div
              className="absolute inset-x-0 bottom-0 h-[196px]"
              aria-hidden
              style={{
                background:
                  "linear-gradient(180deg, rgba(138,140,232,0) 0%, rgba(230,23,95,0.1) 70%, rgba(230,23,95,0) 100%)",
              }}
            />
            <div className="floor-pool absolute inset-0" aria-hidden />
            {/* hazy ambient drift (24s, reduced-motion killed) */}
            <div
              className="absolute inset-0 opacity-40 mix-blend-screen"
              aria-hidden
              style={{
                background:
                  "radial-gradient(120px 60px at 30% 80%, rgba(138,140,232,0.08), transparent 70%), radial-gradient(160px 60px at 72% 60%, rgba(230,23,95,0.07), transparent 70%)",
                backgroundSize: "200% 200%",
                animation: "haze-drift 24s ease-in-out infinite",
              }}
            />
            {/* floor line */}
            <div className="absolute inset-x-0 bottom-[52px] h-px bg-tent/12" aria-hidden />

            {/* captions */}
            <div className="absolute left-3 top-3 flex items-center justify-between">
              <p className="font-mono text-[9px] tracking-[1.4px] text-haze">
                RIG A / RIDGEWAYS
              </p>
            </div>
            <div className="absolute inset-x-5 bottom-[86px] hidden items-center justify-center md:flex">
              <p className="border border-dashed border-tent/20 px-4 py-2 font-mono text-[9px] tracking-[1.4px] text-peri">
                [ YOUR VENUE PHOTO GOES HERE ]
              </p>
            </div>
            <p className="absolute bottom-[74px] left-4 font-mono text-[8.5px] tracking-[1.2px] text-haze transition-opacity duration-300">
              {cue.gelNote}
            </p>
            <p className="absolute bottom-[46px] left-4 font-mono text-[8px] tracking-[1.3px] text-haze/80">
              THE ROOM IS YOURS. WE JUST SET THE LIGHT.
            </p>
          </div>
        </div>
      </div>

      {/* fact strip */}
      <div className="mt-7 flex flex-wrap gap-x-6 gap-y-1.5 border-t border-rule-light px-5 pb-[26px] pt-[28px] md:px-0">
        {HERO_FOOT.map((f) => (
          <p key={f.key} className="flex items-baseline gap-3">
            <span className="font-mono text-[9px] tracking-[1.6px] text-peri">
              {f.key}
            </span>
            <span className="font-mono text-[9.5px] tracking-[1.1px] text-haze">
              {f.val}
            </span>
          </p>
        ))}
      </div>
    </section>
  );
}
