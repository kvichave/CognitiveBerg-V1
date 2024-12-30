"use client";
import { SignedIn, SignedOut, SignIn, SignUp } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { BackgroundBeams } from "../../components/ui/background-beams.jsx";
export default function RootLayout({ children }) {
  const router = useRouter();
  return (
    <>
      <div className=" relative z-20 flex flex-row min-h-screen justify-center items-center">
        {children}
      </div>

      <BackgroundBeams />
    </>
  );
}
