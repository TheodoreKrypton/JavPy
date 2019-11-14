from __future__ import absolute_import, print_function, unicode_literals

from JavPy.embed.fembed import fembed
from JavPy.embed.avgle import avgle
from JavPy.embed.smartshare_tv import smartshare_tv


embeds = [fembed, avgle, smartshare_tv]


def decode(url):
    for embed in embeds:
        if embed.pattern(url):
            return embed.decode(url)
    return url
