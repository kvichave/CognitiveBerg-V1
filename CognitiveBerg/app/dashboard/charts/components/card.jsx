import React from "react";

export function bannercard({ title, content }) {
  return (
    <>
      <div class="flex flex-wrap items-center justify-center gap-y-2 bg-black">
        <div class="px-10 py-4 sm:px-20 ">
          <p class="mb-0 whitespace-nowrap bg-gradient-to-b from-white to-gray-400 bg-clip-text text-4xl font-black text-transparent sm:text-6xl">
            {content}
          </p>
          <p class="mt-2 text-center text-lg leading-relaxed tracking-wide text-gray-400">
            {title}
          </p>
        </div>
      </div>
    </>
  );
}
