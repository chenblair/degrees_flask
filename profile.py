from flask import *
from api import db
from bson.json_util import dumps

# db = 'profiles.db'

DEFAULT_IMAGE = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaWsjTM9wIYQ-L9K5yj7MvBI222lgSd3fpML3zmdwQ8oPHS1Y4'

def update_profile(username, name=None, password=None, email=None, color=None, pathHistory=None, intersections=None):
    user = db.users.find_one({"username": username})
    print(user)
    if user is None:
        return jsonify(success=False, reason="User does not exist")

    if name is not None:
        db.users.update_one({"username": username}, {"$set": {"name": name}})
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
    data = db.users.find_one({"username": username})
    return dumps(data) if data is not None else jsonify(success=False, reason="User does not exist")

def get_intersections(username):
    user = db.users.find_one({"username": username})
    return user.intersections if user is not None else jsonify(success=False, reason="User does not exist")
