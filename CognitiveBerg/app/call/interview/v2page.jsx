"use client";
import { useEffect, useRef, useState } from "react";
import { BackgroundGradientAnimation } from "/components/ui/background-gradient-animation";

export default function MicrophoneComponent() {
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const audioStreamRef = useRef(null);
  const recordingTimeoutRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = async () => {
    // Prevent starting a new recording while the current one is active
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      console.warn("MediaRecorder is already recording");
      return;
    }

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
            console.log("Sending audio chunk");
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
    setIsRecording(false);
    mediaRecorderRef.current.stop();
    console.log("Recording stopped");
  };

  const monitorAudio = (stream) => {
    if (!audioContextRef.current) {
      audioContextRef.current = new AudioContext();
    }

    const audioContext = audioContextRef.current;
    const source = audioContext.createMediaStreamSource(stream);

    if (!analyserRef.current) {
      analyserRef.current = audioContext.createAnalyser();
    }

    const analyser = analyserRef.current;
    source.connect(analyser);

    const data = new Uint8Array(analyser.fftSize);

    const checkAudioLevel = () => {
      analyser.getByteFrequencyData(data);
      const volume = data.reduce((sum, value) => sum + value) / data.length;

      if (volume > 30) {
        // Noise threshold for starting recording
        if (!isRecording) {
          console.log("Voice detected. Starting recording...");
          startRecording();
        }
        if (recordingTimeoutRef.current) {
          clearTimeout(recordingTimeoutRef.current);
        }
      } else if (isRecording) {
        // Stop recording after 2 seconds of silence
        if (!recordingTimeoutRef.current) {
          recordingTimeoutRef.current = setTimeout(() => {
            console.log("Silence detected. Stopping recording...");
            stopRecording();
          }, 2000); // 2 seconds
        }
      }

      requestAnimationFrame(checkAudioLevel);
    };

    checkAudioLevel();
  };

  useEffect(() => {
    const setupMicrophone = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        audioStreamRef.current = stream;

        mediaRecorderRef.current = new MediaRecorder(stream);
        mediaRecorderRef.current.ondataavailable = (event) => {
          // Process or send audio chunks as needed
          if (event.data.size > 0) {
            console.log("Audio chunk recorded", event.data);
          }
        };

        monitorAudio(stream);
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    };

    setupMicrophone();

    return () => {
      if (audioStreamRef.current) {
        audioStreamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (recordingTimeoutRef.current) {
        clearTimeout(recordingTimeoutRef.current);
      }
    };
  }, []);

  return (
    <BackgroundGradientAnimation>
      <div className="relative z-50 flex flex-col items-center justify-center h-screen w-full">
        <h1 className="text-2xl font-bold">Voice-Activated Recording</h1>
        <div className="mt-10 text-lg">
          {isRecording ? (
            <p className="text-green-500">Recording...</p>
          ) : (
            <p className="text-red-500">Listening for voice...</p>
          )}
        </div>
      </div>
    </BackgroundGradientAnimation>
  );
}
