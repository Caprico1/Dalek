import json

CONFIG_NAME = "dalek-config.json"

def get_api_key():
    with open(CONFIG_NAME, 'r') as config_file:
        config = config_file

        config_dict = json.load(config)

        return config_dict['api_key']
