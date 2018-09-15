import sqlite3
import datetime
from flask import *
from api import db

# db = 'users.db'

def add_user(username, password, email):
    if username_exists(username):
        return jsonify(success=False, reason='Username already exists')
    if email_exists(email):
        return jsonify(success=False, reason='Email already exists')

    db.users.insert_one({"username": username, "password": password, "email": email, "color": "#000000", "pathHistory": [], "intersections": []})

    return jsonify(success=True, username=username)

def username_exists(username):
    print(db.users)
    print(db.users.find_one({"username": username}))
    return db.users.find_one({"username": username}) is not None

def email_exists(email):
    return db.users.find_one({"email": email}) is not None

def log_in(username, password):
    user = db.users.find_one({"username": username, "password": password})
    return jsonify(success=False, reason='Invalid username/password') if user is None else jsonify(success=True)
