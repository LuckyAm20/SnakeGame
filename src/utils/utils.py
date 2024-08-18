import json
import os


def load_highscore():
    filename = 'highscore.json'
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump({'highscore': 0}, file)
        return 0

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data.get('highscore', 0)
    except json.JSONDecodeError:
        return 0
