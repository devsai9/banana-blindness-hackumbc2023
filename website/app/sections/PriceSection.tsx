import BananaBlindness from "../components/BananaBlindness";

const PriceSection = () => {
  return (
    <div className="h-screen flex items-center justify-center gap-4 flex-col">
      <p className="text-6xl font-bold font-display">Only $0</p>
      <BananaBlindness width="36rem" />
    </div>
  );
};

export default PriceSection;
