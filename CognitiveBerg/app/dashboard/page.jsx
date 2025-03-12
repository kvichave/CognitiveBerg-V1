"use client";
import { SignedIn } from "@clerk/nextjs";
import React, { useEffect, useState } from "react";
// import Barchart1 from "/home/kunal/Documents/CognitiveBerg/app/dashboard/charts/Barchart1.jsx";
import { useUser } from "@clerk/nextjs";
import AnalysisDashboard from "./charts/Analysis.jsx";
const Page = () => {
  // const [count, setCount] = useState(0);
  const { user, isLoaded } = useUser();
  const { udata, setData } = useUser("");

  // useEffect(() => {
  //   if (isLoaded && user) {
  //     // Send the Clerk user details to Flask backend
  //     const response = fetch("http://localhost:5000/setsession", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         user_id: user.id,
  //         email: user.primaryEmailAddress?.emailAddress,
  //       }),
  //       // credentials: "include", // Send cookies to Flask for session
  //     })
  //       .then((response) => response.json())
  //       .then((data) => {
  //         console.log(data);
  //       })
  //       .catch((error) => console.error("Error:", error));

  //     // console.log("Response:", udata);
  //     // getData();
  //   }
  // }, [isLoaded, user]);

  // async function getData() {
  //   console.log("inside get data");
  //   const response = await fetch(
  //     "http://localhost:5000/api/dashboard_data_fetch",
  //     {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //         "Access-Control-Allow-Credentials": "true",
  //       },
  //       // body: JSON.stringify(),
  //     }
  //   );

  //   const result = await response.json();
  //   console.log(result);
  // }

  // setCount(result);

  return (
    <div className=" items-center justify-center min-h-screen ">
      {/* this is english score and fluency score */}

      {/* {udata} */}
      <AnalysisDashboard />
    </div>
  );
};

export default Page;
