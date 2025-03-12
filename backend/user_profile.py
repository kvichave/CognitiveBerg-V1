import sqlite3
from flask import Flask,request,session,Blueprint
import json

user_profile=Blueprint('user_profile',__name__)
@user_profile.route("/api/user_profile",methods=["POST","GET"])
def submit_user_profile():   
    data = request.get_json()  # Get the incoming JSON data
    # print("data::: ")
    userid = data['user']['id']
    role = data.get('role')
    field = data.get('field')
    experience = data.get('experience')
    scenario = data.get('scenario')
    purpose = data.get('purpose')
    selected_values = ', '.join(data.get('selectedValues', []))  # Convert list to a string for storage
    # print("role::: ",role)

    # print("id::: ",userid)
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    if user_exists(userid):
        # Update the existing user record
        cursor.execute('''
            UPDATE user_profile
            SET role = ?, field = ?, experience = ?, scenario = ?, purpose = ?, selected_values = ?
            WHERE clerk_id = ?
        ''', (role, field, experience, scenario, purpose, selected_values, userid))
        message = "User profile updated successfully!"
    else:
        # Insert a new user record
        cursor.execute('''
            INSERT INTO user_profile (clerk_id, role, experience, scenario, purpose, selected_values, field)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (userid, role, experience, scenario, purpose, selected_values, field))
        message = "New user profile added successfully!"

    conn.commit()  # Commit the changes
    conn.close()  # Close the connection
    return "success"

@user_profile.route("/test")
def test():
    print("test")
    # print(session.get('clerkId'))
    return "success"

def get_db_connection():
    conn = sqlite3.connect('/home/kunal/Documents/major_project/CognitiveBerg/clerkData.db')
    conn.row_factory = sqlite3.Row
    return conn
def user_exists(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(1) FROM user_profile WHERE clerk_id = ?', (userid,))
    exists = cursor.fetchone()[0]
    conn.close()
    return exists

def get_user(userid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_profile WHERE clerk_id = ?', (userid,))
    exists = cursor.fetchone()
    conn.close()
    return exists


@user_profile.route("/api/check_user_profile", methods=["POST", "GET"])
def check_user_profile():
    data=request.get_json()
    print("data::: ",data)
    user_id=data['user']['id']
    print(user_id)
    if user_exists(user_id):
        return([True])
    else:
        return([False])

# 