import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    fontFamily: {
      display: ["var(--playfair-display)"],
      body: ["var(--playfair)"],
    },
    colors: {
      yellow: "#ffe49e",
      black: "#000000"
    },
  },
  plugins: [],
};
export default config;
