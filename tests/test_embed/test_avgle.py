from JavPy.embed.avgle import avgle
import requests


def test():
    assert (
        requests.get(
            avgle.decode("https://avgle.com/embed/f2839fcc751e7f12679c")
        ).status_code
        == 200
    )
