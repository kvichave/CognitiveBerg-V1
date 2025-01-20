"use client";
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation.jsx";
import { Inter } from "next/font/google";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";

export default function MicrophoneComponent() {
  const router = useRouter();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingComplete, setRecordingComplete] = useState(false);
  const [reply, setTranscript] = useState("");
  const [audiourls, setAudiourls] = useState([]);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [msg, setMsg] = useState("");
  const [firstLoad, setFirstLoad] = useState(true);
  const [initialData, setInitialData] = useState(null);

  // Fetch initial data on load
  useEffect(() => {
    const fetchDataOnLoad = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/clearData");
        const data = await response.json();
        setInitialData(data);
        console.log("Initial data loaded:", data);
      } catch (error) {
        console.error("Error fetching initial data:", error);
      }
    };

    fetchDataOnLoad();
  }, []);
  const startRecording = async () => {
    setIsRecording(true);
    audioChunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, {
          type: "audio/mp3",
        });
        const audioFile = new File([audioBlob], "recorded_audio.mp3", {
          type: "audio/mp3",
        });

        const formData = new FormData();
        formData.append("audio", audioFile);

        // Clear old state before new data fetch
        setAudiourls([]);
        setCurrentIndex(0);
        setIsPlaying(false);

        try {
          const response = await fetch("http://127.0.0.1:5000/send_audio", {
            method: "POST",
            body: formData,
          });

          const data = await response.json();
          setFirstLoad(false);
          setTranscript([JSON.parse(data.bot_reply)]);
          const uniqueAudioUrls = data.audio_urls.map(
            (url) => `${url}?timestamp=${new Date().getTime()}`
          );
          // Set new audio URLs and start playback
          setAudiourls(uniqueAudioUrls);
          setIsPlaying(true); // Starts playback on new URLs
        } catch (error) {
          console.error("Error sending audio to server:", error);
        }
      };

      mediaRecorderRef.current.start();
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  useEffect(() => {
    const playAudio = () => {
      if (currentIndex < audiourls.length) {
        if (reply[0]?.length > 1) {
          setMsg(reply[0][currentIndex]["message"]);
        } else if (reply.length === 1) {
          setMsg(reply[0].message || reply[0][0]?.message);
        } else if (reply[0]?.length === 1) {
          setMsg(reply[0][0]["message"]);
        }

        const audio = new Audio(audiourls[currentIndex]);
        audio.play().catch((error) => {
          console.error("Error playing audio:", error);
        });

        audio.addEventListener("ended", () => {
          setCurrentIndex((prevIndex) => prevIndex + 1);
        });
      } else {
        setIsPlaying(false);
        setCurrentIndex(0);
        setAudiourls([]);
      }
    };

    if (isPlaying && audiourls.length > 0) {
      playAudio();
    }
  }, [currentIndex, isPlaying, audiourls]);
  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecordingComplete(true);
      setIsRecording(false);
    }
  };

  const handleToggleRecording = () => {
    if (!isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  };

  return (
    <BackgroundGradientAnimation>
      <div className="relative z-50">
        {firstLoad && (
          <div className="flex items-center justify-center text-3xl pt-24 font-bold">
            You can say <h1 className="italic">&quot;Lets get started&quot;</h1>
          </div>
        )}

        <div className="flex items-center justify-center h-screen w-full">
          <div className="w-full relative">
            {(isRecording || reply) && (
              <div className="w-1/4 m-auto rounded-md border p-4 bg-white">
                <div className="flex-1 flex w-full justify-between">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">
                      {recordingComplete ? "" : "Recording"}
                    </p>
                    <p className="text-sm text-black text-muted-foreground">
                      {recordingComplete
                        ? "Thanks for talking."
                        : "Start speaking..."}
                    </p>
                  </div>
                  {isRecording && (
                    <div className="rounded-full w-4 h-4 bg-red-400 animate-pulse" />
                  )}
                </div>

                {reply && (
                  <div className="border rounded-md p-2 h-full mt-4">
                    <p className="mb-0 text-2xl font-quicksand text-black">
                      {msg}
                    </p>
                  </div>
                )}
              </div>
            )}

            <div className="flex z-50 items-center w-full relative">
              {isRecording ? (
                <button
                  onClick={handleToggleRecording}
                  disabled={isPlaying}
                  className="mt-10 m-auto flex items-center justify-center bg-red-400 hover:bg-red-500 rounded-full w-20 h-20 focus:outline-none relative"
                >
                  <svg
                    className="h-12 w-12"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path fill="white" d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                  </svg>
                </button>
              ) : (
                <button
                  onClick={handleToggleRecording}
                  disabled={isPlaying}
                  className="mt-10 m-auto flex items-center justify-center bg-white hover:bg-blue-500 rounded-full w-20 h-20 focus:outline-none relative"
                >
                  <svg
                    viewBox="0 0 256 256"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-12 h-12 text-white"
                  >
                    <path
                      fill="black"
                      d="M128 176a48.05 48.05 0 0 0 48-48V64a48 48 0 0 0-96 0v64a48.05 48.05 0 0 0 48 48ZM96 64a32 32 0 0 1 64 0v64a32 32 0 0 1-64 0Zm40 143.6V232a8 8 0 0 1-16 0v-24.4A80.11 80.11 0 0 1 48 128a8 8 0 0 1 16 0a64 64 0 0 0 128 0a8 8 0 0 1 16 0a80.11 80.11 0 0 1-72 79.6Z"
                    />
                  </svg>
                </button>
              )}
            </div>
            <div
              onClick={() => router.push("/report")}
              className="m-auto border bg-black border-black rounded w-fit h-fit p-4 flex items-center justify-center -mb-24 mt-24"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth="1.5"
                stroke="currentColor"
                className="size-10"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
                />
              </svg>
              Generate Report
            </div>
          </div>
        </div>
      </div>
    </BackgroundGradientAnimation>
  );
}
