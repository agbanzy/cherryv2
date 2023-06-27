# File: /cherryAI/file_manager.py

import json
import csv
import os
import shutil
from PIL import Image

def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext == '.txt':
        with open(file_path, 'r') as file:
            return file.read()
    elif ext == '.json':
        with open(file_path, 'r') as file:
            return json.load(file)
    elif ext == '.csv':
        with open(file_path, 'r') as file:
            return list(csv.reader(file))
    elif ext in ['.jpg', '.png', '.bmp']:
        return Image.open(file_path)
    else:
        raise ValueError(f'Unsupported file type: {ext}')

def write_file(file_path, content):
    _, ext = os.path.splitext(file_path)
    if ext == '.txt':
        with open(file_path, 'w') as file:
            file.write(content)
    elif ext == '.json':
        with open(file_path, 'w') as file:
            json.dump(content, file)
    elif ext == '.csv':
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(content)
    elif ext in ['.jpg', '.png', '.bmp']:
        content.save(file_path)
    else:
        raise ValueError(f'Unsupported file type: {ext}')

def copy_file(source_path, destination_path):
    shutil.copy2(source_path, destination_path)

def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)

