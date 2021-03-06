from flask import *
from api import db
import time

DEFAULT_IMAGE = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRaWsjTM9wIYQ-L9K5yj7MvBI222lgSd3fpML3zmdwQ8oPHS1Y4'

def add_user(username, password, email):
    if username_exists(username):
        return jsonify(success=False, reason='Username already exists')
    if email_exists(email):
        return jsonify(success=False, reason='Email already exists')

    db.users.insert_one({"username": username, "password": password, "email": email, "color": "#000000", "pathHistory": [], "intersections": [], "currentLocation": [], "lastRevealed": time.time(), "image": DEFAULT_IMAGE})

    return jsonify(success=True, username=username)

def username_exists(username):
    return db.users.find_one({"username": username}) is not None

def email_exists(email):
    return db.users.find_one({"email": email}) is not None

def log_in(username, password):
    user = db.users.find_one({"username": username, "password": password})
    return jsonify(success=False, reason='Invalid username/password') if user is None else jsonify(success=True)
