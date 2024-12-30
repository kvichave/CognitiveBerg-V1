import os
import json
from datetime import datetime  # Import the datetime module

# Function to save chat history
def save_chat(user_id, new_chat):
    chat_file_path = f"/home/kunal/Documents/CognitiveBerg/USERDATA/{user_id}_chats.json"  # Chat file name

    # Check if the chat file exists
    if os.path.exists(chat_file_path):
        # If file exists, read the existing data
        with open(chat_file_path, 'r') as file:
            try:
                chat_data = json.load(file)
            except json.JSONDecodeError:
                chat_data = []  # Start with an empty list if there's an error
    else:
        # If the file doesn't exist, start with an empty list
        chat_data = []

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append new chat data with timestamp
    chat_data.append({
        "message": new_chat,
        "timestamp": timestamp  # Add the current timestamp
    })

    # Write the updated data back to the file
    with open(chat_file_path, 'w') as file:
        json.dump(chat_data, file, indent=4)  # Indent for readability

    # print(f"Chat saved for user {user_id} with timestamp {timestamp}")
    return chat_data


# Function to get chat history
def get_chat(user_id):
    chat_file_path = f"/home/kunal/Documents/CognitiveBerg/USERDATA/{user_id}_chats.json"  # Chat file name

    # Check if the file exists
    if os.path.exists(chat_file_path):
        # If file exists, read the existing data
        with open(chat_file_path, 'r') as file:
            try:
                chat_data = json.load(file)
            except json.JSONDecodeError:
                chat_data = []  # Start with an empty list if there's an error
    else:
        # If the file doesn't exist, start with an empty list
        chat_data = []

    return chat_data


# Function to save user data
def save_user_data(user_id, user_data):
    user_data_file_path = f"/home/kunal/Documents/CognitiveBerg/USERDATA/{user_id}_data.json"  # User data file name

    # Check if the user data file exists
    if os.path.exists(user_data_file_path):
        # If file exists, read the existing data
        with open(user_data_file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}  # Start with an empty dict if there's an error
    else:
        # If the file doesn't exist, start with an empty dict
        data = {}

    # Update the user data
    data.update(user_data)

    # Write the updated data back to the file
    with open(user_data_file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Indent for readability

    print(f"User data saved for user {user_id}")
    return data


# Function to get user data
def get_user_data(user_id):
    user_data_file_path = f"/home/kunal/Documents/CognitiveBerg/USERDATA/{user_id}_data.json"  # User data file name

    # Check if the file exists
    if os.path.exists(user_data_file_path):
        # If file exists, read the existing data
        with open(user_data_file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}  # Start with an empty dict if there's an error
    else:
        # If the file doesn't exist, start with an empty dict
        
        data = {}

    return data
