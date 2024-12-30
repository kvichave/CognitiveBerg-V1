"use client";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "/home/kunal/Documents/CognitiveBerg/components/ui/tabs";
import { Spotlight } from "/home/kunal/Documents/CognitiveBerg/components/ui/Spotlight.jsx";
import { PlaceholdersAndVanishInput } from "/home/kunal/Documents/CognitiveBerg/components/ui/placeholders-and-vanish-input.jsx";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useUser } from "@clerk/nextjs";
import { useEffect } from "react";

export default function PlaceholdersAndVanishInputDemo() {
  const { user, isLoaded } = useUser();
  const [loading, setLoading] = useState(true);

  // console.log(user?.id);
  const [userid, setUserId] = useState("");
  const [step, setStep] = useState(0);
  const [role, setRole] = useState("");
  const [field, setField] = useState("");
  const [experience, setExperience] = useState("");
  const [scenario, setScenario] = useState("");
  const [purpose, setPuropse] = useState("");
  const [alreadySubmitted, setAlreadySubmitted] = useState(false);
  const router = useRouter();
  //   const handleChange = (e) => {
  //     console.log(e.target.value);
  //   };

  const onPageLoad = async () => {
    console.log("Page has loaded!");
    if (isLoaded) {
      const response = await fetch(
        "http://localhost:5000/api/check_user_profile",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ user }),
        }
      );
      const result = await response.json();
      console.log(result[0]);
      if (result[0] == true) {
        setAlreadySubmitted(true);
        // router.push("/dashboard");
      }
    }
  };

  // useEffect hook to run on page load
  useEffect(() => {
    if (isLoaded) {
      onPageLoad();
    }
    // Run the function when the page loads
  }, [isLoaded]);

  const [selectedValues, setSelectedValues] = useState([]);

  // Handler for checkbox change
  const handleCheckboxChange = (event) => {
    const { value, checked } = event.target;
    if (checked) {
      // Add value to selected values
      setSelectedValues((prev) => [...prev, value]);
    } else {
      // Remove value from selected values
      setSelectedValues((prev) => prev.filter((v) => v !== value));
    }
  };

  const submitALL = async () => {
    const response = await fetch("http://localhost:5000/api/user_profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user,
        role,
        field,
        experience,
        scenario,
        purpose,
        selectedValues,
      }),
    });

    const result = await response.json();
    alert(`Response from Flask: ${result.message}`);

    // console.log(
    //   role,
    //   field,
    //   experience,
    //   scenario,
    //   purpose,
    //   selectedValues.join(", ")
    // );
  };

  return (
    <div className="h-[40rem] flex flex-col justify-center  items-center px-4">
      {step == 0 && (
        <>
          <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl  text-white">
            Tell me your Role/Position
          </h2>
          <PlaceholdersAndVanishInput
            placeholders={[
              "Software Developer",
              "Manager",
              "Data Scientist",
              "Product Manager",
              "Sales Representative",
              "Customer Service Representative",
              "Marketing Specialist",
              "Human Resources Professional",
              "Accountant",
              "Engineer",
            ]}
            onChange={(e) => setRole(e.target.value)}
            onSubmit={() => (setStep(1), console.log(role))}
          />
        </>
      )}
      {step == 1 && (
        <>
          <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl  text-white">
            Industry/Field of Interest
          </h2>
          <PlaceholdersAndVanishInput
            placeholders={[
              "IT (Information Technology)",
              "Finance",
              "Healthcare",
              "Education",
              "Manufacturing",
            ]}
            onChange={(e) => setField(e.target.value)}
            onSubmit={() => (setStep(2), console.log(field))}
          />
        </>
      )}

      {step == 2 && (
        <>
          <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl  text-white">
            Experience Level
          </h2>
          <div className="flex gap-3 flex-wrap justify-center text-lg">
            <button
              className="text-center my-2 inline-block w-40 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-48"
              onClick={() => (setExperience("0-1"), setStep(3))}
            >
              0-1 Years
            </button>
            <button
              className="text-center my-2 inline-block w-40 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-48"
              onClick={() => (setExperience("1-2"), setStep(3))}
            >
              1-2 Years
            </button>
            <button
              className="text-center my-2 inline-block w-40 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-48"
              onClick={() => (setExperience("2-5"), setStep(3))}
            >
              2-5 Years
            </button>
            <button
              className="text-center my-2 inline-block w-40 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-48"
              onClick={() => (setExperience("5-10"), setStep(3))}
            >
              5-10 Years
            </button>
          </div>
        </>
      )}

      {step == 3 && (
        <>
          <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl  text-white">
            Scenario Type
          </h2>
          <div className="flex gap-3 flex-wrap justify-center text-lg">
            <button
              className="text-center my-2 inline-block w-56 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-60"
              onClick={() => (setScenario("interview"), setStep(4))}
            >
              Interview
            </button>
            <button
              className="text-center my-2 inline-block w-56 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-60"
              onClick={() => (setScenario("Business-meeting"), setStep(4))}
            >
              Business Meeting
            </button>
            <button
              className="text-center my-2 inline-block w-56 rounded-full bg-slate-200 bg-opacity-25 px-4 py-2 font-semibold text-white duration-200 hover:bg-opacity-95 hover:text-black hover:no-underline sm:w-60"
              onClick={() => (
                setScenario("personal-communication"), setStep(4)
              )}
            >
              Personal Communication
            </button>
          </div>
        </>
      )}
      {step == 4 && (
        <>
          <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl  text-white">
            Purpose of Meeting
          </h2>
          <PlaceholdersAndVanishInput
            placeholders={[
              "Job Interview",
              "Promotion Interview",
              "Negotiation",
              "Presentation",
              "Public Speaking",
              "Team Meeting",
              "Client Meeting",
              "Networking Event",
              "Conference",
              "Workshop",
            ]}
            onChange={(e) => setPuropse(e.target.value)}
            onSubmit={() => setStep(5)}
          />
        </>
      )}
      {step == 5 && (
        <>
          <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl  text-white">
            Key Skills to Focus On
          </h2>
          <div className="w-1/2">
            <ul className="text-sm font-medium text-gray-900 bg-white border border-black bg-opacity-95 rounded-lg dark:bg-gray-900 dark:border-black dark:text-white">
              <li className="w-full rounded-t-lg dark:border-gray-600">
                <div className="flex items-center ps-3">
                  <input
                    id="vue-checkbox"
                    type="checkbox"
                    value="technical"
                    onChange={handleCheckboxChange}
                    className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                  />
                  <label
                    htmlFor="vue-checkbox"
                    className="w-full py-3 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >
                    Technical
                  </label>
                </div>
              </li>
              <li className="w-full rounded-t-lg dark:border-gray-600">
                <div className="flex items-center ps-3">
                  <input
                    id="react-checkbox"
                    type="checkbox"
                    value="behavioral"
                    onChange={handleCheckboxChange}
                    className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                  />
                  <label
                    htmlFor="react-checkbox"
                    className="w-full py-3 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >
                    Behavioral
                  </label>
                </div>
              </li>
              <li className="w-full rounded-t-lg dark:border-gray-600">
                <div className="flex items-center ps-3">
                  <input
                    id="angular-checkbox"
                    type="checkbox"
                    value="communication"
                    onChange={handleCheckboxChange}
                    className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
                  />
                  <label
                    htmlFor="angular-checkbox"
                    className="w-full py-3 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                  >
                    Communication
                  </label>
                </div>
              </li>
            </ul>
            <button
              type="Button"
              className="flex m-auto mt-24 justify-center items-center"
              onClick={() => (setStep(6), submitALL())}
            >
              <div class="bg-black ">
                <div class="relative inline-flex  group">
                  <div class="absolute transitiona-all duration-1000 opacity-70 -inset-px bg-gradient-to-r from-[#44BCFF] via-[#FF44EC] to-[#FF675E] rounded-xl blur-lg group-hover:opacity-100 group-hover:-inset-1 group-hover:duration-200 animate-tilt"></div>
                  <a
                    title="Get quote now"
                    class="relative inline-flex items-center justify-center px-8 py-4 text-lg font-bold text-white transition-all duration-200 bg-gray-900 font-pj rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
                    role="button"
                  >
                    Proceed
                  </a>
                </div>
              </div>
            </button>
          </div>
        </>
      )}
      {step == 6 && (
        <>
          <div className="h-full mt-48 w-full dark:bg-black bg-white  dark:bg-grid-white/[0.2] bg-grid-black/[0.2] relative flex items-center justify-center">
            {/* Radial gradient for the container to give a faded look */}
            <div className="absolute pointer-events-none inset-0 flex items-center justify-center dark:bg-black bg-white [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>
            <p className="text-4xl sm:text-7xl font-bold relative z-20 bg-clip-text text-transparent bg-gradient-to-b from-neutral-200 to-neutral-500 py-8">
              Thank You for Your Interest!
            </p>
          </div>
          {/* {setTimeout(() => {
            router.push("/dashboard"); // Replace '/new-page' with the desired route
          }, 5000)} */}
        </>
      )}
      {setUserId}
      {/* {selectedValues} */}
    </div>
  );
}
