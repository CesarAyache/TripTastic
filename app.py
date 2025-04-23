from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_cors import CORS
import json, os
import sqlite3

app = Flask(__name__)
CORS(app)

user_file = 'users.json'

# In-memory storage for demo (you can replace with a database)
bookings = {}
user_points = {}
point_history = {}

# -------------------- UTILS --------------------

def read_users():
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    return {}

def write_users(data):
    with open(user_file, 'w') as f:
        json.dump(data, f)

# -------------------- USER AUTH --------------------

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

# -------------------- ADMIN --------------------

# ADMIN_EMAIL = 'admin@triptastic.com'
# ADMIN_PASS = 'admin123'

# @app.route('/admin-login', methods=['POST'])
# def admin_login():
#     data = request.get_json()
#     if data['email'] == ADMIN_EMAIL and data['password'] == ADMIN_PASS:
#         return jsonify({'message': 'Admin login successful'})
#     return jsonify({'message': 'Access denied'}), 403

# @app.route('/users', methods=['GET'])
# def get_users():
#     users = read_users()
#     user_list = [{'name': v['name'], 'email': k, 'age': v['age']} for k, v in users.items()]
#     return jsonify({'users': user_list})

# @app.route('/delete-user', methods=['POST'])
# def delete_user():
#     data = request.get_json()
#     users = read_users()
#     if data['email'] in users:
#         del users[data['email']]
#         write_users(users)
#         return jsonify({'message': 'User deleted'})
#     return jsonify({'message': 'User not found'}), 404
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Admin credentials
ADMIN_EMAIL = "triptastic_only@admin.com"
ADMIN_PASSWORD = "triptastic123"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/manager', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('manager_dashboard'))
        else:
            return render_template('manager.html', error="Invalid email or password.")
    return render_template('manager.html')

@app.route('/manager_dashboard')
def manager_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('manager_login'))

    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    trips = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()

    return render_template('manager_dashboard.html', users=users, trips=trips)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('manager_login'))

if __name__ == '__main__':
    app.run(debug=True)

# -------------------- BOOKINGS & POINTS --------------------

@app.route('/book-flight', methods=['POST'])
def book_flight():
    data = request.get_json()
    email = data['email']
    destination = data['destination']
    distance = data['distance']
    date = data['date']
    trip_id = str(len(bookings.get(email, [])) + 1)

    # Save booking
    new_trip = {
        'id': trip_id,
        'destination': destination,
        'date': date,
        'distance': distance
    }
    bookings.setdefault(email, []).append(new_trip)

    # Calculate and add loyalty points
    earned_points = distance * 0.5
    user_points[email] = user_points.get(email, 0) + earned_points

    # Save point history
    point_record = {
        'destination': destination,
        'date': date,
        'distance': distance,
        'points': earned_points
    }
    point_history.setdefault(email, []).append(point_record)

    return jsonify({
        'message': 'Booking successful',
        'earned_points': earned_points,
        'total_points': user_points[email]
    })

@app.route('/upcoming')
def get_upcoming():
    email = request.args.get('email')
    return jsonify({'trips': bookings.get(email, [])})

@app.route('/cancel-booking', methods=['POST'])
def cancel_trip():
    data = request.get_json()
    email = data['email']
    trip_id = data['trip_id']
    if email in bookings:
        bookings[email] = [trip for trip in bookings[email] if trip['id'] != trip_id]
        return jsonify({'message': 'Booking cancelled'})
    return jsonify({'message': 'Booking not found'}), 404

# -------------------- PROFILE DATA --------------------

@app.route('/user-info')
def user_info():
    email = request.args.get('email')
    users = read_users()
    user = users.get(email, {})
    return jsonify({
        'name': user.get('name', ''),
        'email': email,
        'age': user.get('age', ''),
        'points': user_points.get(email, 0)
    })

@app.route('/points-history')
def get_points_history():
    email = request.args.get('email')
    history = point_history.get(email, [])
    return jsonify({'history': history})

# -------------------- ROOT --------------------

@app.route('/')
def index():
    return "TripTastic API is running!"

# -------------------- MAIN --------------------

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