from flask import Flask, session,request, jsonify
from flask_session import Session
from flask_cors import CORS
from call_llm import call_LLm
from call_llm import socketio
from chat_CRUD import mongodb_handler
from user_profile import user_profile
from clerkData import clerk_db
from dashboard_features import dashboard_functions

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "lanukVichave@258"

CORS(app,supports_credentials=True)

app.register_blueprint(user_profile)
app.register_blueprint(clerk_db)
app.register_blueprint(dashboard_functions)
app.register_blueprint(call_LLm)
app.register_blueprint(mongodb_handler)

socketio.init_app(app, cors_allowed_origins="*")

@app.route('/')
def hello_world():
    
    """
    Root endpoint. Returns a simple "Hello World" message.
    """
    return 'Hello World'







    

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
