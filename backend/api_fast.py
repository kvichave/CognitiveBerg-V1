# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,session,g
# from flask_socketio import SocketIO
from user_profile import user_profile
from clerkData import clerk_db
from dashboard import dashboard_functions
from flask_cors import CORS
from call_llm import call_LLm
from call_llm import socketio
from flask_session import Session





app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SECRET_KEY'] = 'lanukVichave@258'
CORS(app)

app.register_blueprint(user_profile)
app.register_blueprint(clerk_db)
app.register_blueprint(dashboard_functions)
app.register_blueprint(call_LLm)
# socketio = SocketIO( app,cors_allowed_origins="*")  # Use async mode for Flask-SocketIO

socketio.init_app(app, cors_allowed_origins="*")

@app.route('/')
def hello_world():
    # session["test"]="kunal"

    return 'Hello World'
@app.route('/getname')
def getname():
    session["name"]="kunal"
    user = session["name"]  # Access the value from g

    print(user)
    return user


if __name__ == '__main__':
    socketio.run(app,debug=True, host='0.0.0.0',port=5000)
