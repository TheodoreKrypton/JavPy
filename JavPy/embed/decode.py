from __future__ import absolute_import, print_function, unicode_literals

from JavPy.embed.fembed import fembed
from JavPy.embed.avgle import avgle


def decode(url):
    if "fembed" in url:
        return fembed.decode(url)
    elif "avgle" in url:
        return avgle.decode(url)
    else:
        return url
