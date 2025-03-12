from flask import Flask, session,request, jsonify
from flask_session import Session
from flask_cors import CORS
from dashboard_features import dashboard_functions,get_data

from call_llm import call_LLm
from call_llm import socketio
from chat_CRUD import mongodb_handler
from user_profile import user_profile
from clerkData import clerk_db

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "lanukVichave@258"

CORS(app,supports_credentials=True)

app.register_blueprint(user_profile)
app.register_blueprint(clerk_db)
app.register_blueprint(call_LLm)
app.register_blueprint(dashboard_functions)
app.register_blueprint(mongodb_handler)

socketio.init_app(app, cors_allowed_origins="*")


@app.route('/')
def hello_world():
    
    """
    Root endpoint. Returns a simple "Hello World" message.

    """
    print(get_data())
    
    return 'Hello World'






    
@app.route('/generatereport',methods=['GET'])
def new():
    # session["name"] = "kunal"
    
    user_id=session.get("user_id")
    email=session.get("email")
    print("from generatereport file main : ",{"user_id":user_id,"email":email})
    return {"user_id":user_id,"email":email}



if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
