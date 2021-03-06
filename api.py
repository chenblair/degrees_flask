from flask import *
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://admin:wordpass1337@ds028310.mlab.com:28310/degrees"
mongo = PyMongo(app)
db = mongo.db

import auth
import profile
import location

@app.route('/')
def cakes():
    return 'Yummy cakes!'

@app.route('/signup', methods=['POST'])
def sign_up():
    try:
        return auth.add_user(**request.json)
    except:
        return jsonify(success=False, reason='Could not sign up due to a Server Error'), 500

@app.route('/signin', methods=['GET'])
def sign_in():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
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
        username = request.args.get('username')
        return profile.get_profile(username)
    except:
        return jsonify(success=False, reason='Could not get profile due to a Server Error'), 500

@app.route('/add_new_location', methods=['POST'])
def add_new_location():
    try:
        return location.add_new_location(**request.json)
    except:
        return jsonify(success=False, reason='Could not add location due to a Server Error'), 500

@app.route('/get_intersections', methods=['GET'])
def get_intersections():
    try:
        username = request.args.get('username')
        return profile.get_intersections(username)
    except:
        return jsonify(success=False, reason='Could not get intersections due to a Server Error'), 500

@app.route('/traverse', methods=['GET'])
def traverse():
    username = request.args.get('username')
    return location.traverse_fake(username)
    # try:
    #     username = request.args.get('username')
    #     return location.traverse(username)
    # except:
    #     return jsonify(success=False, reason='Could not get traversal tree due to a Server Error'), 500

@app.route('/get_question_marks', methods=['GET'])
def questionable_fcn():
    username = request.args.get('username')
    return location.get_questionable_node_list(username)
    # try:
    #     username = request.args.get('username')
    #     return location.get_questionable_node_list(username)
    # except:
    #     return jsonify(success=False, reason='Could not get question mark locations due to a Server Error'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
