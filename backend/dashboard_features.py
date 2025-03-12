from flask import Blueprint, request, session, jsonify
from groq import Groq
import pymongo
import datetime
client = pymongo.MongoClient("mongodb://localhost:27017/")
from user_profile import get_user
from datetime import datetime, timedelta
from collections import defaultdict
import json
client = Groq(api_key="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")
dashboard_functions = Blueprint("dashboard_functions", __name__)



@dashboard_functions.route("/api/dashboard_data_fetch", methods=['GET'])
def dashboard():
    # print("The Mtype is : ",session["Mtype"]) #session["Mtype"]
    # data=get_weekly_analytics(usetype=session["Mtype"])
    # return jsonify(data[0])
    user_id=session.get("user_id")
    email=session.get("email")
    cursor=dict(get_user(user_id))
    if cursor["scenario"]=="interview":
        session["Mtype"]="interview"
    elif cursor["scenario"]=="Business-meeting":
        session["Mtype"]="bmeeting"
    print("cursor from dashboard : ",dict(cursor))
    print("from dashboard : ",{"user_id":user_id,"email":email})
    data=get_weekly_analytics(usetype=session["Mtype"])
    data=serialize_mongo_data(data)
    print("from dashboard : ",data)
    return jsonify(data)



def get_data():
    user_id=session.get("user_id")
    email=session.get("email")
    return {"user_id":user_id,"email":email}
@dashboard_functions.route("/api/store_session", methods=["POST", "GET"])
def store_user():
    data = request.get_json()
    print(":::data:::", data["user_id"])
    session["user_id"] = str(data["user_id"])
    session["email"] = str(data["email"])
    print("from dashboard")
    print("session id::::::::: ", session.get("user_id"))
    return jsonify(user_id=session.get("user_id"))

user=""
@dashboard_functions.route('/setsession',methods=["POST", "GET"])
def getsession():
    global user
    user_id = request.args.get("user_id")
    email = request.args.get("email")
    print("Data received:", user_id)
    user="QQQQQQQQQQ"
    session['user_id'] = user_id
    session['email'] = email

    return jsonify(user_id=session.get('user_id'),email=session.get('email'))


# @dashboard_functions.route('/session_set',methods=["POST", "GET"])
# def test_set():
    
#     user_id = request.form.get("user_id")

#     print(user)
#     global user
#     print("inside test set function")
#     session['user_id'] = "jjjjjjjjjjjjj"
#     return jsonify(user_id=session.get('user_id'))



