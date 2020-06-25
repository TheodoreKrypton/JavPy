import os
import json
from packaging import version
import pkg_resources

try:
    javpy_version = pkg_resources.get_distribution("JavPy").version
except pkg_resources.DistributionNotFound:
    from JavPy.utils.common import version as javpy_version


class Config:
    user_path = os.path.expanduser("~")
    config_path = os.path.join(user_path, ".JavPy")
    config = {}

    @classmethod
    def read_config(cls):
        with open(os.path.join(cls.config_path, "config.json"), encoding="utf-8") as fp:
            cls.config = json.loads(fp.read())

        if "version" not in cls.config or version.parse(cls.config["version"]) <= version.parse("0.3.3"):
            cls.config["proxy"] = ""
            cls.set_config("version", javpy_version)
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
    if config["version"] != javpy_version:
        Config.set_config("version", javpy_version)
        Config.save_config()
        config = Config.read_config()

else:
    Config.config = {
        "ip-whitelist": ["127.0.0.1", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
        "ip-blacklist": [],
        "password": "",
        "proxy": "",
        "version": javpy_version,
    }
    Config.save_config()

if Config.config["proxy"]:
    proxy = {
        'http': Config.config["proxy"],
        'https': Config.config["proxy"]
    }
else:
    proxy = None
