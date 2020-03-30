from JavPy.embed.fembed import fembed
from JavPy.embed.avgle import avgle
from JavPy.embed.smartshare_tv import smartshare_tv
from JavPy.embed.hydrax_net import hydrax_net
from JavPy.embed.playfinder_xyz import playfinder_xyz


embeds = [fembed, avgle, smartshare_tv, hydrax_net, playfinder_xyz]


def decode(url):
    for embed in embeds:
        if embed.pattern(url):
            return embed.decode(url)
    return url
