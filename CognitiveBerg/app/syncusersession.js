"use client";

import { useUser } from "@clerk/nextjs";
import { useEffect, useState } from "react";

export default function SyncUserSession() {
  const { user, isLoaded } = useUser();
  const [isSyncing, setIsSyncing] = useState(true); // Track sync state

  useEffect(() => {
    if (isLoaded && user) {
      console.log("Sending session data to Flask");
      fetch(
        `http://localhost:5000/setsession?user_id=${user.id}&email=${user.primaryEmailAddress?.emailAddress}`,
        {
          method: "GET",
          credentials: "include", // Ensures cookies are sent
        }
      )
        .then((response) => response.json())
        .then((data) => {
          console.log("Response from server:", data);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  }, [isLoaded, user]);

  // If syncing data or waiting for user data, return nothing (still rendering children)
  if (isSyncing) {
    return null;
  }

  return null;
}
