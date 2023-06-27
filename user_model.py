# File: /cherryAI/user_model.py

from .db import db

class User(db.Document):
    #...
    command_history = db.ListField(db.StringField(), default=list)
