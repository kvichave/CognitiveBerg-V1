"use client";
import React, { useEffect } from "react";

function page() {
  useEffect(() =>
    fetch(`http://localhost:5000/generatereport`, {
      method: "GET",
      credentials: "include", // Ensures cookies are sent
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Response from server:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      })
  );

  return <div>page</div>;
}

export default page;
