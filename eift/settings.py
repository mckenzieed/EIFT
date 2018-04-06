import json


def init(file_path):
    """
    Initialize config as a global variable.

    :param file_path: Path to config file to use for this environment. dev_config.json for dev and prod_config.json
    for production environment
    """
    global CONFIG
    with open(file_path, 'r') as file:
        CONFIG = json.load(file)
