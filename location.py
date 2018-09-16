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
    users = db.users.find({"$or": [{"username": username}, {"username": otherUser}]})
    
    db.users.update({"$or": [{"username": username}, {"username": otherUser}]}, {"$push": {"intersections": [lat, lng]}})

    return jsonify(success=True)
