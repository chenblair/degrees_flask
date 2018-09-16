from flask import *
from api import db
from bson.json_util import dumps
import json

# db = 'profiles.db'

DEFAULT_IMAGE = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaWsjTM9wIYQ-L9K5yj7MvBI222lgSd3fpML3zmdwQ8oPHS1Y4'

def create_profile(user):
    if user.get('') is not None and user.get('') is not None: # TODO: fix this schema
        db.users.insert_one(user)

def update_profile(username, password=None, email=None, color=None, pathHistory=None, intersections=None):
    user = db.users.find_one({"username": username})
    print(user)
    if user is None:
        return jsonify(success=False, reason="User does not exist")

    if password is not None:
        db.users.update_one({"username": username}, {"$set": {"password": password}})
    if email is not None:
        db.users.update_one({"username": username}, {"$set": {"email": email}})
    if color is not None:
        db.users.update_one({"username": username}, {"$set": {"color": color}})
    if pathHistory is not None:
        db.users.update_one({"username": username}, {"$set": {"pathHistory": pathHistory}})
    if intersections is not None:
        db.users.update_one({"username": username}, {"$set": {"intersections": intersections}})

    return jsonify(success=True)

def get_profile(username):
    # create_profile(username)
    data = db.users.find_one({"username": username})
    return dumps(data) if data is not None else jsonify(success=False, reason="User does not exist")

# TODO: unused?
def get_name(user):
    # create_profile(user)
    conn = sqlite3.connect(db)  # connect to that database (will create if it doesn't already exist)
    c = conn.cursor()  # make cursor into database (allows us to execute commands)
    rows = c.execute('''SELECT name FROM profiles WHERE user = ?;''', (user,)).fetchone()
    return rows[0]

def get_intersections(username):
    user = db.users.find_one({"username": username})
    return json.dumps(user["intersections"]) if user is not None else jsonify(success=False, reason="User does not exist")
