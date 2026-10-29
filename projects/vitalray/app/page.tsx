import TopBar from "./TopBar";
import SmoothScroll from "./SmoothScroll";
import Hero from "./Hero";
import ServicesGrid from "./ServicesGrid";
import DoctorsBand from "./DoctorsBand";
import JourneyBand from "./JourneyBand";
import InsuranceBand from "./InsuranceBand";
import LocationsBand from "./LocationsBand";
import FinalCta from "./FinalCta";
import Footer from "./Footer";
import WhatsAppSticky from "./WhatsAppSticky";

// VitalRay Health Solutions — the burned "patient report" archetype as a
// real Next site. Flat app/, sections colocated per page folder; everything
// below is verbatim client material from vitalray.com.
export default function Home() {
  return (
    <>
      <SmoothScroll />
      <main id="main" className="relative">
        <TopBar />
        <Hero />
        <ServicesGrid />
        <DoctorsBand />
        <JourneyBand />
        <InsuranceBand />
        <LocationsBand />
        <FinalCta />
        <Footer />
      </main>
      <WhatsAppSticky />
    </>
  );
}
