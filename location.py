from flask import *
from api import db

def add_new_location(username, coordinates):
    user = db.find_one({"username": username})
    if user is not None:
        return jsonify(success=False, reason="User does not exist")
    
    