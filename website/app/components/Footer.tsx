import BananaBlindness from "./BananaBlindness";

const Footer = () => {
  return (
    <footer className="fixed bottom-8 px-10 flex justify-between w-full">
      <p className="font-display text-lg flex items-end leading-none">
        Alex Luo, Aryan Sharma, Daud Idrees, Sai Chandra
      </p>
      <BananaBlindness width="12rem" />
    </footer>
  );
};

export default Footer;
