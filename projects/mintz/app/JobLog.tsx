import { JOB_LOG } from "./site-data";
import Reveal from "./Reveal";

// Job log — five real dated rows from the client's own posts, set as a
// ledger. Hover/focus lands an honest empty PHOTO SLOT frame: their feed
// photos are login-walled, so the emptiness is the ask.
export default function JobLog() {
  return (
    <section id="joblog" aria-label="Recently rigged" className="bg-tent px-5 py-16 text-blackout md:px-[56px]">
      <Reveal>
        <header className="flex flex-wrap items-end justify-between gap-4 pb-[34px]">
          <div className="flex flex-col gap-2">
            <p className="font-mono text-[10px] tracking-[1.8px] text-geldeep">03 / JOB LOG</p>
            <h2 className="font-display text-[clamp(36px,4.4vw,46px)] font-extrabold leading-[0.95] tracking-[-0.5px]">
              RECENTLY RIGGED
            </h2>
          </div>
          <div className="flex flex-col items-start gap-1.5 pb-1">
            <p className="font-mono text-[9.5px] tracking-[1.4px] text-inkmute">
              {JOB_LOG.head.range}
            </p>
            <p className="font-mono text-[9px] tracking-[1.4px] text-inkmute">
              {JOB_LOG.head.places}
            </p>
          </div>
        </header>

        {/* table head */}
        <div className="hidden border-b border-blackout pb-[9px] md:grid md:grid-cols-[112px_330px_1fr_132px]">
          {JOB_LOG.columns.map((c) => (
            <p key={c} className="font-mono text-[8.5px] tracking-[1.6px] text-inkmute">
              {c}
            </p>
          ))}
        </div>

        {/* rows */}
        {JOB_LOG.rows.map((row) => (
          <div
            key={row.date}
            tabIndex={0}
            className="group flex flex-col gap-2 border-b border-rule-dark py-[18px] md:grid md:grid-cols-[112px_330px_1fr_132px] md:items-start"
          >
            <p className="font-mono text-[10px] tracking-[1.2px] text-inkmute">
              {row.date}
            </p>
            <p className="font-display text-[26px] font-extrabold leading-none tracking-[0.2px] md:text-[30px]">
              {row.where}
            </p>
            <p className="text-[14px] leading-[1.4] text-inkmute">{row.what}</p>

            <div className="flex items-center justify-between md:justify-start">
              <span className="flex items-center gap-1.5 border border-rule-mid px-[9px] py-[5px] whitespace-nowrap">
                <span className="h-[5px] w-[5px] bg-geldeep" aria-hidden />
                <span className="font-mono text-[8px] tracking-[1.3px]">
                  {row.status}
                </span>
              </span>
              {/* the photo slot — lands on hover/focus (desktop) */}
              <span
                aria-hidden
                className="hidden border border-dashed border-blackout/30 font-mono text-[7px] tracking-[1.4px] text-inkmute/0 transition-opacity duration-200 group-hover:text-inkmute/70 group-focus-visible:text-inkmute/70 md:flex md:h-16 md:w-16 md:items-center md:justify-center md:bg-blackout/[0.015] md:mix-blend-normal"
              >
                {""}
              </span>
            </div>
          </div>
        ))}

        <footer className="flex flex-wrap items-center gap-3 pt-[22px]">
          <p className="bg-geldeep px-[10px] py-1.5 font-mono text-[8px] tracking-[1.4px] text-tent">
            {JOB_LOG.noteTag}
          </p>
          <p className="max-w-[680px] text-[13px] leading-[1.4] text-inkmute">
            {JOB_LOG.note}
          </p>
        </footer>
      </Reveal>
    </section>
  );
}
