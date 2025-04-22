from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows requests from other origins like your frontend

# Admin login credentials (for demo purposes)
ADMIN_EMAIL = 'admin@triptastic.com'
ADMIN_PASS = 'admin123'

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    if email == ADMIN_EMAIL and password == ADMIN_PASS:
        return jsonify({'message': 'Admin login successful'})
    else:
        return jsonify({'message': 'Invalid admin credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)
