import requests
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.utils.config import proxy


class hydrax_net(BaseEmbed):
    @staticmethod
    def decode(url):
        # rsp = requests.get(url)
        return url

    @staticmethod
    def pattern(url):
        if "hydrax.net" in url:
            return True
        return False
