import os
import json


class Config:

    user_path = os.path.expanduser("~")
    config_path = os.path.join(user_path, ".JavPy")
    config = {}

    @classmethod
    def read_config(cls):
        with open(os.path.join(cls.config_path, "config.json")) as fp:
            cls.config = json.loads(fp.read())
        return cls.config

    @classmethod
    def save_config(cls):
        if not os.path.exists(cls.config_path):
            os.mkdir(cls.config_path)
        with open(os.path.join(cls.config_path, "config.json"), "w", encoding='utf-8') as fp:
            fp.write(json.dumps(cls.config))


if os.path.exists(os.path.join(Config.config_path, "config.json")):
    Config.read_config()
else:
    Config.config = {
        "permitted-ip": [
            "127.0.0.1",
            "192.168.0.0/16"
        ],
        "password": ""
    }
    Config.save_config()
