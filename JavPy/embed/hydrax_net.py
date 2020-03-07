import requests
from JavPy.embed.BaseEmbed import BaseEmbed
from JavPy.utils.config import proxy


class hydrax_net(BaseEmbed):
    @staticmethod
    def decode(url):
        rsp = requests.get(url)
        print(rsp.text)
        return url

    @staticmethod
    def pattern(url):
        if "hydrax.net" in url:
            return True
        return False


if __name__ == "__main__":
    print(smartshare_tv.decode("https://smartshare.tv/v/kdrx7f3z2ernewj"))
