import os
import json


class Config:

    user_path = os.path.expanduser("~")
    config_path = os.path.join(user_path, ".JavPy")
    if os.path.exists(os.path.join(config_path, "config.json")):
        with open(os.path.join(config_path, "config.json")) as fp:
            config = json.loads(fp.read())
    else:
        config = {
            "permitted-ip": [
                "127.0.0.1"
            ]
        }