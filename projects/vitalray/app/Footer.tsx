import { BUSINESS, LOCATIONS } from "./site-data";

// Footer — one name line, one mono facts line. Server component.
export default function Footer() {
  return (
    <footer className="w-full bg-deep px-5 py-[30px] md:px-[50px]">
      <div className="mx-auto flex max-w-[1180px] flex-col gap-2">
        <p className="font-display text-[15px] font-semibold text-paper">
          {BUSINESS.name.toUpperCase()} — outpatient hospital ·{" "}
          {LOCATIONS[0].area} + {LOCATIONS[1].area}, Nairobi
        </p>
        <p className="font-mono text-[9.5px] text-glow md:max-w-[900px]">
          {BUSINESS.email} · {BUSINESS.tel} · {BUSINESS.site} · radiology,
          laboratory &amp; day care at {LOCATIONS[0].area} +{" "}
          {LOCATIONS[1].area} · {BUSINESS.hours}
        </p>
      </div>
    </footer>
  );
}
