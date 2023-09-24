import { Metadata } from "next";
import { Playfair, Playfair_Display } from "next/font/google";
import "../index.css";

const playfairDisplay = Playfair_Display({
  subsets: ["latin"],
  weight: ["400", "700", "900"],
  variable: "--playfair-display",
});
const playfair = Playfair({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
  variable: "--playfair",
});

export const metadata: Metadata = {
  title: "Banana Blindness",
  description: "",
};

const RootLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <html lang="en">
      <body className={`bg-yellow ${playfair.className} ${playfairDisplay.className}`}>
        {children}
      </body>
    </html>
  );
};

export default RootLayout;
