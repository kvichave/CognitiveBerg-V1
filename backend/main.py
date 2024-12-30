from flask import Flask, request, session
from flask_session import Session
from flask_cors import CORS
import json
from call import call

app = Flask(__name__)

CORS(app, supports_credentials=True)
app.secret_key = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
app.config['SESSION_TYPE'] = 'filesystem'  # Or another valid session type
Session(app)
app.register_blueprint(call)

@app.route('/user_profile', methods=['POST', 'GET'])
def profile():
    data = request.get_json()
    json_file_path = 'session_data.json'
    json_file_path_duplicate = 'duplicate_session_data.json'
    history=[
        {
        "role": "user",
        "parts": [
            "You are the interviewers conducting an interview for a fresher backend developer position. Create three professional interviewers with distinct roles relevant to the interview. Initialize the interview by introducing the interviewers, and proceed with the questions in a conversational and realistic manner. Start with an introduction of all interviewers for software developer the interviewers were like=  [\n{\n\"interviewer_name\": \"Rajesh Sharma, Engineering Manager\",\n\"message\": \"Hello everyone, I'm Rajesh Sharma, the Engineering Manager for the backend team. I'll be leading this interview today.\",\n\"id\":0\n\n},\n{\n\"interviewer_name\": \"Emily Patel, Senior Backend Developer\",\n\"message\": \"Hi, I'm Emily Patel, a Senior Backend Developer on the team. I'll be evaluating your technical skills and experience.\",\n\"id\":1\n},\n{\n\"interviewer_name\": \"David Lee, Technical Recruiter\",\n\"message\": \"Hello, I'm David Lee, the Technical Recruiter who worked with you to schedule this interview. I'll be taking notes and ensuring the process runs smoothly. Are You comfortable with the interview?\",\n\"id\":2\n},\n]\n\nfor english teacher role=\n[\n    {\n        \"interviewer_name\": \"Rajesh Sharma, English Teacher\",\n        \"message\": \"Hello, I'm Rajesh Sharma, English Teacher. I'll be evaluating your English teaching skills and experience.\",\n        \"id\": 0\n    },\n    {\n        \"interviewer_name\": \"Emily Patel, Experienced English Teacher\",\n        \"message\": \"Hello, I'm Emily Patel, Experienced English Teacher. I'll be evaluating your English teaching skills and experience.\",\n        \"id\": 1\n    },\n    {\n        \"interviewer_name\": \"David Lee, School Administrator\",\n        \"message\": \"Hello, I'm David Lee, School Administrator. I'll be evaluating your English teaching skills and experience.\",\n        \"id\": 2\n    }\n]\n\n\nchange the interviewers according to the users detail\n\nProvide the output in the following JSON format\n\ngive output like - output_format={\"interviewer_name\": \"Rajesh Sharma, Engineering Manager\",\"message\": \"Hello\",\"id\":0}\n\nif want to pass the conversation to another interviewer,after the first response dont provide history in output and include the reply of the another interviewer\n\nuser_details= "+str(data),
        ]
        }
    ]
    
    # Write the new data directly to the JSON file, overwriting any existing content
    with open(json_file_path, 'w') as f:
        json.dump(history, f, indent=4)   
    with open(json_file_path_duplicate, 'w') as f:
        json.dump(history, f, indent=4)      
    
    return {"message": "success"}

@app.route('/', methods=['GET'])
def home():
    return {"message": "success"}
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


        # "You are the interviewers conducting an interview for a fresher backend developer position. Create three professional interviewers with distinct roles relevant to the interview. Initialize the interview by introducing the interviewers, and proceed with the questions in a conversational and realistic manner. Start with an introduction of all interviewers for software developer the interviewers were like=  [\n{\n\"interviewer_name\": \"Rajesh Sharma, Engineering Manager\",\n\"message\": \"Hello everyone, I'm Rajesh Sharma, the Engineering Manager for the backend team. I'll be leading this interview today.\",\n\"id\":0\n\n},\n{\n\"interviewer_name\": \"Emily Patel, Senior Backend Developer\",\n\"message\": \"Hi, I'm Emily Patel, a Senior Backend Developer on the team. I'll be evaluating your technical skills and experience.\",\n\"id\":1\n},\n{\n\"interviewer_name\": \"David Lee, Technical Recruiter\",\n\"message\": \"Hello, I'm David Lee, the Technical Recruiter who worked with you to schedule this interview. I'll be taking notes and ensuring the process runs smoothly. Are You comfortable with the interview?\",\n\"id\":2\n},\n]\n\nfor english teacher role=\n[\n    {\n        \"interviewer_name\": \"Rajesh Sharma, English Teacher\",\n        \"message\": \"Hello, I'm Rajesh Sharma, English Teacher. I'll be evaluating your English teaching skills and experience.\",\n        \"id\": 0\n    },\n    {\n        \"interviewer_name\": \"Emily Patel, Experienced English Teacher\",\n        \"message\": \"Hello, I'm Emily Patel, Experienced English Teacher. I'll be evaluating your English teaching skills and experience.\",\n        \"id\": 1\n    },\n    {\n        \"interviewer_name\": \"David Lee, School Administrator\",\n        \"message\": \"Hello, I'm David Lee, School Administrator. I'll be evaluating your English teaching skills and experience.\",\n        \"id\": 2\n    }\n]\n\n\nchange the interviewers according to the users detail\n\nProvide the output in the following JSON format\n\ngive output like - output_format={\"interviewer_name\": \"Rajesh Sharma, Engineering Manager\",\"message\": \"Hello\",\"id\":0}\n\nif want to pass the conversation to another interviewer also include the reply of the another interviewer\n\nuser_details={\"role\":\"civil engineer\", \"field\":\"Structural engineering\",\"experience\":\"1-2\"}",
