// thumb skip r/l

interface Review {
  review: string;
  origin: string;
}

const reviews = [{ review: "test", origin: "MKBHD" }, {review: "",}];

const ReviewsSection = () => {
  return <section className="h-screen w-screen"></section>;
};

export default ReviewsSection;
