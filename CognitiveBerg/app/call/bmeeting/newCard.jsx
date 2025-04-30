"use client";
import React, { useState, useEffect } from "react";
import { BackgroundGradient } from "/components/ui/background-gradient";
import Image from "next/image";

export function Interviewercard({ isSpeaking, userName, imageLink }) {
  const [animate, setAnimate] = useState(false); // By default animation is off

  useEffect(() => {
    // Simulate toggling animation every 2 seconds
    const interval = setInterval(() => {
      setAnimate((prev) => !prev);
    }, 2000);

    // Cleanup interval on unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <BackgroundGradient
        isSpeaking={isSpeaking}
        animate={animate} // Pass the dynamic animation state here
        className="rounded-[22px] w-64  max-w-sm p-4 sm:p-10 bg-white dark:bg-white"
      >
        <Image
          src={
            imageLink
              ? imageLink
              : `https://static.vecteezy.com/system/resources/thumbnails/011/381/900/small_2x/young-businessman-3d-cartoon-avatar-portrait-png.png`
          }
          alt="jordans"
          height="400"
          width="400"
          className="object-contain"
        />
        <p className="text-base sm:text-xl text-black mt-4 mb-2 ">{userName}</p>

        <p className="text-sm text-neutral-600 dark:text-black">
          {/* The Air Jordan 4 Retro Reimagined Bred will release on Saturday,
          February 17, 2024. Your best opportunity to get these right now is by
          entering raffles and waiting for the official releases. */}
        </p>
        {isSpeaking ? (
          <button className="rounded-full pl-4 pr-1 py-1 text-white flex items-center space-x-1 bg-green-500 mt-4 text-xs font-bold ">
            <span>SPEAKING </span>
            <span className="bg-white rounded-full text-[0.6rem] px-2 py-0 text-white">
              &nbsp;
            </span>
          </button>
        ) : (
          ""
        )}
      </BackgroundGradient>
    </div>
  );
}