def create_analytics(user_data):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an AI analyst specializing in interview performance analysis.\nYou will receive historical data of user interactions in AI-powered interviews.\nYour task is to generate a detailed analytics JSON, structured for easy visualization.\nEnsure each metric includes a date field to enable timeline-based insights.\n\n🔹 The JSON must contain the following analytics:\n\n1️⃣ Performance Trends Over Time\n\nInterview scores (date, score).\nGrammar accuracy (date, accuracy).\nSentiment progression (date, sentiment).\nInterview frequency (total_interviews).\n2️⃣ Language & Grammar Analysis\n\nCommon grammar mistakes and their frequency.\nReadability scores (date, score).\nMost frequently used words & phrases.\n3️⃣ Sentiment & Confidence Analysis\n\nSentiment breakdown per session.\nConfidence level progression (date, confidence_level).\nEmotional tone in responses.\n4️⃣ Engagement & Interaction Patterns\n\nUser talk time vs. AI talk time (date, user_talk_time, ai_talk_time).\nResponse length trend (date, average_response_length).\nResponse speed trend (date, response_speed).\n5️⃣ Question-Answer Analysis & Topic Proficiency\n\nMost frequent questions asked.\nDifficulty level breakdown (Easy, Medium, Hard).\nStrengths & weaknesses in technical topics.\n6️⃣ AI Recommendations for User Improvement\n\nFeedback trends from past interviews.\nSuggested improvements.\nNext steps for better performance.\n📌 use double quotes. Output Format: Return the JSON in the following structured format:\n\n📜 JSON Output Format with Comments\n\n{\n  \"user_id\": \"user_2nKvfjz5RHE5JEdlpcD2h2isN0U\",\n  \"analytics\": {\n    \"performance_trends\": {\n      \"interview_scores\": [\n                { \"date\": \"2025-02-17\", \"score\": 50 },\n        { \"date\": \"2025-02-19\", \"score\": 50 },\n        { \"date\": \"2025-02-21\", \"score\": 55 },\n        { \"date\": \"2025-02-22\", \"score\": 57 },\n        { \"date\": \"2025-02-23\", \"score\": 60 },\n        { \"date\": \"2025-02-24\", \"score\": 62 },\n        { \"date\": \"2025-02-25\", \"score\": 65 }\n      ],\n      \"grammar_accuracy\": [\n         { \"date\": \"2025-02-17\", \"accuracy\": 35 },\n        { \"date\": \"2025-02-19\", \"accuracy\": 45 },\n        { \"date\": \"2025-02-21\", \"accuracy\": 53 },\n        { \"date\": \"2025-02-22\", \"accuracy\": 58 },\n        { \"date\": \"2025-02-23\", \"accuracy\": 60 },\n        { \"date\": \"2025-02-24\", \"accuracy\": 64 },\n        { \"date\": \"2025-02-25\", \"accuracy\": 70 }\n      ],\n      \"sentiment_progression\": [\n        { \"date\": \"2025-02-17\", \"sentiment\": \"neutral\" },\n        { \"date\": \"2025-02-19\", \"sentiment\": \"neutral\" },\n        { \"date\": \"2025-02-21\", \"sentiment\": \"positive\" },\n        { \"date\": \"2025-02-22\", \"sentiment\": \"positive\" },\n        { \"date\": \"2025-02-23\", \"sentiment\": \"positive\" },\n        { \"date\": \"2025-02-24\", \"sentiment\": \"positive\" },\n        { \"date\": \"2025-02-25\", \"sentiment\": \"positive\" }\n      ],\n      \"interview_frequency\": 2\n    },\n    \"language_grammar_analysis\": {\n      \"common_mistakes\": {\n        \"tense_errors\": [2,[\"No, I don't know.\",\"Let's end this conversation and interview.\"]],\n        \"prepositions\": [1,[\"What is object-oriented programming (OOP) and give an example of inheritance in Python?\"]],\n        \"sentence_fragments\": [1,[\"Okay fine, so let's start by asking questions\"]]\n      },\n      \"readability_score\": [\n       { \"date\": \"2025-02-17\", \"score\": 60 },\n        { \"date\": \"2025-02-19\", \"score\": 60 },\n        { \"date\": \"2025-02-21\", \"score\": 62 },\n        { \"date\": \"2025-02-22\", \"score\": 63 },\n        { \"date\": \"2025-02-23\", \"score\": 65 },\n        { \"date\": \"2025-02-24\", \"score\": 67 },\n        { \"date\": \"2025-02-25\", \"score\": 70 }\n      ],\n      \"top_words\": [\"Hello\", \"Okay\", \"Let's\"]\n    },\n    \"sentiment_confidence_analysis\": {\n      \"sentiment_distribution\": {\n        \"positive\": 10,\n        \"neutral\": 85,\n        \"negative\": 5\n      },\n      \"confidence_trend\": [\n         { \"date\": \"2025-02-17\", \"confidence_level\": \"low\" },\n        { \"date\": \"2025-02-19\", \"confidence_level\": \"low\" },\n        { \"date\": \"2025-02-21\", \"confidence_level\": \"medium\" },\n        { \"date\": \"2025-02-22\", \"confidence_level\": \"medium\" },\n        { \"date\": \"2025-02-23\", \"confidence_level\": \"high\" },\n        { \"date\": \"2025-02-24\", \"confidence_level\": \"high\" },\n        { \"date\": \"2025-02-25\", \"confidence_level\": \"high\" }\n      ],\n      \"emotional_tone\": [\"nervous\", \"uneasy\"]\n    },\n    \"engagement_patterns\": {\n      \"user_talk_time\": [\n                { \"date\": \"2025-02-17\", \"user_talk_time\": 35, \"ai_talk_time\": 65 },\n        { \"date\": \"2025-02-19\", \"user_talk_time\": 35, \"ai_talk_time\": 65 },\n        { \"date\": \"2025-02-21\", \"user_talk_time\": 40, \"ai_talk_time\": 60 },\n        { \"date\": \"2025-02-22\", \"user_talk_time\": 42, \"ai_talk_time\": 58 },\n        { \"date\": \"2025-02-23\", \"user_talk_time\": 45, \"ai_talk_time\": 55 },\n        { \"date\": \"2025-02-24\", \"user_talk_time\": 47, \"ai_talk_time\": 53 },\n        { \"date\": \"2025-02-25\", \"user_talk_time\": 50, \"ai_talk_time\": 50 },\n        {\"average_user_talk_time\": 45, \"average_ai_talk_time\": 55}\n      ],\n      \"response_length_trend\": [\n        {\n          \"average_response_length\": 15\n        },\n      ],\n      \"response_speed_trend\": [\n        {\n          \"response_speed\": 2.0\n        }\n      ],\n    },\n    \"qa_analysis\": {\n      \"most_frequent_questions\": [\n        \"What is object-oriented programming (OOP) and give an example of inheritance in Python?\",\n        \"Can you explain the concept with a simple class hierarchy diagram?\"\n      ],\n      \"difficulty_levels\": \"medium\",\n      \"question_types\": {\n        \"technical\": 2,\n        \"behavioral\": 1\n      },\n      \"answering_proficiency\": {\n          \"technical\": 50,\n          \"behavioral\": 70\n      },\n      \"interviewers_types\": \n        [\n            {\"interviewer_name\": \"Rajesh Sharma\",\"Position\": \"Senior Software Engineer\"},\n            {\"interviewer_name\": \"Emily Patel\", \"Position\": \"Software Engineer\"},\n            {\"interviewer_name\": \"David Lee\" , \"Position\": \"Software Engineer\"}\n\n        ],\n      \"strengths_weaknesses\": {\n        \"strengths\": [],\n        \"weaknesses\": [\"Lack of understanding or confidence in explaining basic programming concepts\"]\n      }\n    },\n    \"ai_recommendations\": {\n      \"feedback_trends\": [\n        \"The user appeared to lack confidence when answering technical questions, specifically those related to fundamental programming concepts.\",\n        \"Encourage the user to review basic programming concepts such as Object-Oriented Programming (OOP).\"\n      ],\n      \"suggested_improvements\": [\n        \"Review OOP principles and practice coding exercises to build confidence and understanding.\",\n        \"Work on expressing technical concepts clearly and concisely.\"\n      ],\n      \"next_steps\": [\n        \"Attend workshops or online courses focused on fundamental programming concepts.\",\n        \"Engage in mock interviews to practice and gain confidence.\"\n      ]\n    }\n  }\n}"
            },
            {
                "role": "user",
                "content": "'''"+str(user_data)+"'''"
            },
        ],
        temperature=1,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response=completion.choices[0].message
    return json.loads(response.content)



