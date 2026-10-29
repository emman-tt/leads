"use client";

// QuoteSheet — the form that writes the WhatsApp message. Five real rows
// (what / where / when / guests / photo), a live preview of the message on
// the right, and the CTA opens WhatsApp with it — nothing is submitted
// anywhere else. Photo attaches in WhatsApp by the client; the drop zone
// only confirms the ask.
import { useRef, useState } from "react";
import { BUSINESS, QUOTE, waLink } from "./site-data";
import { WhatsAppGlyph } from "./TopBar";

type Whats = (typeof QUOTE.chips)[number];

export default function QuoteSheet() {
  const [picked, setPicked] = useState<Whats[]>(["LIGHT"]);
  const [venue, setVenue] = useState("");
  const [area, setArea] = useState("");
  const [date, setDate] = useState("");
  const [callTime, setCallTime] = useState("");
  const [guests, setGuests] = useState("");
  const [photo, setPhoto] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const toggle = (c: Whats) =>
    setPicked((prev) =>
      prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]
    );

  const what =
    picked.length > 0
      ? picked.join(" + ").replace("DRESS", "DÉCOR")
      : "—";
  const when = [date, callTime].filter(Boolean).join(" · ") || "—";
  const where = [venue, area].filter(Boolean).join(" — ") || "—";

  const message =
    `Hi Mintz Lights — I am planning` +
    (picked.length ? ` ${picked.join(" + ").toLowerCase()}` : " an event") +
    (guests ? ` for about ${guests} guests` : "") +
    (where !== "—" ? ` at ${where}` : "") +
    (date ? ` on ${date}` : "") +
    (callTime ? `, call time ${callTime}` : "") +
    (photo ? ". Photo attached." : ". One photo of the room to follow.") +
    " Could you quote?";

  return (
    <>
      <SheetHero />
      <div className="flex flex-col gap-12 bg-tent px-5 py-9 text-blackout md:px-[56px] md:flex-row md:gap-12 md:pb-10 md:pt-9">
        {/* form */}
        <div className="min-w-0 flex-1">
          {QUOTE.rows.map((row, i) => (
            <div key={row.n} className="flex flex-col gap-[9px] border-b border-rule-dark py-4">
              <div className="flex flex-wrap items-baseline justify-between gap-1">
                <p className="flex items-baseline gap-3">
                  <span className="font-mono text-[9px] tracking-[1.5px] text-geldeep">
                    {row.n}
                  </span>
                  <span className="font-mono text-[9px] tracking-[1.5px] text-inkmute">
                    {row.label}
                  </span>
                </p>
                <p className="font-mono text-[8px] tracking-[1.2px] text-inkmute">
                  {row.note}
                </p>
              </div>

              {i === 0 && (
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                  {QUOTE.chips.map((c) => {
                    const on = picked.includes(c);
                    return (
                      <button
                        key={c}
                        type="button"
                        aria-pressed={on}
                        onClick={() => toggle(c)}
                        className={`px-0 py-2.5 font-mono text-[9px] tracking-[1.3px] transition-colors ${
                          on
                            ? "bg-gelfill text-tent"
                            : "border border-rule-mid text-blackout hover:border-geldeep"
                        }`}
                      >
                        {c}
                      </button>
                    );
                  })}
                </div>
              )}

              {i === 1 && (
                <div className="flex flex-col gap-2 sm:flex-row">
                  <Field
                    value={venue}
                    onChange={setVenue}
                    placeholder="e.g. a home in Karen"
                    className="sm:w-[336px]"
                  />
                  <Field
                    value={area}
                    onChange={setArea}
                    placeholder="e.g. Karen / Ngara"
                  />
                </div>
              )}

              {i === 2 && (
                <div className="flex flex-col gap-2 sm:flex-row">
                  <Field
                    value={date}
                    onChange={setDate}
                    placeholder="14 February 2027"
                    className="sm:w-[300px]"
                  />
                  <Field
                    value={callTime}
                    onChange={setCallTime}
                    placeholder="e.g. guests at 16:00"
                  />
                </div>
              )}

              {i === 3 && (
                <Field
                  value={guests}
                  onChange={setGuests}
                  placeholder="e.g. 180"
                />
              )}

              {i === 4 && (
                <button
                  type="button"
                  onClick={() => fileRef.current?.click()}
                  className="flex h-[96px] w-full items-center justify-center gap-2.5 border border-dashed border-blackout/25 px-4 hover:border-geldeep"
                >
                  <span className="text-geldeep">⊞</span>
                  <span className="font-mono text-[8.5px] tracking-[1.2px] text-inkmute">
                    {photo
                      ? `SELECTED — ${photo.toUpperCase()} · ATTACHED IN WHATSAPP`
                      : QUOTE.drop}
                  </span>
                </button>
              )}
            </div>
          ))}
          <input
            ref={fileRef}
            type="file"
            accept="image/jpeg,image/heic,image/heif,image/png"
            className="hidden"
            onChange={(e) => setPhoto(e.target.files?.[0]?.name ?? null)}
          />
        </div>

        {/* live preview */}
        <aside className="w-full flex-none bg-blackout p-[22px] text-tent lg:w-[430px]">
          <p className="font-mono text-[9px] tracking-[1.5px] text-peri">
            {QUOTE.prevLabel}
          </p>
          <p className="min-h-[120px] pt-3 text-[16px] leading-[1.6]">
            {message}
          </p>
          <div className="pt-2">
            <PrevRow k="WHAT" v={what} />
            <PrevRow k="WHERE" v={where} />
            <PrevRow k="WHEN" v={when} />
            <PrevRow
              k="PHOTO"
              v={photo ? "1 FRAME · ATTACHED" : "[ ATTACH ]"}
              muted={!photo}
            />
          </div>
          <a
            href={waLink(message)}
            className="mt-4 flex items-center justify-center gap-[9px] bg-gelfill px-0 py-[15px] font-mono text-[10px] tracking-[1.5px] text-tent transition-colors hover:bg-gel"
          >
            <WhatsAppGlyph className="h-3.5 w-3.5" />
            {QUOTE.sendCta}
          </a>
          <p className="pt-2.5 text-[11px] leading-[1.45] text-haze">
            {QUOTE.prevNote}
          </p>
        </aside>
      </div>
      <BeforeYouSend />
    </>
  );
}

