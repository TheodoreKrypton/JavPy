from JavPy.sources.BaseSource import ISearchMagnet
import requests
import re
import bs4
from JavPy.functions.datastructure import Magnet
from JavPy.utils.config import proxy


class JavBusCom(ISearchMagnet):
    @classmethod
    def search_magnet(mcs, code):
        url = "https://www.javbus.com/" + code
        rsp = requests.get(url, proxies=proxy)

        if not rsp.status_code == 200:
            return None

        gid = re.search(r"var gid = (\d+?);", rsp.text).group(1)
        uc = re.search(r"var uc = (\d+?);", rsp.text).group(1)
        img = re.search(r"var img = '(.+?)';", rsp.text).group(1)

        querystring = {"gid": gid, "lang": "zh", "img": img, "uc": uc}

        headers = {"Referer": url}

        rsp = requests.get(
            "https://www.javbus.com/ajax/uncledatoolsbyajax.php",
            headers=headers,
            params=querystring,
            proxies=proxy
        )
        bs = bs4.BeautifulSoup(rsp.text, "lxml")
        trs = bs.find_all(name="tr")

        res = []

        for tr in trs:
            magnet = tr.td.a.attrs["href"]
            description = tr.td.next_sibling.next_sibling.a.text.strip()
            mgnt = Magnet()
            mgnt.magnet = magnet
            mgnt.description = description

            res.append(mgnt)

        return res

    @classmethod
    def test(mcs):
        mcs.test_search_magnet("ABP-123")


if __name__ == '__main__':
    JavBusCom.test()