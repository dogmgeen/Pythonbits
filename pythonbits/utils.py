import os

def existing_directory(path):
    path = os.path.abspath(path)
    os.makedirs(path, exist_ok=True)
    return path