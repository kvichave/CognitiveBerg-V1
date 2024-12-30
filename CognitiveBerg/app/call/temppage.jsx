"use client";
import { BackgroundGradientAnimation } from "@/components/ui/background-gradient-animation.jsx";
import { Inter } from "next/font/google";
import io from "socket.io-client";
import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Interviewercard } from "./newCard";

export default function MicrophoneComponent() {
  const websocketRef = useRef(null);

  const router = useRouter();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingComplete, setRecordingComplete] = useState(false);
  const [audiourls, setAudiourls] = useState([]);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speakers, setSpeakers] = useState([]);

  useEffect(() => {
    // Initialize WebSocket
    if (!websocketRef.current) {
      websocketRef.current = io("http://localhost:5000", {
        transports: ["websocket"],
      });

      websocketRef.current.on("connect", () => {
        console.log("WebSocket connection established");
      });

      websocketRef.current.on("disconnect", () => {
        console.log("WebSocket disconnected");
      });

      websocketRef.current.on("audio_urls", (files) => {
        const inter = files.interviewers;
        const updatedSpeakers = inter.map((interviewer) => ({
          ...interviewer,
          isSpeaking: false,
        }));
        setSpeakers(updatedSpeakers);

        const uniqueAudioUrls = files.files.map(
          (url) => `${url}?timestamp=${new Date().getTime()}`
        );
        setAudiourls(uniqueAudioUrls);
        setIsPlaying(true);
      });
    }

    // Cleanup WebSocket connection when component unmounts
    return () => {
      if (websocketRef.current) {
        websocketRef.current.disconnect();
      }

      if (mediaRecorderRef.current) {
        stopRecording();
      }
    };
  }, []);

  const startRecording = async () => {
    setIsRecording(true);
    audioChunksRef.current = [];

    try {
      // Access user's microphone
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (websocketRef.current && event.data.size > 0) {
          const reader = new FileReader();
          reader.onload = () => {
            const audioBuffer = reader.result;
            websocketRef.current.emit("audio_chunk", audioBuffer);
          };
          reader.readAsArrayBuffer(event.data);
        }
      };

      mediaRecorderRef.current.start(200);
      websocketRef.current.emit("start");
      console.log("Recording started");

      mediaRecorderRef.current.onstop = () => {
        setIsRecording(false);
        websocketRef.current.emit("stop");
        console.log("Recording stopped");
      };
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecordingComplete(true);
      setIsRecording(false);
      mediaRecorderRef.current.stream
        .getTracks()
        .forEach((track) => track.stop());
      mediaRecorderRef.current = null;
    }
  };

  const playAudio = () => {
    if (currentIndex < audiourls.length) {
      const audio = new Audio(audiourls[currentIndex]);
      audio.play(toggleSpeaking(currentIndex)).catch((error) => {
        console.error("Error playing audio:", error);
      });

      audio.addEventListener("ended", () => {
        setCurrentIndex((prevIndex) => prevIndex + 1);
      });
    } else {
      setIsPlaying(false);
      setCurrentIndex(0);
      setAudiourls([]);
      updateSpeakers();
    }
  };
  const updateSpeakers = () => {
    setSpeakers((prevSpeakers) =>
      prevSpeakers.map((interviewer) => ({
        ...interviewer,
        isSpeaking: false,
      }))
    );
  };

  useEffect(() => {
    if (isPlaying && audiourls.length > 0) {
      playAudio();
    }
  }, [currentIndex, isPlaying, audiourls]);

  const toggleSpeaking = (id) => {
    setSpeakers((prevUsers) =>
      prevUsers.map(
        (user) =>
          user.id === id
            ? { ...user, isSpeaking: !user.isSpeaking }
            : { ...user, isSpeaking: false } // Ensure only one speaks at a time
      )
    );
  };
  const handleToggleRecording = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <BackgroundGradientAnimation>
      <div className="relative z-50">
        <div className="flex items-center justify-center text-3xl pt-24 font-bold">
          {isRecording ? "Recording..." : "Click to start recording"}
        </div>

        <div className="flex flex-col items-center justify-center h-screen w-full">
          <div className="flex flex-row items-center justify-center">
            {speakers.length > 0
              ? speakers.map((user, index) => (
                  <div key={user.id} className={`m-16 animate-slide-in-up`}>
                    <Interviewercard
                      isSpeaking={user.isSpeaking}
                      userName={user.interviewer_name}
                      imageLink="https://static.vecteezy.com/system/resources/previews/008/332/204/non_2x/3d-young-smiling-man-with-dark-sin-tone-and-black-hair-people-cartoon-cute-minimal-character-style-illustration-user-avatar-in-round-frame-isolated-on-white-background-vector.jpg"
                    />
                  </div>
                ))
              : null}
          </div>

          {isRecording && (
            <div className="w-1/4 m-auto rounded-md border p-4 bg-white">
              <p className="text-sm font-medium leading-none">
                {recordingComplete ? "" : "Recording..."}
              </p>
              <p className="text-sm text-muted-foreground">
                {recordingComplete
                  ? "Thanks for talking."
                  : "Start speaking..."}
              </p>
            </div>
          )}

          <div className="flex items-center justify-center">
            <button
              onClick={handleToggleRecording}
              className={`${
                isRecording ? "bg-red-400" : "bg-white hover:bg-gray-400"
              } mt-10 m-auto flex items-center justify-center rounded-full w-20 h-20`}
            >
              {isRecording ? (
                <svg className="h-12 w-12" viewBox="0 0 24 24">
                  <path fill="white" d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                </svg>
              ) : (
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
              )}
            </button>
          </div>

          <div
            onClick={() => router.push("/report")}
            className="m-auto border bg-black border-black rounded w-fit h-fit p-4 flex items-center justify-center -mb-24 mt-24"
          >
            Generate Report
          </div>
        </div>
      </div>
    </BackgroundGradientAnimation>
  );
}
