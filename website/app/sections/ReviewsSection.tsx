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
      className="h-screen w-screen cursor-pointer select-none flex flex-col items-center"
      onClick={handleClick}
    >
      <p className="text-7xl text-center font-display pb-4">
        &ldquo;{reviews[pos].review}&rdquo;
      </p>
      <p className="text-6xl text-center font-display mb-14">{reviews[pos].origin}</p>
      <iframe src="https://games.poki.com/458768/8b32c0f4-2dcb-4fdd-bf8b-16df63b01532?tag=pg-v3.130.1&amp;site_id=3&amp;iso_lang=en&amp;country=US&amp;poki_url=https://poki.com/en/g/fruit-ninja" title="Fruit Ninja" width={700} height={400}></iframe>
    </section>
  );
};

export default ReviewsSection;
