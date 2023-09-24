import BananaBlindness from "../components/BananaBlindness";

const PriceSection = () => {
  return (
    <div className="h-screen flex items-center justify-center gap-4 flex-col">
      <BananaBlindness width="36rem" />
      <p className="text-6xl font-bold font-display">$0</p>
    </div>
  );
};

export default PriceSection;
