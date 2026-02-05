import json
import os

DATA_FILE = "user_data.json"

def load_user_data():
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    return True
