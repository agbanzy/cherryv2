# File: /cherryAI/models.py

from shared import db, bcrypt  # Import from shared.py instead of main.py

# Define the User model
class User(db.Document):  # Assuming you're using MongoEngine, User should be a Document
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def insert(self):
        # Insert the user into the 'users' collection
        self.save()  # Using save() method provided by MongoEngine

class Feedback(db.Document):  # Assuming Feedback is also a MongoEngine Document
    # Define fields as per your requirements
    pass