import { DESK, waLink } from "./site-data";
import { WhatsAppGlyph } from "./TopBar";
import Reveal from "./Reveal";

// The desk — the yard on Kigwa Road: hours, payments, the three real
// contact lines, and the WhatsApp card that writes your first message.
export default function Desk() {
  return (
    <section id="desk" aria-label="The desk" className="bg-blackout px-5 py-16 md:px-[56px]">
      <Reveal className="flex flex-col gap-[52px] lg:flex-row">
        {/* left column */}
        <div className="flex min-w-0 flex-1 flex-col gap-4">
          <p className="font-mono text-[10px] tracking-[1.8px] text-gelhi">
            {DESK.label}
          </p>
          <h2 className="font-display text-[clamp(36px,4.4vw,46px)] font-extrabold leading-[0.95] tracking-[-0.5px] text-tent">
            {DESK.title}
          </h2>
          <p className="text-[20px] leading-[1.4] text-tent">{DESK.address}</p>
          <p className="max-w-[520px] text-[14px] leading-[1.55] text-haze">
            {DESK.note}
          </p>

          {/* hours ledger */}
          <ul className="max-w-[480px] pt-2">
            {DESK.hours.map((h) => (
              <li
                key={h.day}
                className="flex items-center justify-between border-b border-rule-light py-[7px]"
              >
                <span className="font-mono text-[9px] tracking-[1.3px] text-peri">
                  {h.day}
                </span>
                <span className="font-mono text-[9.5px] tracking-[1.2px] text-tent">
                  {h.val}
                </span>
              </li>
            ))}
          </ul>

          {/* payments */}
          <div className="flex flex-wrap gap-2 pt-2.5">
            {["M-PESA", "CASH", "CHEQUE"].map((p) => (
              <span
                key={p}
                className="border border-rule-chip px-[10px] py-1.5 font-mono text-[8px] tracking-[1.3px] text-tent"
              >
                {p}
              </span>
            ))}
          </div>

          {/* contacts */}
          <div className="flex flex-wrap gap-9 pt-2.5">
            {DESK.contacts.map((c) => (
              <p key={c.k} className="flex flex-col gap-0.5">
                <span className="font-mono text-[8px] tracking-[1.4px] text-peri">
                  {c.k}
                </span>
                <span className="font-mono text-[9.5px] tracking-[0.8px] text-tent">
                  {c.v}
                </span>
              </p>
            ))}
          </div>

          {/* pin block */}
          <div className="flex items-start gap-4 pt-4">
            <span className="flex h-[104px] w-[150px] flex-none items-center justify-center border border-rule-lighter" aria-hidden>
              <svg viewBox="0 0 24 24" className="h-[18px] w-[18px] text-peri" fill="currentColor">
                <path d="M12 2a7 7 0 0 0-7 7c0 4.4 4.9 9.6 6.5 11.2a1 1 0 0 0 1 0C14.1 18.6 19 13.4 19 9a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z" />
              </svg>
            </span>
            <div className="flex max-w-[280px] flex-col gap-1.5">
              <p className="font-mono text-[8px] tracking-[1.4px] text-peri">
                {DESK.pin.label}
              </p>
              <p className="text-[12px] leading-[1.45] text-haze">
                {DESK.pin.copy}
              </p>
            </div>
          </div>
        </div>

        {/* WhatsApp card */}
        <aside className="w-full flex-none bg-tent p-6 text-blackout lg:w-[452px]">
          <p className="font-mono text-[9px] tracking-[1.6px] text-geldeep">
            {DESK.card.label}
          </p>
          <p className="pt-3.5 text-[17px] leading-[1.6]">
            {DESK.card.body}
          </p>
          <div className="pt-3">
            {DESK.card.meta.map((m) => (
              <p
                key={m.k}
                className="flex items-center justify-between border-b border-rule-dark py-[6px]"
              >
                <span className="font-mono text-[8px] tracking-[1.3px] text-inkmute">
                  {m.k}
                </span>
                <span className="font-mono text-[8px] tracking-[1.3px]">
                  {m.v}
                </span>
              </p>
            ))}
          </div>
          <a
            href={waLink(DESK.card.body)}
            className="mt-4 flex items-center justify-center gap-[9px] bg-gelfill px-0 py-[15px] font-mono text-[10px] tracking-[1.5px] text-tent transition-colors hover:bg-gel"
          >
            <WhatsAppGlyph className="h-3.5 w-3.5" />
            {DESK.card.cta}
          </a>
        </aside>
      </Reveal>
    </section>
  );
}
