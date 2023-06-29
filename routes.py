from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_cors import CORS
from marshmallow import Schema, fields, validate, ValidationError
from . import app, db, bcrypt
from .models import User
from .dialogflow import detect_intent
from .user_suggestions import get_top_commands
from .todo_model import ToDo
from .weather_manager import get_weather
from .image_processor import convert_to_grayscale
from .document_processor import extract_text_from_pdf
from .code_executor import execute_python_code
import openai

openai.api_key = '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'

# CORS setup
CORS(app)

# Rate limiting setup
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=6))

user_schema = UserSchema()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = user_schema.load(request.json)
        username = data.get('username')
        password = data.get('password')
    except ValidationError as err:
        return jsonify(err.messages), 400

    if username and password:
        user = User(username, password)
        user.insert()

        return jsonify(message='User registered successfully!'), 200

@app.route('/login', methods=['POST'])
def login():
    try:
        data = user_schema.load(request.json)
        username = data.get('username')
        password = data.get('password')
    except ValidationError as err:
        return jsonify(err.messages), 400

    if username and password:
        user = db.users.find_one({'username': username})

        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

        return jsonify(message='Invalid username or password!'), 401

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = jsonify({"code": e.code, "name": e.name, "description": e.description})
    response.content_type = "application/json"
    return response

# Additional routes

@app.route('/command', methods=['POST'])
@jwt_required()
def process_command():
    user_id = get_jwt_identity()
    command = request.json.get('command')

    if command:
        response = detect_intent('your-project-id', user_id, command)
        return jsonify(response=response), 200

    return jsonify(message='Command required!'), 400

@app.route('/suggestions', methods=['GET'])
@jwt_required()
def get_suggestions():
    num_suggestions = request.args.get('num', default=5, type=int)
    suggestions = get_top_commands(current_user.command_history, num_suggestions)
    return jsonify(suggestions=suggestions), 200

@app.route('/todos', methods=['GET', 'POST'])
@jwt_required()
def todos():
    if request.method == 'GET':
        todos = ToDo.objects(user=get_current_user().id)
        return jsonify(todos=[todo.to_dict() for todo in todos]), 200
    elif request.method == 'POST':
        todo = ToDo(user=get_current_user(), task=request.json.get('task')).save()
        return jsonify(todo=todo.to_dict()), 201

@app.route('/todos/<todo_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def todo(todo_id):
    todo = ToDo.objects.get_or_404(id=todo_id, user=get_current_user().id)
    if request.method == 'PUT':
        todo.update(set__task=request.json.get('task'), set__done=request.json.get('done'))
        return jsonify(todo=todo.to_dict()), 200
    elif request.method == 'DELETE':
        todo.delete()
        return '', 204

@app.route('/process_document', methods=['POST'])
@jwt_required()
def process_document():
    if 'document' not in request.files:
        return jsonify(message='No document file part'), 400
    file = request.files['document']
    if file.filename == '':
        return jsonify(message='No selected file'), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        text = extract_text_from_pdf(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(text=text), 200

@app.route('/weather', methods=['GET'])
@jwt_required()
def weather():
    city = request.args.get('city', default='New York')
    weather_data = get_weather(city, 'your_api_key_here')
    return jsonify(weather_data)

@app.route('/process_image', methods=['POST'])
@jwt_required()
def process_image():
    if 'image' not in request.files:
        return jsonify(message='No image file part'), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify(message='No selected file'), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gray_image_path = convert_to_grayscale(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify(image_path=gray_image_path), 200

@app.route('/execute_code', methods=['POST'])
@jwt_required()
def execute_code():
    code = request.form.get('code')
    if not code:
        return jsonify({'message': 'No code provided'}), 400
    output = execute_python_code(code)
    return jsonify({'output': output.decode('utf-8')}), 200

@app.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    item_id = request.json.get('item_id')
    rating = request.json.get('rating')
    if not item_id or not rating:
        return jsonify({'message': 'Missing item_id or rating'}), 400

    client = MongoClient("mongodb+srv://innoedgetech:W4UyYBXqQGRrSiNB@cluster0.mongodb.net/test")
    db = client.cherryAI
    feedback = db.feedback

    feedback.insert_one({
        'user_id': get_jwt_identity(),
        'item_id': item_id,
        'rating': rating
    })

    return jsonify({'message': 'Feedback submitted successfully'}), 200

@app.route('/generate_code', methods=['POST'])
@jwt_required()
def generate_code():
    description = request.form.get('description')
    if not description:
        return jsonify({'message': 'No description provided'}), 400
    
    prompt = f"Python function to {description}:\n"
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, temperature=0.5, max_tokens=100)

    return jsonify({'code': response.choices[0].text.strip()}), 200
@app.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    user = User(**body)
    user.hash_password()
    user.save()
    return {'id': str(user.id)}, 200

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.objects.get(email=body.get('email'))
    authorized = user.check_password(body.get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401

    access_token = create_access_token(identity=str(user.id))
    return {'token': access_token}, 200

@app.route('/command', methods=['POST'])
@jwt_required()
def process_command():
    command_text = request.json.get('command')
    response = detect_intent_texts('your-project-id', 'unique-session-id', command_text, 'en-US')
    return jsonify(response), 200

@app.route('/suggestions', methods=['GET'])
@jwt_required()
def get_suggestions():
    user_id = get_jwt_identity()
    user = User.objects.get(id=user_id)
    commands = get_top_commands(user.command_history)
    return jsonify(commands), 200

@app.route('/process_image', methods=['POST'])
@jwt_required()
def process_image():
    image = request.files['image']
    image_data = open_image(image)
    processed_image_data = resize_image(image_data, 128, 128)
    save_image(processed_image_data, 'new_image.png')
    return send_file('new_image.png', mimetype='image/png'), 200

@app.route('/generate_code', methods=['POST'])
@jwt_required()
def handle_generate_code():
    code_text = request.json.get('code_text')
    generated_code = generate_code(code_text)
    return jsonify({'code': generated_code}), 200

@app.route('/email', methods=['GET', 'POST'])
@jwt_required()
def handle_email():
    if request.method == 'GET':
        return jsonify(read_email())
    elif request.method == 'POST':
        recipient = request.json.get('recipient')
        subject = request.json.get('subject')
        body = request.json.get('body')
        send_email(recipient, subject, body)
        return jsonify({'status': 'Email sent'}), 200

@app.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    feedback_text = request.json.get('feedback')
    user_id = get_jwt_identity()
    feedback = Feedback(user_id=user_id, text=feedback_text)
    feedback.save()
    return jsonify({'status': 'Feedback submitted'}), 200




