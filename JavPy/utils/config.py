# encoding: utf-8

import os
import json
import six
from JavPy.utils.common import version


class Config:
    user_path = os.path.expanduser("~")
    config_path = os.path.join(user_path, ".JavPy")
    config = {}

    @classmethod
    def read_config(cls):
        if six.PY2:
            with open(os.path.join(cls.config_path, "config.json")) as fp:
                cls.config = json.loads(fp.read().decode("utf-8"))
        else:
            with open(
                os.path.join(cls.config_path, "config.json"), encoding="utf-8"
            ) as fp:
                cls.config = json.loads(fp.read())

        if "version" not in cls.config or cls.config["version"] != version:
            # fix ip address issues
            if (
                "version" not in cls.config
                and cls.config["ip-whitelist"][0] == "127.0.0.1"
                and cls.config["ip-whitelist"][1] == "192.168.0.0/16"
            ):
                cls.config["ip-whitelist"] = [
                    "127.0.0.1",
                    "10.0.0.0/8",
                    "172.16.0.0/12",
                    "192.168.0.0/24",
                ]
            cls.set_config("version", version)
            cls.save_config()

        return cls.config

    @classmethod
    def save_config(cls):
        if not os.path.exists(cls.config_path):
            os.mkdir(cls.config_path)
        with open(os.path.join(cls.config_path, "config.json"), "w") as fp:
            fp.write(json.dumps(cls.config, sort_keys=True, indent=4))

    @classmethod
    def set_config(cls, key, value):
        """
        set dictionary in an easier way:

        cls.set_config("a.b.c", "123")
        {}  => {
                    "a": {
                        "b": {
                            "c": "123"
                        }
                    }
                }
        """
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
    config = Config.read_config()

else:
    Config.config = {
        "ip-whitelist": ["127.0.0.1", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/24"],
        "ip-blacklist": [],
        "password": "",
        "version": version,
    }
    Config.save_config()
