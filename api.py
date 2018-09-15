from flask import *
from flask_pymongo import PyMongo
import sqlite3

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://admin:wordpass1337@ds028310.mlab.com:28310/degrees"
mongo = PyMongo(app)
db = mongo.db

import auth
import profile

@app.route('/')
def cakes():
    return 'Yummy cakes!'

@app.route('/signup', methods=['POST'])
def sign_up():
    try:
        username = request.form['user']
        password = request.form['pass']
        email = request.form['email']
        return auth.add_user(username, password, email)
    except:
        return jsonify(success=False, reason='Could not sign up due to a Server Error'), 500

@app.route('/signin', methods=['GET'])
def sign_in():
    try:
        username = request.args.get('user')
        password = request.args.get('pass')
        return auth.log_in(username, password)
    except:
        return jsonify(success=False, reason='Could not sign in due to a Server Error'), 500

@app.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        return profile.update_profile(**request.json)
    except:
        return jsonify(success=False, reason='Could not update profile due to a Server Error'), 500

@app.route('/get_profile', methods=['GET'])
def get_profile():
    try:
        username = request.args.get('user')
        return profile.get_profile(username)
    except:
        return jsonify(success=False, reason='Could not get profile due to a Server Error'), 500

if __name__ == '__main__':
    # initialize_dbs()
    app.run(debug=True, host='0.0.0.0', port=5555)
