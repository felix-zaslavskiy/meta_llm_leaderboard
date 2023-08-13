import os
import pickle

def load_previous_data(filepath):
    print("Change tracking: " + filepath)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as file:
            return pickle.load(file)
    return {}

def save_current_data(data, filepath):
    with open(filepath, 'wb') as file:
        pickle.dump(data, file)

def track_changes(current_data, previous_data):
    had_change = False
    for key in current_data:
        if key not in previous_data:
            print(f'New model: {key}')
            had_change = True
        elif current_data[key] != previous_data[key]:
            print(f'Model {key} changed from {previous_data[key]} to {current_data[key]}')
            had_change = True

    for key in previous_data:
        if key not in current_data:
            print(f'Model {key} was removed')
            had_change = True

    if not had_change:
        print("No changes")

    return had_change
