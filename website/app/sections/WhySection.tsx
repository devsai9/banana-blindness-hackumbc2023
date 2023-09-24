import { useState } from "react";
import { motion } from "framer-motion";
import dynamic from "next/dynamic";

const ReactPlayer = dynamic(() => import("react-player/lazy"), { ssr: false });

// cursor move/click to reveal
const WhySection = () => {
  const [visible, setVisible] = useState<boolean>(false);

  return (
    <section className="h-screen flex flex-col items-center ">
      <h2 className="text-center pb-8">why banana blindness?</h2>
      {visible ? (
        <p className="font-black text-8xl text-center mb-6">we&apos;re broke</p>
      ) : (
        <button
          className="w-32 h-32 flex items-center justify-center mb-6"
          onClick={() => setVisible(true)}
        >
          <motion.svg
            initial={{}}
            animate
            width="6rem"
            height="6rem"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 448 512"
          > 
            <path d="M128 40c0-22.1 17.9-40 40-40s40 17.9 40 40V188.2c8.5-7.6 19.7-12.2 32-12.2c20.6 0 38.2 13 45 31.2c8.8-9.3 21.2-15.2 35-15.2c25.3 0 46 19.5 47.9 44.3c8.5-7.7 19.8-12.3 32.1-12.3c26.5 0 48 21.5 48 48v48 16 48c0 70.7-57.3 128-128 128l-16 0H240l-.1 0h-5.2c-5 0-9.9-.3-14.7-1c-55.3-5.6-106.2-34-140-79L8 336c-13.3-17.7-9.7-42.7 8-56s42.7-9.7 56 8l56 74.7V40zM240 304c0-8.8-7.2-16-16-16s-16 7.2-16 16v96c0 8.8 7.2 16 16 16s16-7.2 16-16V304zm48-16c-8.8 0-16 7.2-16 16v96c0 8.8 7.2 16 16 16s16-7.2 16-16V304c0-8.8-7.2-16-16-16zm80 16c0-8.8-7.2-16-16-16s-16 7.2-16 16v96c0 8.8 7.2 16 16 16s16-7.2 16-16V304z" />
          </motion.svg>
        </button>
      )}
      <ReactPlayer url="https://www.youtube.com/watch?v=GYkq9Rgoj8E&t=2h1m27s" width="650px" justify-content="center"/>
    </section>
  );
};

export default WhySection;
