from JavPy.embed.fembed import fembed
from JavPy.embed.avgle import avgle
from JavPy.embed.smartshare_tv import smartshare_tv
from JavPy.embed.hydrax_net import hydrax_net
from JavPy.embed.playfinder_xyz import playfinder_xyz
from JavPy.embed.javcl_me import javcl_me


embeds = [avgle, hydrax_net]


def decode(url):
    for embed in embeds:
        if embed.pattern(url):
            return embed.decode(url)
    return url


if __name__ == '__main__':
    print(decode("https://playfinder.xyz/v/7q970kx-wog#poster=https://findercdn.me/cdn/movie/s1no-1style-ssni-351-yoshitaka-nene-the-adviser-of-the-bad-female-teacher-was-a-humiliation-tennis-club-with-only-devil-pupils_1542526435.png"))