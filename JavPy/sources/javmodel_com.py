from JavPy.sources.BaseSource import ITranslateEn2Jp
import requests
import re
from JavPy.utils.config import proxy


class JavModelCom():
    @classmethod
    def translate2jp(cls, actress):
        url = "https://javmodel.com/jav/" + "-".join(re.split(r"\s+", actress)).lower()
        rsp = requests.get(url, proxies=proxy)
        return re.search(r"<h1 class=\"intro-title mb20\">(.+?)<br>", rsp.text).group(1)

    @classmethod
    def test(cls):
        cls.test_translate_en2jp("Nao Jinguuji")


if __name__ == "__main__":
    JavModelCom.test()
