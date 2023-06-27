# File: /cherryAI/app.py

# Import necessary modules
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson.json_util import dumps

# Initialize Flask app and Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Connect to MongoDB database
client = MongoClient('your-connection-string')  # replace with your connection string
db = client['your-database-name']  # replace with your database name

# Route for registering new users
@app.route('/register', methods=['POST'])
def register():
    # Get username and password from request
    username = request.json.get('username')
    password = request.json.get('password')

    # If both fields are provided
    if username and password:
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Store the username and hashed password in the database
        db.users.insert_one({
            'username': username,
            'password': hashed_password,
        })

        # Return a success message
        return jsonify(message='User registered successfully!'), 200

    # If either field is not provided, return an error message
    return jsonify(message='Username and password required!'), 400


# Route for logging in existing users
@app.route('/login', methods=['POST'])
def login():
    # Get username and password from request
    username = request.json.get('username')
    password = request.json.get('password')

    # If both fields are provided
    if username and password:
        # Fetch the user from the database
        user = db.users.find_one({'username': username})

        # If the user exists and the password is correct
        if user and bcrypt.check_password_hash(user['password'], password):
            # Return a success message
            return jsonify(message='Logged in successfully!'), 200

        # If the user doesn't exist or the password is incorrect, return an error message
        return jsonify(message='Invalid username or password!'), 401

    # If either field is not provided, return an error message
    return jsonify(message='Username and password required!'), 400

# Starting the Flask application
if __name__ == '__main__':
    app.run(debug=True)
