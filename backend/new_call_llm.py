from flask import Flask, send_from_directory, Blueprint, g, session
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import asyncio
import time
import json
from deepgram import Deepgram
from llms_module import App
from llms_module import gemini_class
import eventlet
eventlet.monkey_patch() 
# import logging
# logging.basicConfig(level=logging.DEBUG)
# Initialize Deepgram
DEEPGRAM_API_KEY = '65ca2172b0a49754082f4379ba8ae2788d51b913'
dg_client = Deepgram(DEEPGRAM_API_KEY)

call_LLm = Blueprint('call_LLm', __name__)
socketio = SocketIO(cors_allowed_origins="*")

# Audio processing globals
audio_file = None
objectApp = App()
GEMINIobj = gemini_class()
saved_prompt = None
wav_file_path = "received_audio/recording.wav"
img_counter = 1

# Deepgram-related globals
live_transcription = None
silence_threshold = 1.5  # Seconds of silence to trigger processing
last_speech_time = None
processing_lock = asyncio.Lock()

# Image handling
image_chunks_data = []

async def connect_to_deepgram():
    global live_transcription
    try:
        print("Attempting Deepgram connection...")
        live_transcription = await dg_client.transcription.live({
            'smart_format': True,
            'interim_results': True,
            'punctuate': True,
            'endpointing': True,
            'vad_events': True,
            'encoding': 'linear16',
            'sample_rate': 16000,
        })
        
        if live_transcription:
            print("Deepgram connection established successfully!")
        else:
            print("Deepgram connection failed to initialize!")

        live_transcription.registerHandler(live_transcription.event.CLOSE, 
            lambda _: print('Deepgram connection closed'))
        live_transcription.registerHandler(live_transcription.event.TRANSCRIPT_RECEIVED, 
            process_transcript)

    except Exception as e:
        print(f'Deepgram connection failed: {e}')


async def process_transcript(transcript):
    global last_speech_time
    try:
        print(f"Raw transcript data: {transcript}")
        data = json.loads(transcript)

        if 'channel' in data and 'alternatives' in data['channel']:
            text = data['channel']['alternatives'][0]['transcript']
            if text.strip():
                last_speech_time = time.time()
                print(f"Interim transcript: {text}")

            if 'vad' in data and data['vad']['event'] == 'silence':
                print("Silence detected, checking for completion...")
                await check_silence()

    except Exception as e:
        print(f'Error processing transcript: {e}')


async def check_silence():
    global last_speech_time, processing_lock
    async with processing_lock:
        current_time = time.time()
        # logging.debug("Last speech: %s, Current time: %s, Difference: %s", 
        #              last_speech_time, current_time, 
        #              current_time - last_speech_time if last_speech_time else None)
        
        if last_speech_time and (current_time - last_speech_time) > silence_threshold:
            print("Triggering audio processing")
            await send_to_model()
            last_speech_time = None

async def send_to_model():
    global audio_file
    try:
        if audio_file:
            audio_file.close()
            print(f"Processing audio from {wav_file_path}")
            
            # Your existing processing logic
            if session.get("type") == "interview":
                await objectApp.groq_whisper(wav_file_path, add_to_history=True)
                audio_urls = [f'http://127.0.0.1:5000/audios/{file.split("/")[-1]}' 
                            for file in objectApp.outputPaths]
                interviewers = objectApp.LLM_reply
                if interviewers == "END":
                    socketio.emit("interview_end", {"message": "Interview ended"})
                socketio.emit("audio_urls", {"files": audio_urls, "interviewers": interviewers})

            elif session.get("type") == "bmeeting":
                await GEMINIobj.groq_whisper(input=wav_file_path, image=True)
                audio_urls = [f'http://127.0.0.1:5000/audios/{file.split("/")[-1]}' 
                            for file in GEMINIobj.outputPaths]
                interviewers = GEMINIobj.LLM_reply
                if interviewers == "END":
                    socketio.emit("interview_end", {"message": "Interview ended"})
                socketio.emit("audio_urls", {"files": audio_urls, "interviewers": interviewers})

            # Reset audio file
            audio_file = open(wav_file_path, "wb")
            
    except Exception as e:
        print(f"Error processing audio: {e}")
    finally:
        processing_lock.release()

@socketio.on("start")
def handle_start(data=None):  # Add default value for data
    global audio_file
    if data:
        session["type"] = data.get("type", "interview")
    os.makedirs(os.path.dirname(wav_file_path), exist_ok=True)
    audio_file = open(wav_file_path, "wb")
    print(f"Started recording for {session.get('type', 'interview')}")


@socketio.on("audio_chunk")
def handle_audio_chunk(audio_data):
    global audio_file, live_transcription
    if audio_file:
        audio_file.write(audio_data)
        audio_file.flush()
        print(f"Received audio chunk size: {len(audio_data)} bytes")

    if live_transcription:
        try:
            if live_transcription.state == 'connected':
                print("Sending audio to Deepgram...")
                live_transcription.send(audio_data)
            else:
                print("Deepgram is not connected! Reconnecting...")
                socketio.start_background_task(connect_to_deepgram)
        except Exception as e:
            print(f'Error sending audio to Deepgram: {e}')


@socketio.on('screen_capture')
def handle_image_chunk(data):
    global img_counter
    try:
        import base64
        
        # Initialize image_data properly
        if isinstance(data, dict):
            image_data = data.get('image', '')
        else:
            image_data = data  # Handle non-dictionary format

        # Validate image data exists
        if not image_data:
            raise ValueError("Empty image data received")

        # Handle base64 prefix
        if 'base64,' in image_data:
            base64_data = image_data.split('base64,')[1]
        else:
            base64_data = image_data

        # Generate alternating filenames
        image_path = f'received_img/screenshot{img_counter % 2 + 1}.jpg'
        img_counter += 1

        # Decode and save
        image_bytes = base64.b64decode(base64_data)
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        print(f"Screenshot saved: {image_path}")
        return {"success": True, "path": image_path}

    except Exception as e:
        print(f"Error saving image: {e}")
        return {"success": False, "error": str(e)}
    

@socketio.on("connect")
def handle_connect():
    print("Client connected")
    
    async def connect_wrapper():
        try:
            await connect_to_deepgram()
        except Exception as e:
            print(f"Connection error: {e}")
            
    # Start the coroutine properly
    socketio.start_background_task(connect_wrapper)
    print(f"Connection errorrrr")


@socketio.on("disconnect")
def handle_disconnect():
    global audio_file, live_transcription, objectApp, saved_prompt
    if live_transcription:
        live_transcription.finish()
    
    if audio_file:
        audio_file.close()
        audio_file = None
        
    saved_prompt = objectApp.prompt[1:]
    session["saved_prompt"] = saved_prompt
    objectApp.clear_prompt()
    print("Client disconnected")

# Existing routes
@call_LLm.route('/audios/<path:filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory('AUDIOS', filename)

@call_LLm.route("/wow", methods=['GET'])
def wow():
    obj = gemini_class()
    obj.groq_whisper(input="received_audio/recording.wav", image="second.png")
    return "Processing initiated"

@call_LLm.route('/generatereport', methods=['GET'])
def new():
    print("The saved prompt is:", session.get("saved_prompt"))
    return "Report generation initiated"


@call_LLm.route('/trigger-manual', methods=['GET'])
def manual_trigger():
    socketio.start_background_task(send_to_model)
    return "Manual processing triggered"