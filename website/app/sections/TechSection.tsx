import Image from "next/image";

// thumb skip r/l
const TechSection = () => {
  return (
    <section className="min-h-screen pb">
      <h2 className="text-center pb-8">tech stack</h2>
      <div className="grid mx-auto grid-cols-2 w-fit gap-12 pb-48">
        <div className="flex flex-col gap-12 items-center">
          <h3 className="text-5xl font-display text-center">banana app</h3>
          <div className="p-12 w-full">
            <div className="relative w-full aspect-square">
              <Image
                className="object-contain"
                src="/python.png"
                alt="Python"
                width={200}
                height={200}
              />
            </div>
          </div>
          <div className="p-12 w-full">
            <div className="relative w-full aspect-square">
                <Image
                className="object-contain"
                src="/opencv.png"
                alt="OpenCV"
                width={200}
                height={200}
                />
            </div>
          </div>
          <div className="p-12 w-full">
            <div className="relative w-full aspect-video">
                <Image
                className="object-contain"
                src="/mediapipe.png"
                alt="Media Pipe"
                width={200}
                height={200}
                />
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-12 items-center">
          <h3 className="text-5xl font-display text-center">
            demo site (this)
          </h3>
          <div className="p-12 w-full">
          <div className="relative w-full aspect-video">
            <Image
              className="object-contain"
              src="/nextjs.png"
              alt="Next.js"
              fill
            />
          </div>
          </div>
          <div className="relative w-full aspect-video">
            <Image
              className="object-contain"
              src="/typescript.png"
              alt="TypeScript"
              fill
            />
          </div>
          <div className="relative w-full aspect-video">
            <Image
              className="object-contain"
              src="/tailwindcss.png"
              alt="TailwindCSS"
              fill
            />
          </div>
          <div className="relative w-full aspect-video">
            <Image
              className="object-contain"
              src="/vercel.png"
              alt="Vercel"
              width={300}
              height={300}
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default TechSection;
