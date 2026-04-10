import json
import os

def load_offset(filepath):
    """
    Returns (log_file, log_pos). 
    Defaults to (None, None) which starts from the current master position.
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get('log_file'), data.get('log_pos')
        except (json.JSONDecodeError, IOError):
            print(f"⚠️ Warning: Could not read offset file {filepath}. Starting fresh.")
    return None, None

def save_offset(filepath, log_file, log_pos):
    """Saves the current binlog position to a JSON file."""
    data = {
        "log_file": log_file,
        "log_pos": log_pos
    }
    # Write to a temp file then rename to ensure atomicity (prevents corruption on crash)
    temp_file = f"{filepath}.tmp"
    with open(temp_file, 'w') as f:
        json.dump(data, f)
    os.replace(temp_file, filepath)