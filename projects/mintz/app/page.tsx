import TopBar from "./TopBar";
import SmoothScroll from "./SmoothScroll";
import Hero from "./Hero";
import RigSection from "./RigSection";
import JobLog from "./JobLog";
import CuesSection from "./CuesSection";
import TaglineBand from "./TaglineBand";
import Desk from "./Desk";
import Footer from "./Footer";
import WhatsAppSticky from "./WhatsAppSticky";

// Mintz Lights — the cue console. Sections in the signed-off order:
// topbar, hero (console + stage plot), the rig, job log, the cues,
// tagline band, the desk, footer. Real facts only — data/briefs/992.
export default function Home() {
  return (
    <>
      <SmoothScroll />
      <main id="main" className="relative">
        <TopBar />
        <Hero />
        <RigSection />
        <JobLog />
        <CuesSection />
        <TaglineBand />
        <Desk />
        <Footer />
      </main>
      <WhatsAppSticky />
    </>
  );
}
