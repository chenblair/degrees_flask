from flask import *
from api import db
import mpu

def check_close(username, coords):
    users = db.users.find()
    for user in users:
      if (user.get("currentLocation", False)) and (user["username"] != username):
        if (mpu.haversine_distance(coords, (float(user["currentLocation"][0]), float(user["currentLocation"][1]))) < 0.02):
          add_intersection(username, user["username"], coords[0], coords[1])

def add_new_location(username, lat, lng):
    user = db.users.find_one({"username": username})
    if user is None:
        return jsonify(success=False, reason="User does not exist")
    
    db.users.update_one({"username": username}, {"$push": {"pathHistory": [lat, lng]}})
    db.users.update_one({"username": username}, {"$set": {"currentLocation": [lat, lng]}})

    check_close(username, (lat, lng))

    return jsonify(success=True)

# doesn't check if intersection was already added but check_close should handle it
def add_intersection(username, otherUser, lat, lng):
    # check if user does not exist
    user = db.users.find_one({"username": username})
    user2 = db.users.find_one({"username": otherUser})
    if user is None or user2 is None:
        return jsonify(success=False, reason="One of the users does not exist")
    
    # check if intersection has already occurred between these two users
    prevOccur = db.users.find_one({"$and": [{"username": username}, {"intersections.otherUser": otherUser}]})
    if prevOccur is not None:
        return jsonify(success=False, reason="Intersection already exists")

    # add intersection in both users
    db.users.update_one({"username": username}, {"$push": {"intersections": {"otherUser": otherUser, "coords": [lat, lng]}}})
    db.users.update_one({"username": otherUser}, {"$push": {"intersections": {"otherUser": username, "coords": [lat, lng]}}})

    return jsonify(success=True)

def traverse(username):
    user = db.users.find_one({"username": username})
    if user is None:
        return jsonify(success=False, reason="User does not exist")
    users = [user]
    moreUsers = []
    depth = 0
    tree = []
    while len(users) > 0:
        users = list(filter(lambda x: len(x["intersections"]) > 1, users))
        for user in users:
            user2 = db.users.find_one({"username": user["intersections"][0]["otherUser"]})
            while user2["intersections"][0]["otherUser"] != user["username"]:
                user2["intersections"].drop(0)
            moreUsers.append(user2["intersections"])
        users = users + moreUsers
        level = []
        for user in users:
            level.append([user["intersections"][0]["coords"], user["intersections"][1]["coords"], user["color"]])
            user["intersections"].drop(0)
        tree.append(level)
    return json.dumps(tree)

# get second degree intersections
def get_questionable_node_list(username):
    user = db.users.find_one({"username": username})
    if user is None:
        return jsonify(success=False, reason="User does not exist")
    
    nodes = []

    # stop at second degree
    if len(user["intersections"]) > 0:
        # get intersections of all intersections
        for intersection in user["intersections"]:
            # add this point to list
            nodes.append(intersection["coords"])
            # get other user
            user2 = db.users.find_one({"username": intersection["otherUser"]})
            # delete everything up to first intersection with OG user
            while user2["intersections"][0]["otherUser"] != user["username"]:
                user2["intersections"].drop(0)
            # add all other intersections to nodes list
            for remaining in user2["intersections"]:
                nodes.append(remaining["coords"])
    return json.dumps(nodes)
