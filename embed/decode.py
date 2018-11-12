from fembed import fembed
from avgle import avgle


def decode(url):
    if "fembed" in url:
        return fembed.decode(url)
    else:
        return avgle.decode(url)