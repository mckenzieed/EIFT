import json


def init(file_path):
    """
    Initialize config as a global variable.

    :param file_path: Path to config file to use for this environment. dev_config.json for dev and prod_config.json
    for production environment
    """
    global EIFT_ARTICLES_CONNECTION
    global VARIABLES
    with open(file_path, 'r') as file:
        config = json.load(file)

    VARIABLES = dict(api_key=config["VARIABLES"]["API_KEY"])
    EIFT_ARTICLES_CONNECTION = dict(user=config["DBVARIABLES"]["USER"], password=config["DBVARIABLES"]["PASSWORD"],
                                    host=config["DBVARIABLES"]["HOST"], database=config["DBVARIABLES"]["DATABASE"])