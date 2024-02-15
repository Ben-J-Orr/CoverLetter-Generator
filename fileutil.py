import json


def read_config_from_file(path='config.json'):
    with open(path, 'r') as f:
        return json.load(f)
