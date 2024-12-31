import sqlite3
from flask import Flask,request,session,Blueprint
import json
    # @app.route("/api/webhooks",methods=["POST","GET"])
    # def getData():
    #     data=request.get_json()
    #     print("this is webhook",type(data))
    #     return "success"
clerk_db=Blueprint('clerk_db',__name__)
@clerk_db.route("/api/webhooks", methods=["POST", "GET"])
def clerk():
    data=request.get_json()
    # print("data",data)
    clerkId,clerkName,clerkEmail,requestType=extractClerk(data)
    conn = get_db_connection()
    
    if requestType == "user.created":
        cursor = conn.execute('SELECT * FROM clerk WHERE clerk_id = ? OR email = ?', (clerkId, clerkEmail))
        existing_user = cursor.fetchone()

        if existing_user:
            print("User already exists. No new user created.")
        else:
            conn.execute('INSERT INTO clerk (name, email, clerk_id) VALUES (?, ?, ?)', (clerkName, clerkEmail, clerkId))
            conn.commit()
            print("User created")

    elif requestType == "user.deleted":
        # Delete user from the database using clerk_id
        conn.execute('DELETE FROM clerk WHERE clerk_id = ?', (clerkId,))
        conn.commit()
        print("User deleted")

    elif requestType == "user.updated":
        # Update user information in the database using clerk_id
        conn.execute('UPDATE clerk SET name = ?, email = ? WHERE clerk_id = ?', (clerkName, clerkEmail, clerkId))
        conn.commit()
        print("User updated")

    # elif requestType == "session.created":
    #     session['clerkId'] = clerkId
    #     print("session ::::::::" ,session.get('clerkId'))


    conn.close()
    # print(clerkName,clerkEmail,clerkId,requestType)
    return("Success")


def extractClerk(data):
    requestType=data['type']
    if requestType == "session.created":
        clerkId=data['data']['user_id']
        clerkName="NA"
        clerkEmail="NA"
        return(clerkId,clerkName,clerkEmail,requestType)


    if requestType == "user.deleted":
            clerkId=data['data']['id']
            clerkName="NA"
            clerkEmail="NA"
            return(clerkId,clerkName,clerkEmail,requestType)
    clerkId=data['data']['id']

    clerkName=data['data']['first_name']
    clerkEmail=data['data']['email_addresses'][0]['email_address']
    return (clerkId,clerkName,clerkEmail,requestType)



def get_db_connection():
    conn = sqlite3.connect('/home/kunal/Documents/CognitiveBerg/clerkData.db')
    conn.row_factory = sqlite3.Row  # Allows us to return rows as dictionaries
    return conn