function Field({
  value,
  onChange,
  placeholder,
  className = "",
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
  className?: string;
}) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      aria-label={placeholder}
      className={`h-[52px] w-full rounded-none border border-rule-hard bg-transparent px-2.5 pt-1 font-body text-[17px] text-blackout placeholder:text-blackout/40 focus:outline-none focus:ring-1 focus:ring-geldeep ${className}`}
    />
  );
}

function PrevRow({ k, v, muted = false }: { k: string; v: string; muted?: boolean }) {
  return (
    <p className="flex items-center justify-between border-b border-rule-light py-[6px]">
      <span className="font-mono text-[8px] tracking-[1.2px] text-peri">{k}</span>
      <span
        className={`font-mono text-[8px] tracking-[1.1px] ${
          muted ? "text-gelhi" : "text-tent"
        }`}
      >
        {v}
      </span>
    </p>
  );
}

// dark header + dark footer band + "five things" checklist rail
function SheetHero() {
  return (
    <section className="flex flex-wrap items-end justify-between gap-6 px-5 pb-[44px] pt-[54px] md:px-[56px]">
      <div className="max-w-[760px] flex-col gap-4">
        <p className="font-mono text-[10px] tracking-[1.8px] text-gelhi">
          {QUOTE.kicker}
        </p>
        <h1 className="flex items-end gap-4 pt-4 leading-[0.86]">
          <span className="font-display text-[clamp(40px,5.6vw,76px)] font-extrabold tracking-[-2px] text-tent">
            {QUOTE.h1a}
          </span>
          <span className="font-stencil text-[clamp(40px,5.6vw,76px)] font-extrabold tracking-[-1px] text-gel">
            {QUOTE.h1b}
          </span>
        </h1>
        <p className="max-w-[600px] pt-4 text-[16px] leading-[1.55] text-haze">
          {QUOTE.body}
        </p>
      </div>
      <div className="flex flex-col gap-1.5">
        <p className="font-mono text-[9px] tracking-[1.4px] text-haze">
          {QUOTE.meta1}
        </p>
        <p className="font-mono text-[9px] tracking-[1.4px] text-peri">
          {QUOTE.meta2}
        </p>
      </div>
    </section>
  );
}

function BeforeYouSend() {
  return (
    <section className="flex flex-col gap-9 px-5 pb-12 pt-10 md:flex-row md:gap-[56px] md:px-[56px] md:pb-10">
      <div className="min-w-0 flex-1">
        <p className="font-mono text-[9px] tracking-[1.6px] text-gelhi">
          {QUOTE.things.label}
        </p>
        <h2 className="pt-2 font-display text-[clamp(30px,3.2vw,40px)] font-extrabold leading-[0.95] tracking-[-0.4px] text-tent">
          {QUOTE.things.title}
        </h2>
        <ol className="flex flex-wrap gap-x-6 gap-y-4 pt-4">
          {QUOTE.things.items.map((t, i) => (
            <li key={t} className="flex min-w-[180px] max-w-[260px] flex-1 flex-col gap-1.5">
              <span className="font-mono text-[8px] tracking-[1.4px] text-peri">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="font-mono text-[10px] leading-[1.35] tracking-[1px] text-tent">
                {t}
              </span>
            </li>
          ))}
        </ol>
      </div>
      <div className="w-full flex-none lg:w-[360px]">
        <p className="font-mono text-[8px] tracking-[1.4px] text-peri">
          {QUOTE.things.deskLabel}
        </p>
        <p className="pt-2 font-mono text-[10px] leading-[1.5] tracking-[1px] text-tent">
          {BUSINESS.hours.quote}
        </p>
        <p className="pt-2 font-mono text-[10px] leading-[1.5] tracking-[1px] text-haze">
          {BUSINESS.payments.join(" · ")} · 46 KIGWA ROAD, RIDGEWAYS
        </p>
      </div>
    </section>
  );
}
