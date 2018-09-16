from flask import *
from api import db
import geopy.distance

def check_close(username, coords):
    users = db.users.find()
    for user in users:
      if (user.currentLocation) and (user.username != username):
        if (geopy.distance.vincenty(coords, (user.currentLocation[0], user.currentLocation[1])).km < 0.02):
          add_intersection(username, user.username coords[0], coords[1])

def add_new_location(username, lat, lng):
    user = db.users.find_one({"username": username})
    if user is None:
        return jsonify(success=False, reason="User does not exist")
    
    db.users.update_one({"username": username}, {"$push": {"pathHistory": [lat, lng]}})
    db.users.update_one({"username": username}, {"$set": {"currentLocation": [lat, lng]}})

    check_close(username, (lat, lng))

    return jsonify(success=True)

