# File: /cherryAI/todo_model.py

from .db import db

class ToDo(db.Document):
    user = db.ReferenceField('User')
    task = db.StringField(required=True)
    done = db.BooleanField(default=False)