from datetime import datetime, timedelta
from collections import defaultdict
from pymongo import MongoClient
from bson import ObjectId
from pymongo import DESCENDING


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

def save_analytics(data, usertype,save,last_updated_with=None, date=None,conversationID=None):
    if date is None:
        date = datetime.today().date()

    user_id = session["user_id"]
    email = session["email"]
    if save=="per_conv_analysis":
        out = {
            "user_id": user_id,
            "email": email,
            "analytics": data,
            "date": str(date),
            "usetype": usertype,
            "conversationID": conversationID,
            
        }
    if save=="weekly_analysis": 
        out = {
            "user_id": user_id,
            "email": email,
            "analytics": data,
            "date": str(date),
            "usetype": usertype,
            "last_updated_with":str(last_updated_with),
            
        }
    
    db = client["users_conversation"]
    analytics_collection=db["analytics"]
    analytics_collection.insert_one(out)
    # serialize_mongo_data(analytics_collection.find_one(out))
    
    print("Analytics saved.")
    return serialize_mongo_data(analytics_collection.find_one(out))


def group_by_week(data):
    weekly_data = defaultdict(list)

    for entry in data:
        date_str = entry.get("date")  # Ensure "date" key exists
        if not date_str:
            continue
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            week_start = date_obj - timedelta(days=date_obj.weekday())  # Get Monday of the week
            week_label = week_start.strftime("%Y-%m-%d")
            weekly_data[week_label].append(entry)
        except ValueError:
            print(f"Invalid date format: {date_str}")

    return weekly_data

