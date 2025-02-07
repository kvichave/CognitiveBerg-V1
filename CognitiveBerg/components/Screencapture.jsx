import React, {
  useState,
  useRef,
  forwardRef,
  useImperativeHandle,
  useEffect,
} from "react";

const ScreenCaptureWithPreview = forwardRef((_, ref) => {
  const [stream, setStream] = useState(null);
  const [track, setTrack] = useState(null);
  const [screenshot, setScreenshot] = useState(null);
  const videoRef = useRef(null);

  const startScreenCapture = async () => {
    try {
      const screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
      });
      const videoTrack = screenStream.getVideoTracks()[0];

      setStream(screenStream);
      setTrack(videoTrack);

      if (videoRef.current) {
        videoRef.current.srcObject = screenStream;
      }

      console.log("Screen capture started!");
    } catch (err) {
      console.error("Error starting screen capture:", err);
    }
  };

  const captureScreen = async () => {
    if (!track) {
      console.error("No active screen capture track.");
      return;
    }

    try {
      const imageCapture = new ImageCapture(track);
      const bitmap = await imageCapture.grabFrame();

      // Convert bitmap to canvas
      const canvas = document.createElement("canvas");
      canvas.width = bitmap.width;
      canvas.height = bitmap.height;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(bitmap, 0, 0, canvas.width, canvas.height);

      // Convert canvas to base64 image
      const imageData = canvas.toDataURL("image/png");
      setScreenshot(imageData);

      console.log("Screenshot captured successfully!");
      return imageData;
    } catch (err) {
      console.error("Error capturing screen:", err);
    }
  };

  const stopScreenCapture = () => {
    if (track) {
      track.stop();
      setStream(null);
      setTrack(null);

      if (videoRef.current) {
        videoRef.current.srcObject = null;
      }

      console.log("Screen capture stopped!");
    }
  };
  useImperativeHandle(ref, () => ({
    startScreenCapture,
    captureScreen,
    stopScreenCapture,
  }));

  return (
    <div style={{ fontFamily: "Arial, sans-serif", margin: "20px" }}>
      <h1>Screen Capture with Preview</h1>
      <button onClick={startScreenCapture} disabled={!!stream}>
        Start Screen Capture
      </button>
      <button onClick={captureScreen} disabled={!track}>
        Capture Screenshot
      </button>
      <button onClick={stopScreenCapture} disabled={!track}>
        Stop Screen Capture
      </button>

      <div style={{ marginTop: "20px" }}>
        <h3>Live Preview:</h3>
        <video
          ref={videoRef}
          autoPlay
          muted
          style={{ maxWidth: "100%", border: "1px solid #ccc" }}
        ></video>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Screenshot:</h3>
        {screenshot && (
          <img
            src={screenshot}
            alt="Captured Screenshot"
            style={{ maxWidth: "100%", border: "1px solid #ccc" }}
          />
        )}
      </div>
    </div>
  );
});

export default ScreenCaptureWithPreview;
