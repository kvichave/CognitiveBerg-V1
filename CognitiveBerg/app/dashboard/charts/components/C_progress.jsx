import { useState, useEffect } from "react";

const CircularProgress = ({ percent, color, label, value }) => {
  const circumference = 50 * 2 * Math.PI;
  const offset = circumference - (percent / 100) * circumference;

  return (
    <div className="flex items-center flex-wrap max-w-md px-10 bg-gray-800 shadow-xl rounded-2xl h-20">
      <div className="flex items-center justify-center -m-6 overflow-hidden bg-gray-700 rounded-full">
        <svg
          className="w-32 h-32 transform translate-x-1 translate-y-1"
          aria-hidden="true"
        >
          <circle
            className="text-gray-300"
            strokeWidth="10"
            stroke="currentColor"
            fill="transparent"
            r="50"
            cx="60"
            cy="60"
          />
          <circle
            className={`text-yellow-600`} // Dynamic color
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            stroke="currentColor"
            fill="transparent"
            r="50"
            cx="60"
            cy="60"
          />
        </svg>
      </div>
      <p className="ml-10 font-medium text-gray-600 sm:text-xl">{label}</p>
      &nbsp; &nbsp;
      <span
        className={`ml-auto text-xl font-medium text-yellow-600 hidden sm:block`}
      >
        {value}%
      </span>
    </div>
  );
};

export default CircularProgress;
