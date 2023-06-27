# File: /cherryAI/__init__.py

from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize Flask app
app = Flask(__name__)

# Configure JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # replace with your secret key

# Initialize Bcrypt and JWT
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Connect to MongoDB database
client = MongoClient('your-connection-string')  # replace with your connection string
db = client['your-database-name']  # replace with your database name
