from __future__ import print_function, unicode_literals, absolute_import
from JavPy.sources.BaseSource import ITranslateEn2Jp
import requests
import re


class JavModelCom(ITranslateEn2Jp):
    @classmethod
    def translate2jp(cls, actress):
        url = "https://javmodel.com/jav/" + "-".join(re.split(r"\s+", actress)).lower()
        rsp = requests.get(url)
        return re.search(r"<h1 class=\"intro-title mb20\">(.+?)<br>", rsp.text).group(1)


if __name__ == '__main__':
    print(JavModelCom.translate2jp("Aoi Akane"))
