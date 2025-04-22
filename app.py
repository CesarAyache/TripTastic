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

# # Create new dict to track point history per user
# point_history = {}

# @app.route('/book-flight', methods=['POST'])
# def book_flight():
#     data = request.get_json()
#     email = data['email']
#     destination = data['destination']
#     distance = data['distance']
#     date = data['date']
#     trip_id = str(len(bookings.get(email, [])) + 1)

#     new_trip = {
#         'id': trip_id,
#         'destination': destination,
#         'date': date,
#         'distance': distance
#     }

#     # Save booking
#     bookings.setdefault(email, []).append(new_trip)

#     # Calculate and add points
#     earned_points = distance * 0.5
#     user_points[email] = user_points.get(email, 0) + earned_points

#     # Save point history
#     point_record = {
#         'destination': destination,
#         'date': date,
#         'distance': distance,
#         'points': earned_points
#     }
#     point_history.setdefault(email, []).append(point_record)

#     return jsonify({
#         'message': 'Booking successful',
#         'earned_points': earned_points,
#         'total_points': user_points[email]
#     })