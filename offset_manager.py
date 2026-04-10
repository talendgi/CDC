import json
import os

def load_offset(file_path):
    if not os.path.exists(file_path):
        return None, None

    with open(file_path, "r") as f:
        data = json.load(f)
        return data.get("log_file"), data.get("log_pos")


def save_offset(file_path, log_file, log_pos):
    with open(file_path, "w") as f:
        json.dump({
            "log_file": log_file,
            "log_pos": log_pos
        }, f)