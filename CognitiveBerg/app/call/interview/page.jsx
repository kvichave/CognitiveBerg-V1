"use client";
import { BackgroundGradientAnimation } from "/components/ui/background-gradient-animation";
import { Inter } from "next/font/google";
import io from "socket.io-client";
import UserCard from "./userCard";
import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Interviewercard } from "./newCard";

import { PinContainer } from "/components/ui/3d-pin";
export default function MicrophoneComponent() {
  const websocketRef = useRef(null);

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
  const [speakers, setSpeakers] = useState([]);
  const [audioContext, setAudioContext] = useState(null);
  const [analyser, setAnalyser] = useState(null);
  const silenceTimeoutRef = useRef(null);
  const animationFrameRef = useRef(null);
  const [voice_detected, setVoice_detected] = useState(false);

  useEffect(() => {
    websocketRef.current = io("http://localhost:5000", {
      transports: ["websocket"],
    });

    websocketRef.current.on("connect", () => {
      console.log("WebSocket connection established");
    });

    // Initialize voice detection
    const initializeVoiceDetection = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        // detectSilence(stream);
        console.log("Voice detection initialized");
      } catch (error) {
        console.error("Error initializing voice detection:", error);
      }
    };

    // initializeVoiceDetection();

    websocketRef.current.on("interview_end", () => {
      console.log("WebSocket connection established");
      router.push("/dashboard");
    });

    websocketRef.current.on("audio_urls", (files) => {
      if (isRecording) {
        stopRecording();
      }
      console.log("WebSocket audio_urls event received", files.files);
      // console.log(
      //   "WebSocket audio_urls event received",
      //   files.interviewers[0]
      // );
      const inter = files.interviewers;
      const inte = inter.map((interviewer) => ({
        ...interviewer,
        isSpeaking: false,
      })); // Received data (assume it's an array)

      setSpeakers((prevSpeakers) => {
        if (prevSpeakers.length === 0) {
          // Initialize only if speakers are not set
          return inte;
        }
        // Keep the previous data if already set
        return prevSpeakers;
      });

      const uniqueAudioUrls = files.files.map(
        (url) => `${url}?timestamp=${new Date().getTime()}`
      );
      // Set new audio URLs and start playback
      setAudiourls(uniqueAudioUrls);
      setIsPlaying(true);
    });
    return () => {
      if (websocketRef.current) {
        websocketRef.current.disconnect();
      }

      if (mediaRecorderRef.current) {
        stopRecording();
      }
    };
  }, []);
  // Fetch initial data on load
  // useEffect(() => {
  //   const fetchDataOnLoad = async () => {
  //     try {
  //       const response = await fetch("http://127.0.0.1:5000/clearData");
  //       const data = await response.json();
  //       setInitialData(data);
  //       console.log("Initial data loaded:", data);
  //     } catch (error) {
  //       console.error("Error fetching initial data:", error);
  //     }
  //   };

  //   fetchDataOnLoad();
  // }, []);
  const detectSilence = (
    stream,
    silenceThreshold = -30,
    silenceDuration = 2000
  ) => {
    const audioContext = new AudioContext();
    const analyser = audioContext.createAnalyser();
    const microphone = audioContext.createMediaStreamSource(stream);
    microphone.connect(analyser);

    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Float32Array(bufferLength);

    setAudioContext(audioContext);
    setAnalyser(analyser);

    const checkAudioLevel = () => {
      analyser.getFloatTimeDomainData(dataArray);
      let sumSquares = 0.0;
      for (const amplitude of dataArray) {
        sumSquares += amplitude * amplitude;
      }
      const volume = Math.sqrt(sumSquares / dataArray.length);
      var volumeDb = 20 * Math.log10(volume);

      console.log("Current volume:", volumeDb, "isRecording:", isRecording);

      if (volumeDb > silenceThreshold) {
        // Sound detected
        if (!isRecording && !isPlaying) {
          console.log("Sound detected, starting recording");
          // startRecording();
          setVoice_detected(true);
          setIsRecording(true);
          console.log("lets check isRecording", isRecording);
        }
        // Clear any existing silence timeout
        if (silenceTimeoutRef.current) {
          console.log("Clearing silence timeout");
          clearTimeout(silenceTimeoutRef.current);
          silenceTimeoutRef.current = null;
        }
      } else {
        // Silence detected
        // console.log(
        //   "Silence detected, isRecording:",
        //   isRecording,
        //   "silenceTimeoutRef:",
        //   silenceTimeoutRef.current
        // );
        if (!silenceTimeoutRef.current) {
          console.log("Setting silence timeout");
          silenceTimeoutRef.current = setTimeout(() => {
            console.log("Stopping recording due to silence");
            stopRecording();
            setVoice_detected(false);

            console.log("stopped recording");
            setIsRecording(false);
            silenceTimeoutRef.current = null; // Clear the timeout reference
          }, silenceDuration);
        }
      }

      animationFrameRef.current = requestAnimationFrame(checkAudioLevel);
    };

    checkAudioLevel();
  };

  useEffect(() => {
    if (voice_detected === true) {
      startRecording();
    }
  }, [voice_detected]);

  const startRecording = async () => {
    console.log("startRecording", isRecording);
    // if (!isRecording) return;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          noiseSuppression: true, // Reduces background noise
          echoCancellation: true, // Cancels echo
          autoGainControl: true, // Adjusts volume automatically
        },
      });
      mediaRecorderRef.current = new MediaRecorder(stream);
      // if (isRecording)
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

      // Set recording state before starting
      setIsRecording(true);
      audioChunksRef.current = [];

      mediaRecorderRef.current.start(200);
      websocketRef.current.emit("start");
      console.log("Recording started successfully, isRecording:", isRecording);

      mediaRecorderRef.current.onstop = () => {
        setIsRecording(false);
        websocketRef.current.emit("stop", {
          type: "interview",
        });
        console.log("Recording stopped, isRecording:", false);
      };
    } catch (error) {
      console.error("Error starting recording:", error);
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    // if (!isRecording) return;

    console.log("SSSSSSSSSSSSSSSSSSSSSSS recording...");

    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream
        .getTracks()
        .forEach((track) => track.stop());
      mediaRecorderRef.current = null;
    }

    // Clear the silence timeout
    if (silenceTimeoutRef.current) {
      clearTimeout(silenceTimeoutRef.current);
      silenceTimeoutRef.current = null;
    }

    setIsRecording(false);
    console.log("Recording stopped successfully");
  };

  useEffect(() => {
    console.log("Speakers updated:", speakers);
  }, [speakers]);
  useEffect(() => {
    const playAudio = () => {
      if (currentIndex < audiourls.length) {
        const audioUrlWithTimestamp = `${
          audiourls[currentIndex]
        }?t=${new Date().getTime()}`;
        const audio = new Audio(audioUrlWithTimestamp);

        const urlstring = audiourls[currentIndex];
        const match = urlstring.match(/audios\/(\d+)\.mp3/);
        const result = parseInt(match[1]);
        console.log("assuming its a index", result, typeof result); // Output: 0

        // toggleSpeaking(user.id)
        audio.play(toggleSpeaking(result)).catch((error) => {
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

    if (isPlaying && audiourls.length > 0) {
      playAudio();
    }
  }, [currentIndex, isPlaying, audiourls]);

  const updateSpeakers = () => {
    setSpeakers((prevSpeakers) =>
      prevSpeakers.map((interviewer) => ({
        ...interviewer,
        isSpeaking: false,
      }))
    );
  };
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
    console.log("Button clicked, isRecording", isRecording);
    if (isRecording) {
      stopRecording();
      // setIsRecording(false);
    } else {
      startRecording();
    }
  };

  useEffect(() => {
    return () => {
      // Cleanup WebSocket
      if (websocketRef.current) {
        websocketRef.current.disconnect();
      }

      // Stop recording if active and release resources
      if (mediaRecorderRef.current) {
        stopRecording();
      }

      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (silenceTimeoutRef.current) {
        clearTimeout(silenceTimeoutRef.current);
      }
      if (audioContext) {
        audioContext.close();
      }
    };
  }, []);

  return (
    <BackgroundGradientAnimation>
      <div className="relative z-50">
        {firstLoad && (
          <div className="flex items-center justify-center text-3xl pt-24 font-bold">
            You can say <h1 className="italic">&quot;Lets get started&quot;</h1>
          </div>
        )}

        <div className="flex flex-col items-center justify-center h-screen w-full">
          <div className="flex  flex-row items-center justify-center">
            {speakers.length > 0 ? (
              speakers.map((user, index) => (
                <div
                  key={user.id}
                  className={`m-16  animate-slide-in-up opacity-100 delay-${
                    index * 100
                  }`}
                >
                  {user.isSpeaking ? (
                    <PinContainer title={user.message}>
                      <Interviewercard
                        isSpeaking={user.isSpeaking}
                        userName={user.interviewer_name}
                        imageLink={
                          "https://static.vecteezy.com/system/resources/previews/008/332/204/non_2x/3d-young-smiling-man-with-dark-sin-tone-and-black-hair-people-cartoon-cute-minimal-character-style-illustration-user-avatar-in-round-frame-isolated-on-white-background-vector.jpg"
                        }
                      />{" "}
                    </PinContainer>
                  ) : (
                    <Interviewercard
                      isSpeaking={user.isSpeaking}
                      userName={user.interviewer_name}
                      imageLink={
                        "https://static.vecteezy.com/system/resources/previews/008/332/204/non_2x/3d-young-smiling-man-with-dark-sin-tone-and-black-hair-people-cartoon-cute-minimal-character-style-illustration-user-avatar-in-round-frame-isolated-on-white-background-vector.jpg"
                      }
                    />
                  )}
                </div>
              ))
            ) : (
              <div className="animate-fade-out opacity-100">
                <Interviewercard />
              </div>
            )}
          </div>
          {/* <Interviewercard isSpeaking={true}></Interviewercard> */}

          <div className="w-full relative">
            {/* {(isRecording || reply) && (
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
            )} */}

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
            <a
              href="http://127.0.0.1:5000/generatereport"
              // onClick={() => router.push("/generate")}

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
            </a>

            {/* {speakers.length > 0 ? (
              speakers.map((user) => (
                <UserCard
                  key={user.id}
                  isSpeaking={user.isSpeaking}
                  userName={user.interviewer_name}
                ></UserCard>
              ))
            ) : (
              <UserCard></UserCard>
            )} */}
            {/* <div className="user-cards-container flex gap-4">
              {speakers.length > 0 ? (
                speakers.map((user, index) => (
                  <div
                    key={user.id}
                    className={`animate-slide-in-up opacity-100 delay-${
                      index * 100
                    }`}
                  >
                    <UserCard
                      isSpeaking={user.isSpeaking}
                      userName={user.interviewer_name}
                    />
                  </div>
                ))
              ) : (
                <div className="animate-fade-out opacity-100">
                  <UserCard />
                </div>
              )}
            </div> */}
          </div>
        </div>
      </div>
    </BackgroundGradientAnimation>
  );
}
