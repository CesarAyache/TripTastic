from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

user_file = 'users.json'

def read_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    return {}

def write_users(data):
    with open(user_file, 'w') as f:
        json.dump(data, f)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    users = read_users()
    if data['email'] in users:
        return jsonify({'message': 'User already exists'}), 400
    users[data['email']] = data
    write_users(users)
    return jsonify({'message': 'User created successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    users = read_users()
    user = users.get(data['email'])
    if user and user['password'] == data['password']:
        return jsonify({'message': 'Login successful'})
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
