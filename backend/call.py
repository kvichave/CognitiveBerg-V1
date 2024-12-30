from flask import Blueprint, request, jsonify, session,send_from_directory
import os
import google.generativeai as genai
import json
import asyncio
from dotenv import load_dotenv
import environ
load_dotenv()

import audio_controller
# Configure the Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create a blueprint for user-related routes
call = Blueprint('call', __name__)
AUDIO_FOLDER = 'AUDIOS'

# Set the directory to save audio files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define the path for the JSON file to store conversation history
HISTORY_FILE_PATH = 'duplicate_session_data.json'


def load_history():
    """Load conversation history from a JSON file."""
    if os.path.exists(HISTORY_FILE_PATH):
        with open(HISTORY_FILE_PATH, 'r') as f:
            return json.load(f)
    return []  # Return an empty list if the file does not exist

def save_history(history):
    """Save conversation history to a JSON file."""
    with open(HISTORY_FILE_PATH, 'w') as f:
        json.dump(history, f, indent=4)

@call.route('/send_audio', methods=['POST'])
async def send_audio():
    # Check if the audio file is provided
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, "recorded_audio.mp3")
    
    # Save the audio file
    audio_file.save(file_path)

    # Transcribe the audio file
    user_reply = transcribe(file_path)
    
    # Add the transcription to the conversation history and generate a response
    bot_reply = generate(user_reply)
    print("bot_reply::::::::::::: ",bot_reply)
    # print("type::::::::::::: ",type(bot_reply))


    json_data = json.loads(bot_reply)
    # reply_list=await((json_data))   
    if type(json_data) == dict:
        json_data = [json_data]
    print("json_data::::::::::::: ",json_data)
    # Run speakers in the background without blocking the current loop
    reply_list = await audio_controller.speakers(json_data)

    # Wait for the result (non-blocking)
    print("reply_list:::::::::::: ",reply_list)
    audio_urls = [f'http://127.0.0.1:5000/audio/{file.split("/")[-1]}' for file in reply_list]
    # return jsonify(audio_urls)

    return jsonify({"message": "Audio received and transcribed successfully!", "user_reply": user_reply, "bot_reply": bot_reply, "audio_urls": audio_urls}), 200

def transcribe(file_path):
    """Transcribe the uploaded audio file using Gemini."""
    # Upload the file to Gemini
    myfile = genai.upload_file(file_path)
    
    # Generate the transcription
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
    result = model.generate_content([myfile, "Transcribe this audio clip, provide only plain text response"])
    
    # Return the transcription
    return result.text

def generate(user_reply):
    """Generate a bot response using the Gemini model based on user reply and conversation history."""
    
    # Load conversation history from JSON file
    history = load_history()
    
    # Add the user's transcription to the conversation history
    history.append({
        "role": "user",
        "parts": [user_reply]
    })
    
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-8b",
        generation_config=generation_config,
    )
    print("11111111111111111111")
    # Start the chat session with the current conversation history
    chat_session = model.start_chat(
        history=history
    )
    print("222222222222222222222222222")

    # Send the user transcription to the AI model for a response
    response = chat_session.send_message(user_reply)
    print("33333333333333333333333333333333333")
    # Append the AI's reply to the conversation history
    history.append({
        "role": "model",
        "parts": [response.text]
    })

    # Save the updated history back to the JSON file
    save_history(history)

    # Return the AI's reply
    print("response.text::::::::::::: ",response.text)
    return response.text


@call.route('/audio/<path:filename>', methods=['GET'])
def serve_audio(filename):
    # Serve audio files from the AUDIOS directory
    return send_from_directory(AUDIO_FOLDER, filename)


@call.route('/clearData', methods=['POST','GET'])
def create_json():
    
    with open("session_data.json", 'r') as f:
            data= json.load(f)
    with open(HISTORY_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)
    return {"message": "Data cleared successfully"}


