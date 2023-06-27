# File: /cherryAI/shared.py

from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine

db = MongoEngine()
bcrypt = Bcrypt()
