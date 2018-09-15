from flask import *
from api import db

def add_new_location(username, lat, lng):
    user = db.users.find_one({"username": username})
    if user is None:
        return jsonify(success=False, reason="User does not exist")
    
    db.users.update_one({"username": username}, {"$push": {"pathHistory": [lat, lng]}})

    return jsonify(success=True)