@call.route('/report', methods=['POST','GET'])
def generateRoport():
    with open(HISTORY_FILE_PATH, 'r') as f:
            data= json.load(f)
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    )

    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            "I will provide a Json to you, It contains the conversation between Model and user, You have to generate a extreamly detailed report of their mistakes and also score them widely , point there mistakes from the conversation to give examples\nformat \n{ \"Interview Report\": {role,Scenario}\n  \"fluency\": \"7.5\",\n  \"mistakes\": [ explain in detail],\n  \"scores\": { explain in detail\n    \"clarity\": 8,\n    \"confidence\": 7,\n    \"accuracy\": 6\n  },\n  \"visualization_data\": {\n    \"line_chart_fluency\": [\n      { \"response\": 1, \"fluency_score\": 6 },\n      { \"response\": 2, \"fluency_score\": 7 },\n      ...\n    ],\n    \"bar_chart_mistakes\": {\n      \"tenses\": 5,\n      \"word_usage\": 3,\n      \"sentence_structure\": 4\n    },\n    \"pie_chart_communication_clarity\": {\n      \"clarity_score\": 8,\n      \"communication_score\": 7\n    }\n  },\n  \"suggested_improvements\": [\"mprove sentence structure and choice of words.\"],\n  \"benchmark_comparison\": {\n    \"average_fluency\",\n    \"average_clarity\",\n    \"average_accuracy\"\n  },\n  \"summary\": \"The candidate shows strong clarity and communication skills but could improve in sentence structure and word choice to achieve greater accuracy.\"\n}",
        ],
        },
        {
        "role": "model",
        "parts": [
            "```json\n{\"Interview Report\": {\"role\": \"Model\", \"Scenario\": \"Conversation between Model and user\"}, \"fluency\": \"7.5\", \"mistakes\": [\"The candidate displayed minor grammatical errors in some responses, particularly in tense usage. For example, in response 3, the candidate used the past tense instead of the present tense, leading to a slightly confusing sentence structure.  \", \"There were a few instances where the candidate could have used more precise vocabulary to express their thoughts more effectively. In response 5, for instance, the word 'stuff' could have been replaced with a more specific and descriptive term, improving the overall clarity of the message.\", \"While the candidate generally provided relevant information, some responses lacked sufficient detail and could have been expanded upon to provide a more comprehensive answer. For example, in response 7, the candidate could have offered more specific examples to illustrate their point.\"], \"scores\": {\"clarity\": 8, \"confidence\": 7, \"accuracy\": 6}, \"visualization_data\": {\"line_chart_fluency\": [{\"response\": 1, \"fluency_score\": 6}, {\"response\": 2, \"fluency_score\": 7}, {\"response\": 3, \"fluency_score\": 8}, {\"response\": 4, \"fluency_score\": 7}, {\"response\": 5, \"fluency_score\": 6}, {\"response\": 6, \"fluency_score\": 8}, {\"response\": 7, \"fluency_score\": 7}], \"bar_chart_mistakes\": {\"tenses\": 5, \"word_usage\": 3, \"sentence_structure\": 4}, \"pie_chart_communication_clarity\": {\"clarity_score\": 8, \"communication_score\": 7}}, \"suggested_improvements\": [\"Improve sentence structure and choice of words.\", \"Pay attention to verb tense consistency.\", \"Provide more detailed and specific explanations.\"], \"benchmark_comparison\": {\"average_fluency\": \"7.2\", \"average_clarity\": \"7.8\", \"average_accuracy\": \"6.5\"}, \"summary\": \"The candidate demonstrates strong clarity and communication skills, but could benefit from improving sentence structure, word choice, and providing more detailed responses for increased accuracy.  Overall, they performed well in this conversation, showcasing good understanding and fluency.\"}\n\n```",
        ],
        },
    ]
    )

    response = chat_session.send_message(str(data))

    # print(response.text)
    # json_data = json.loads(response.text)
    
    # # Print formatted JSON
    # formatted_json = json.dumps(json_data, indent=4)
    # print(formatted_json)
# Print the formatted JSON
    print(response.text)
    return{"message": response.text}