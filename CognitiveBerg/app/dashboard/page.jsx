"use client";
import { SignedIn } from "@clerk/nextjs";
import React, { useEffect, useState } from "react";
// import Barchart1 from "/home/kunal/Documents/CognitiveBerg/app/dashboard/charts/Barchart1.jsx";
import { useUser } from "@clerk/nextjs";
const Page = () => {
  // const [count, setCount] = useState(0);
  const { user, isLoaded } = useUser();
  const { udata, setData } = useUser("");

  useEffect(() => {
    if (isLoaded && user) {
      // Send the Clerk user details to Flask backend
      const response = fetch("http://localhost:5000/setsession", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: user.id,
          email: user.primaryEmailAddress?.emailAddress,
        }),
        // credentials: "include", // Send cookies to Flask for session
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
        })
        .catch((error) => console.error("Error:", error));

      // console.log("Response:", udata);
      getData();
    }
  }, [isLoaded, user]);

  async function getData() {
    console.log("inside get data");
    const response = await fetch(
      "http://localhost:5000/api/dashboard_data_fetch",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Credentials": "true",
        },
        // body: JSON.stringify(),
      }
    );

    const result = await response.json();
    console.log(result);
  }

  // setCount(result);

  return (
    <div>
      {/* this is english score and fluency score */}
      <div className="stats-section py-10 px-5">
        <div className="stats-grid z-20 max-w-5xl rounded-xl bg-[#FF6347] dark:bg-[#4B5563] mx-auto grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 items-center justify-between md:px-10 gap-x-10 py-10 px-5 lg:px-10 gap-y-5">
          <div className="col-span-1 md:col-span-3 lg:col-span-1 flex flex-col items-center justify-center gap-y-3">
            <h2 className="text-3xl md:pb-5 md:text-3xl text-white dark:text-gray-200 font-bold">
              Here are your scores
            </h2>
          </div>
          <div className="col-span-1 md:col-span-1 lg:col-span-1 flex flex-col items-center justify-center gap-y-3">
            <h2 className="text-3xl lg:text-5xl text-white dark:text-gray-200 font-bold">
              1.2M
            </h2>
            <p className="text-center text-sm md:text-base text-white dark:text-gray-400">
              Members worldwide
            </p>
          </div>
          <div className="col-span-1 md:col-span-1 lg:col-span-1 flex flex-col items-center justify-center gap-y-3">
            <h2 className="text-3xl lg:text-5xl text-white dark:text-gray-200 font-bold">
              95%
            </h2>
            <p className="text-center text-sm md:text-base text-white dark:text-gray-400">
              Customer satisfaction rate
            </p>
          </div>
          <div className="col-span-1 md:col-span-1 lg:col-span-1 flex flex-col items-center justify-center gap-y-3">
            <h2 className="text-3xl lg:text-5xl text-white dark:text-gray-200 font-bold">
              3500+
            </h2>
            <p className="text-center text-sm md:text-base text-white dark:text-gray-400">
              Transactions processed daily
            </p>
          </div>
        </div>
      </div>
      {/* {udata} */}
    </div>
  );
};

export default Page;
