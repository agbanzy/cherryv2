from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from bson import ObjectId
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import User, Feedback
from utils.db import initialize_db
from utils.dialogflow_framework import detect_intent_texts
from utils.file_manager import read_file, write_file
from utils.user_suggestions import get_top_commands
from utils.image_processor import open_image, save_image, resize_image, crop_image, rotate_image
from utils.code_generator import generate_code
from email_manager import send_email, read_email

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

# Initialize the database
initialize_db(app)

@app.route('/signup', methods=['POST'])
def signup():
    # Handle signup logic here
    pass

@app.route('/login', methods=['POST'])
def login():
    # Handle login logic here
    pass

@app.route('/command', methods=['POST'])
@jwt_required()
def process_command():
    # Handle command processing logic here
    pass

@app.route('/suggestions', methods=['GET'])
@jwt_required()
def get_suggestions():
    # Handle command suggestions logic here
    pass

@app.route('/process_image', methods=['POST'])
@jwt_required()
def process_image():
    # Handle image processing logic here
    pass

@app.route('/generate_code', methods=['POST'])
@jwt_required()
def handle_generate_code():
    # Handle code generation logic here
    pass

@app.route('/email', methods=['GET', 'POST'])
@jwt_required()
def handle_email():
    # Handle email reading and sending logic here
    pass

@app.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    # Handle feedback submission logic here
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

