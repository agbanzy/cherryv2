# File: /cherryAI/utils/file_manager.py

import os

def read_file(file_path):
    """
    Reads a text file and returns its content.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    str: The content of the file.
    """
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'r') as file:
        content = file.read()

    return content

def write_file(file_path, content):
    """
    Writes content to a text file. If the file already exists, it is overwritten.

    Parameters:
    file_path (str): The path to the file.
    content (str): The content to write to the file.
    """
    with open(file_path, 'w') as file:
        file.write(content)
