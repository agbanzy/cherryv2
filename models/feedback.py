# File: /cherryAI/models/feedback.py

from mongoengine import Document, StringField, IntField

class Feedback(Document):
    """
    Model for user feedback.
    """
    task_id = StringField(required=True)
    user_id = StringField(required=True)
    rating = IntField(min_value=1, max_value=5)
    comments = StringField()
