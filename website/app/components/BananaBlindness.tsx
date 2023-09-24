import Image from "next/image";

interface Props {
  width: string;
}

const BananaBlindness = ({ width }: Props) => {
  return (
    <div style={{ width }} className="relative aspect-[1244/468]">
      <Image
        className="object-contain"
        src="/banana-blindness.png"
        alt="Banana Blindness"
        fill
        unoptimized
      />
    </div>
  );
};

export default BananaBlindness;
