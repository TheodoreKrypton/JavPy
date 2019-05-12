# encoding: utf-8

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
        with open(os.path.join(cls.config_path, "config.json"), "w") as fp:
            fp.write(json.dumps(cls.config, sort_keys=True, indent=4))

    @classmethod
    def set_config(cls, key, value):
        keys = key.split(".")
        obj = cls.config
        for key in keys[:-1]:
            if key in obj:
                obj = obj[key]
            else:
                obj[key] = {}
                obj = obj[key]
        obj[keys[-1]] = value

    @classmethod
    def get_config(cls, key):
        keys = key.split(".")
        obj = cls.config
        for key in keys:
            if key in obj:
                obj = obj[key]
            else:
                return None
        return obj


if os.path.exists(os.path.join(Config.config_path, "config.json")):
    Config.read_config()
else:
    Config.config = {
        "ip-whitelist": [
            "127.0.0.1",
            "192.168.0.0/16"
        ],
        "ip-blacklist": [

        ],
        "password": ""
    }
    Config.save_config()

