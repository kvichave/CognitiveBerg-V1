import os
import wave
import pyaudio
from faster_whisper import WhisperModel

# Define colors for terminal output
NEON_GREEN = "\033[92m"
RESET_COLOR = "\033[0m"

def record_chunk(p, stream, file_path, chunk_length=1):
    """
    Records a chunk of audio and saves it to the specified file.

    :param p: PyAudio object
    :param stream: PyAudio stream object
    :param file_path: Path to save the recorded audio
    :param chunk_length: Length of the audio chunk in seconds
    """
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_chunk(model, file_path):
    """
    Transcribes the given audio file using the Whisper model.

    :param model: WhisperModel object
    :param file_path: Path to the audio file to transcribe
    :return: Transcription of the audio file
    """
    segments, _ = model.transcribe(file_path)
    return ''.join(segment.text for segment in segments)

def main2():
    """
    Main function to record audio in chunks, transcribe it, and accumulate the transcription.
    """
    model_size = "base.en"
    model = WhisperModel(model_size,  compute_type="float32")

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    accumulated_transcription = ""  # Initialize an empty string to accumulate transcriptions

    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file)
            transcription = transcribe_chunk(model, chunk_file)

            print(NEON_GREEN + transcription + RESET_COLOR)
            print()
            # os.remove(chunk_file)

            # Append the new transcription to the accumulated transcription
            accumulated_transcription += transcription + " "

    except KeyboardInterrupt:
        print("Stopping...")

        # Write the accumulated transcription to the log file
        with open("log.txt", "w") as log_file:
            log_file.write(accumulated_transcription)

    finally:
        print("LOG:" + accumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main2()
