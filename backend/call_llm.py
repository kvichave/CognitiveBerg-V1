from flask import Flask,send_from_directory,Blueprint,g,session,request
from flask_socketio import SocketIO
from flask_cors import CORS
import os
import asyncio
from llms_module import App
from llms_module import gemini_class
from chat_CRUD import add_data
import dashboard_features
from user_profile import get_user


call_LLm=Blueprint('call_LLm',__name__)

socketio = SocketIO(cors_allowed_origins="*")  # Use async mode for Flask-SocketIO

audio_file = None
objectApp = App()
GEMINIobj=gemini_class()
#Global variable for storing the user code
user_code = ""

saved_prompt=None
wav_file_path = "received_audio/recording.wav"

# Global variable for storing image chunks
image_chunks_data = []

@socketio.on("start")
def handle_start():
    global audio_file
    os.makedirs(os.path.dirname(wav_file_path), exist_ok=True)
    audio_file = open(wav_file_path, "wb")
    # print("Started recording and file opened.")

@socketio.on("audio_chunk")
def handle_audio_chunk(audio_data):
    # print("receiving")

    global audio_file
    if audio_file:
        # print(f"Received chunk of size: {len(audio_data)} bytes")
        audio_file.write(audio_data)
img_counter=1
@socketio.on('screen_capture')
def handle_image_chunk(data):
    image_data = data
    global img_counter
    if img_counter<3:
        image_path = f'received_img/screenshot{img_counter}.jpg'
        if img_counter==2:
            img_counter=1
        else:
            img_counter+=1

    # else:
    #     img_counter=1
    if isinstance(data, dict):
        image_data = data.get('image', '')
    
    # Remove data URL prefix if present
    if 'base64,' in image_data:
        base64_data = image_data.split('base64,')[1]
    else:
        base64_data = image_data
        
    # Decode and save image
    import base64
    image_bytes = base64.b64decode(base64_data)
    
    with open(image_path, 'wb') as f:
        f.write(image_bytes)
        
    # print(f"Screenshot saved: {image_path}")
    return {"success": True, "path": image_path}

# def save_image(base64_image):
#     import base64

#     # Remove "data:image/png;base64," prefix
#     base64_image = base64_image.split(",")[1]

#     with open("captured_image.png", "wb") as f:
#         f.write(base64.b64decode(base64_image))
#         print("Image saved as 'captured_image.png'")

def remove_image_url(message):
    for item in message:
        if item["role"] == "user" and isinstance(item["content"], list):
            # Filter out the dictionary with "type": "image_url"
            item["content"] = [content for content in item["content"] if content.get("type") != "image_url"]
    return message
@socketio.on("stop")
def on_stop(data):

    # print("flask Stopping recording...  ",data.get("type"))
    cursor=dict(get_user(session.get("user_id")))
    objectApp.userDetails=cursor
    print(objectApp.userDetails)
    
    # print("IMAGEEEE...  ",data.get("image"))
    global audio_file
    try:
        # print("user id from stop:",session.get("user_id"))

        if audio_file:
            audio_file.close()
            # print(f"Recording stopped and saved at {wav_file_path}")
            
            # Await the async method call

            if data.get("type") == "interview":
                session["Mtype"]="interview"    
                whisper_object=objectApp.groq_whisper(wav_file_path, add_to_history=True,cursor=cursor)
                print("from call_llm.py",objectApp.userDetails)
                # print("from prompt   ::::::::: call_llm.py",objectApp.prompt)
                # print("prompt::::",objectApp.prompt)
                if whisper_object=="reset":
                    if audio_file:
                        audio_file.close()
                        # print("File closed due to client disconnect.")
                        audio_file = None
                    handle_start()
                objectApp.usercode=None
                audio_urls = [f'http://127.0.0.1:5000/audios/{file.split("/")[-1]}' for file in objectApp.outputPaths]
                interviewers=objectApp.LLM_reply
                if interviewers =="END":
                    saved_prompt=objectApp.prompt[1:]
                    if len(saved_prompt) is not 0:
                        # print("Analytics saved for bmeeting")
                        id=add_data(saved_prompt,session["Mtype"])
                        print(str(id))
                        session["saved_prompt_interview"] = saved_prompt
                        analytics=dashboard_features.create_analytics(session["saved_prompt_interview"])
                        print("Analytics saved for interview:::::::::::::::::::")
                        dashboard_features.save_analytics(data=analytics, usertype="per_interview_analytics",save="daily_analylsis",conversationID=str(id))
                        print("Analytics saved for interview")


                        
                    socketio.emit("interview_end", {"message": "Interview ended"})
                    # here the analytics function can be called

            
            # Access output paths generated by App
                # print("Generated audio paths:", audio_urls)
                socketio.emit("audio_urls", {"files": audio_urls,"interviewers":interviewers})

            elif data.get("type") == "bmeeting":
                session["Mtype"]="bmeeting"    

                GEMINIobj.groq_whisper(input=wav_file_path,cursor=cursor,image=True)
                audio_urls = [f'http://127.0.0.1:5000/audios/{file.split("/")[-1]}' for file in GEMINIobj.outputPaths]
                investors=GEMINIobj.LLM_reply
                if investors =="END":
                    try:
                        saved_prompt=GEMINIobj.history[1:]
                        saved_prompt=remove_image_url(saved_prompt)

                        id=add_data(saved_prompt,session["Mtype"])
                        # print("saved prompt",saved_prompt)

                        session["saved_prompt_bmeeting"] = saved_prompt
                        analytics=dashboard_features.create_analytics(session["saved_prompt_bmeeting"])
                        dashboard_features.save_analytics(data=analytics, usertype="per_bmeeting_analytics",save="daily_analylsis",conversationID=str(id))
                    except Exception as e:
                        print(e)
                    finally:
                        socketio.emit("meeting_end", {"message": "meeting ended"})
                # print("Generated audio paths:", audio_urls)
                socketio.emit("audio_urls", {"files": audio_urls,"investors":investors})
    
    except Exception as e:
        print(f"Error during transcription: {e}")
    finally:
        audio_file = None  # Reset the file reference


@call_LLm.route('/audios/<path:filename>',methods=['GET'])
def serve_audio(filename):
    # print("filename::::::",filename)
    return send_from_directory('AUDIOS', filename)

@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("message")
def handle_message():
    print("IN MESSAGE")

@socketio.on("disconnect")
def handle_disconnect():
    global audio_file
    global objectApp


    objectApp.clear_prompt()
    GEMINIobj.clear_prompt()
    if audio_file:
        audio_file.close()
        # print("File closed due to client disconnect.")
        audio_file = None
    print("Client disconnected")



@call_LLm.route("/getcode",methods=['POST'])
def acceptCode():
    data = request.get_json()
    language = data.get("language")
    code = data.get("code")
    print("Language: ",language)
    print("Code: ",code)
    global user_code
    user_code = "LANGUAGE: "+language+"\nCODE: "+code
    objectApp.usercode=user_code
    

    return ({"submitted":True}) 






