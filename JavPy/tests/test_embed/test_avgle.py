from JavPy.embed.avgle import avgle
import requests
from JavPy.utils.config import proxy


def test():
    assert (
        requests.get(
            avgle.decode("https://avgle.com/embed/f2839fcc751e7f12679c"),
            proxies=proxy
        ).status_code
        == 200
    )
