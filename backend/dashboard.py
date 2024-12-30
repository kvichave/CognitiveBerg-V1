import sqlite3
from flask import Flask,request,session,Blueprint,jsonify
import json
import chat_functions

dashboard_functions=Blueprint('dashboard_functions',__name__)
import google.generativeai as genai
import os


genai.configure(api_key="AIzaSyC0O4dCvtLxrXg3BMBciSzrXhO3Vkb5Irw")

@dashboard_functions.route("/api/dashboard_data_fetch",methods=["POST","GET"])
def dashboard():
    userid=session['user_id']
    print(userid)
    userData=chat_functions.get_user_data(userid)
       
    if userData=={}:
        user_chat=chat_functions.get_chat(userid)
        if user_chat==[]:
            return{"status":False}
        else:
            
            model = genai.GenerativeModel("gemini-1.5-flash", )
            chat = model.start_chat(
                history=[]
            )
            response=chat.send_message(str(user_chat)+'''  keeping in mind that is is voice to text, judge it like that only
give me the  [Fluency,English score,Frequently Used Terms,Confidence Score,Pronunciation Accuracy,Grammar Correction Rate, Speech Analysis Breakdown, Top Mistakes to Focus On,Interview Readiness Meter,Suggestions for Next Sessions,Progress Over Time] of the user where role is user only  , use percentage or score, Return only valid JSON''')
        try:
            # The actual JSON response is embedded within the response string
            # Remove the ```json and trailing ``` markers
            print("string")
            print(response.text)
            json_str = str(response.text).strip('```json\n').strip('```')
            print("---------------------------------------------")
            print(json_str)
            # Parse the extracted JSON string
            print("load")
            json_response = json.loads(json_str)

            # Print or return the JSON response
            print("dump")
            print(json.dumps(json_response, indent=4))
            response=json.dumps(json_response, indent=4)  # Pretty-print JSON response

        except json.JSONDecodeError:
            print("Failed to parse JSON from response.")
        except KeyError:
            print("Response does not contain the expected structure.")          
            # print((json_response))
            return response





    else:
        response=jsonify(userData)
    print("user id::::::::: ",session.get('user_id'))
    print(type(response))
    return {"response":response}


@dashboard_functions.route("/api/store_session",methods=["POST","GET"])
def store_user():
    data=request.get_json()
    print(":::data:::",data['user_id'])
    session['user_id'] = data['user_id']
    session['email'] = data['email']
    print("sessuion id::::::::: ",session.get('user_id'))
    return data['user_id']

    # user_id = data.get('user_id')
    # email = data.get('email')

    # Store user information in the Flask session
    # session['user_id'] = user_id
    # session['email'] = email

