# File: /cherryAI/models/task.py

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://innoedgetech:W4UyYBXqQGRrSiNB>@cluster0.mongodb.net/test")
db = client.cherryAI
tasks = db.tasks

def add_task(user_id, task):
    """
    Add a new task to the user's task list.

    Parameters:
    user_id (str): The ID of the user.
    task (str): The description of the task.

    Returns:
    str: The ID of the new task.
    """
    task = tasks.insert_one({
        'user_id': user_id,
        'task': task,
        'completed': False
    })
    return str(task.inserted_id)

def delete_task(user_id, task_id):
    """
    Delete a task from the user's task list.

    Parameters:
    user_id (str): The ID of the user.
    task_id (str): The ID of the task.
    """
    tasks.delete_one({
        '_id': ObjectId(task_id),
        'user_id': user_id
    })

def get_tasks(user_id):
    """
    Retrieve the user's task list.

    Parameters:
    user_id (str): The ID of the user.

    Returns:
    list: The user's task list.
    """
    user_tasks = tasks.find({
        'user_id': user_id
    })
    return list(user_tasks)
