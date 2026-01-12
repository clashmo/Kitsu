import React from "react";
import Image from "next/image";

const Loading = () => {
  return (
    <div className="w-full py-16 flex items-center justify-center">
      <div className="h-[8rem] w-[8rem] rounded-xl bg-slate-800/40 flex items-center justify-center">
        <Image
          src="/loader.gif"
          height={100}
          width={100}
          unoptimized
          priority
          alt="loader"
          className="h-full w-full object-cover"
          suppressHydrationWarning
        />
      </div>
    </div>
  );
};

export default Loading;
