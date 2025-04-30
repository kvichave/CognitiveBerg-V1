"use client";
import { SignedIn, SignedOut, SignIn, SignUp } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import React, { useEffect, useState } from "react";
import {
  Sidebar,
  SidebarBody,
  SidebarLink,
} from "/home/kunal/Documents/CognitiveBerg/components/ui/sidebar";
import {
  IconArrowLeft,
  IconBrandTabler,
  IconSettings,
  IconUserBolt,
  IconArrowAutofitRight,
} from "@tabler/icons-react";
import Link from "next/link";
import { motion } from "framer-motion";
import Image from "next/image";
import { cn } from "/home/kunal/Documents/CognitiveBerg/lib/utils";
import {
  useSignOut,
  UserProfile,
  UserButton,
  SignOutButton,
  useClerk,
} from "@clerk/nextjs";

export default function RootLayout({ children }) {
  const { signOut } = useClerk();
  const handleSignOut = async () => {
    await signOut();
    router.push("/"); // Redirect after sign-out
  };

  const [userprofile, setUser] = useState(() => {
    // Ensure localStorage value exists before parsing
    if (typeof window !== "undefined") {
      const storedUser = localStorage.getItem("user-profile");
      return storedUser ? JSON.parse(storedUser) : {};
    }
    return {};
  });

  useEffect(() => {
    console.log("Updated userprofile:", userprofile);
  }, [userprofile]);
  const router = useRouter();
  const links = [
    {
      label:
        userprofile.scenario == "interview" ? "Interview" : "Business Meeting",
      href:
        userprofile.scenario == "interview"
          ? "/call/interview"
          : "/call/bmeeting",
      icon: (
        <IconArrowAutofitRight className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Dashboard",
      href: "/dashboard",
      icon: (
        <IconBrandTabler className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
    {
      label: "Profile",
      href: "/dashboard/user-profile",
      icon: (
        <IconUserBolt className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },

    // {
    //   label: "Settings",
    //   href: "#",
    //   icon: (
    //     <UserButton
    //     >
    //       <IconSettings className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
    //     </UserButton>
    //   ),
    // },
    {
      label: "Logout",
      href: "#",
      icon: (
        <button onClick={() => handleSignOut()} className="">
          <IconArrowLeft className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />{" "}
        </button>
      ),
    },
  ];
  const [open, setOpen] = useState(false);
  return (
    <>
      {/* {children} */}
      {/* <SignedOut>{router.push("/auth")}</SignedOut> */}
      <div
        className={cn(
          "rounded-md h-screen flex flex-col md:flex-row bg-gray-100 dark:bg-neutral-800 w-screen flex-1  mx-auto border border-neutral-200 dark:border-neutral-700 overflow-hidden"
          // for your use case, use `h-screen` instead of `h-[60vh]`
        )}
      >
        <Sidebar open={open} setOpen={setOpen}>
          <SidebarBody className="justify-between gap-10">
            <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
              {<Logo />}
              {/* {userprofile.scenario == "interview" ? (
                <div className=" flex flex-col gap-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke-width="1.5"
                    stroke="currentColor"
                    class="size-6"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="m3.75 13.5 10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75Z"
                    />
                  </svg>
                  <button
                    className="flex items-center justify-start gap-2  group/sidebar py-2"
                    onClick={() => router.push("/call/interview")}
                  >
                    Interview
                  </button>
                </div>
              ) : (
                <button onClick={() => router.push("/call/bmeeting")}>
                  Business Meeting
                </button>
              )} */}

              <div className="mt-8 flex flex-col gap-2">
                {links.map((link, idx) => (
                  <SidebarLink key={idx} link={link} />
                ))}
              </div>
            </div>
            <div>
              {/* <SidebarLink
                link={{
                  label: "Manu Arora",
                  href: "#",
                  icon: (
                    <Image
                      src="https://assets.aceternity.com/manu.png"
                      className="h-7 w-7 flex-shrink-0 rounded-full"
                      width={50}
                      height={50}
                      alt="Avatar"
                    />
                  ),
                }}
              /> */}
              <UserButton
                // showName
                userProfileProps={{
                  className: "text-lg font-semibold text-blue-400", // Customize name styles here
                }}
              ></UserButton>
            </div>
          </SidebarBody>
        </Sidebar>

        {/* <Dashboard /> */}
        <div className="m-4 bg-black p-4 w-screen border border-neutral-200 dark:border-neutral-700 rounded-xl overflow-y-scroll ">
          {children}
        </div>
      </div>
    </>
  );
}

export const Logo = () => {
  return (
    <Link
      href="/"
      className="font-normal flex space-x-2 items-center text-sm text-black py-1 relative z-20"
    >
      {/* <div className="h-5 w-6 bg-black dark:bg-white text-white rounded-br-lg rounded-tr-sm rounded-tl-lg rounded-bl-sm flex-shrink-0" /> */}
      {/* <Image src={"/logo.png"} width={100} height={100}></Image> */}
      <h1 className="text-white text-xl">𝗖𝗼𝗴𝗻𝗶𝘁𝗶𝘃𝗲 𝗕𝗲𝗿𝗴</h1>
    </Link>
  );
};
export const LogoIcon = () => {
  return (
    <Link
      href="#"
      className="font-normal flex space-x-2 items-center text-sm text-black py-1 relative z-20"
    >
      <div className="h-5 w-6 bg-black dark:bg-white rounded-br-lg rounded-tr-sm rounded-tl-lg rounded-bl-sm flex-shrink-0" />
    </Link>
  );
};

// Dummy dashboard component with content
// const Dashboard = () => {
//   return (
//     <div className="flex flex-1">
//       <div className="p-2 md:p-10 rounded-tl-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-900 flex flex-col gap-2 flex-1 w-full h-full">
//         <div className="flex gap-2">
//           {[...new Array(4)].map((i) => (
//             <div
//               key={"first-array" + i}
//               className="h-20 w-full rounded-lg  bg-gray-100 dark:bg-neutral-800 animate-pulse"
//             ></div>
//           ))}
//         </div>
//         <div className="flex gap-2 flex-1">
//           {[...new Array(2)].map((i) => (
//             <div
//               key={"second-array" + i}
//               className="h-full w-full rounded-lg  bg-gray-100 dark:bg-neutral-800 animate-pulse"
//             ></div>
//           ))}
//         </div>
//       </div>
//     </div>
//   );
// };
