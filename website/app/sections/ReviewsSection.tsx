/* eslint-disable jsx-a11y/no-static-element-interactions */
// thumb skip r/l

import { useState } from "react";

interface Review {
  review: string;
  origin: string;
}

const reviews: Review[] = [
  { review: "this is actually nuts", origin: "- mkbhd" },
  { review: "sensational", origin: "- the verge" },
  { review: "this is the future", origin: "- darth vader" },
  { review: "these quotes are fake", origin: "- blind banana" },
];

const ReviewsSection = () => {
  const [pos, setPos] = useState<number>(0);

  const handleClick = () => {
    if (pos === reviews.length - 1) return;

    setPos((prev) => prev + 1);
  };

  return (
    <section
      className="h-screen cursor-pointer select-none flex flex-col items-center"
      onClick={handleClick}
    >
      <p className="text-7xl text-center font-display pb-4">
        &ldquo;{reviews[pos].review}&rdquo;
      </p>
      <p className="text-6xl text-center font-display mb-24">{reviews[pos].origin}</p>
      <a href="https://youtube.com/shorts" className="text-4xl underline hover:no-underline">YouTube Shorts</a>
    </section>
  );
};

export default ReviewsSection;
