"use client";

import Footer from "./components/Footer";
import FrontSection from "./sections/FrontSection";
import ReviewsSection from "./sections/ReviewsSection";
import TechSection from "./sections/TechSection";
import WhySection from "./sections/WhySection";

// right/left arrow (skip) thumb, cursor move pointer, cursor click tap pointer thumb, scroll peace
// slide up/down scroll
// cursor move/click why reveal
// r/l skip tech
// close hand to stop watching
// gui
// TODO: cursor hacking
const Home = () => {
  return (
    <main className="bg-yellow font-body">
      <FrontSection />
      <WhySection />
      <TechSection />
      <ReviewsSection />
      <Footer />
    </main>
  );
};

export default Home;
