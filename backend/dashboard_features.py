from flask import Blueprint, request, session, jsonify

dashboard_functions = Blueprint("dashboard_functions", __name__)

@dashboard_functions.route("/api/dashboard_data_fetch", methods=["POST", "GET"])
def dashboard():
    return "success"

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