def get_weekly_analytics(usetype):
    db = client["users_conversation"]
    user_id = session["user_id"]
    user_collection = db[str(user_id)]
    analytics_collection=db["analytics"]
    # Fetch user data
    data = list(user_collection.find({"usetype": usetype}))  # Exclude `_id` for clarity

    if not data:
        print("No user data found.")
        return

    # Group conversations into weeks
    weekly_conversations = group_by_week(data)
    
    if not weekly_conversations:
        print("No weekly data available.")
        return
    
    weeks = list(weekly_conversations.keys())
    data=dict(weekly_conversations)
    print(weeks)
    # Ensure at least one week exists

    if weeks:
        

        last_convo_id=serialize_mongo_data(data[weeks[-1]][-1]["_id"])
        # print(last_convo_id)
        # print({"user_id":user_id,"usetype": "weekly_"+usetype+"_analytics","last_updated_with":str(last_convo_id)})
        last_history=analytics_collection.find_one({"user_id":user_id,"usetype": "weekly_"+usetype+"_analytics","last_updated_with":str(last_convo_id)})
        if len(last_history)==0 :
            analytics_data = create_analytics(user_data=serialize_mongo_data(data[weeks[-1]])) # Ensure function is defined
        # # print("analysis doneeeee",data[weeks[-1]][-1]["_id"])
            print("Weekly analytics saved.")

            return save_analytics(save="weekly_analysis",data=analytics_data, usertype="weekly_"+usetype+"_analytics", date=weeks[-1],last_updated_with=data[weeks[-1]][-1]["_id"])


        else:
            print("from database")
            return last_history
            
            # print(last_history)
        # print( "analysis started",serialize_mongo_data(data[weeks[-1]][-1]["_id"]))

        # 

def get_perconvo_analysis(usetype):
    db = client["users_conversation"]
    user_id = session["user_id"]
    user_collection = db[str(user_id)]
    analytics_collection=db["analytics"]

    data = user_collection.find_one({"user_id":user_id,"usetype":usetype}, sort=[('date', DESCENDING)])
    print(dict(data))
    entity=list(analytics_collection.find({"usetype":"convo_"+usetype+"_analytics","conversationID":str(data["_id"])}))
    # print("length a",len(list(entity)))

    if  len(entity)==0 :
        print(len(list(entity)))
        print("inside")
        analytics_data = create_analytics(user_data=serialize_mongo_data(data)) # Ensure function is defined
        return list(save_analytics(data=analytics_data, usertype="convo_"+usetype+"_analytics",conversationID=str(data["_id"]),save="per_conv_analysis"))
        
    else:
        print("already present")
        return entity

    # print(data)
  # Exclude `_id` for clarity


def serialize_mongo_data(data):
    if isinstance(data, list):
        return [{**doc, "_id": str(doc["_id"])} for doc in data]
    elif isinstance(data, dict):
        data["_id"] = str(data["_id"])
        return data
    return data