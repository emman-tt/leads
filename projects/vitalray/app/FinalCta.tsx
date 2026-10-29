import { BUSINESS } from "./site-data";

// Final CTA — teal closing band. Book the scan; reports run through the
// patient portal. Server component.
export default function FinalCta() {
  return (
    <section
      aria-label="Book the scan"
      className="w-full bg-teal px-5 py-14 md:px-[50px] md:py-[54px]"
    >
      <div className="mx-auto flex max-w-[1180px] flex-col gap-9 md:flex-row md:items-center md:justify-between md:gap-9">
        <div className="flex flex-col gap-2.5 md:max-w-[700px]">
          <h2 className="max-w-[700px] font-display text-[clamp(28px,3.2vw,44px)] leading-[1.08] font-semibold text-paper">
            Book the scan. Leave with prints that explain.
          </h2>
          <p className="max-w-[640px] text-[13.5px] leading-[1.55] font-semibold text-glow">
            Appointments, billing questions and report requests run through the
            patient portal — or simply call the desk.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <a
            href={BUSINESS.portal.book}
            className="block flex-none rounded-[3px] bg-deep px-6 py-[14px] text-[13px] font-bold text-paper transition-colors hover:bg-[#0b1a1f]"
          >
            BOOK AN APPOINTMENT →
          </a>
          <a
            href={BUSINESS.portal.reports}
            className="block flex-none rounded-[3px] bg-paper px-6 py-[14px] text-[13px] font-bold text-deep ring-1 ring-deep transition-colors hover:bg-glow/40"
          >
            REQUEST MEDICAL REPORTS
          </a>
        </div>
      </div>
    </section>
  );
}
