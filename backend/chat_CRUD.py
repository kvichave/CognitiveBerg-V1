from flask import Blueprint, session, jsonify
import pymongo
import datetime
import json
mongodb_handler = Blueprint("mongodb_handler", __name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")


def add_data(conversation,usetype):
    print("\n\nInside add_data---------------------------------------------------\n\n")
    user_id=session.get("user_id")
    email=session.get("email")
    today = datetime.date.today()
    out={"user_id":user_id,"email":email,"conversation":conversation,"date":str(today),"usetype":usetype}
    db = client["users_conversation"]
    collection = db[str(user_id)]
    collection.insert_one(out)
    print(conversation)

    # return jsonify(user_id=session.get("user_id"))
