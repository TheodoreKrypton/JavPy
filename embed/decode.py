from __future__ import absolute_import, print_function, unicode_literals

from embed.fembed import fembed
from embed.avgle import avgle


def decode(url):
    if "fembed" in url:
        return fembed.decode(url)
    else:
        return avgle.decode(url)