from JavPy.sources.BaseSource import INewlyReleased
import cfscrape
from JavPy.utils.requester import spawn_many, Task
import re
from JavPy.functions.datastructure import AV
import datetime


class JavLibraryCom(INewlyReleased):

    __client = cfscrape.create_scraper()

    @classmethod
    def get_newly_released(cls, page):
        major_info_req = Task(cls.__client.get, "http://www.javlibrary.com/cn/vl_newrelease.php?mode=2&page=%d" % page)
        dates_req = Task(cls.__client.get, "http://www.javlibrary.com/cn/vl_newrelease.php?list&mode=2&page=%d" % page)
        major_info_rsp, dates_rsp = spawn_many((major_info_req, dates_req)).wait_for_all_finished()
        major_info = cls.parse_major_info(major_info_rsp)
        dates = map(lambda d: datetime.datetime.strptime(d, "%Y-%m-%d"), filter(
            lambda x: "-" in x, re.findall("<td>(.+?)</td>", dates_rsp.text)
        ))

        for i, date in enumerate(dates):
            major_info[i].release_date = date
        return major_info

    @staticmethod
    def parse_major_info(rsp):
        items = re.findall("<div class=\"video\".+?</div></div>", rsp.text, re.S)
        res = []
        for item in items:
            av = AV()
            img_url = re.search("<img src=\"(.+?)\"", item).group(1).replace("ps.jpg", "pl.jpg")
            if not img_url.startswith("http"):
                img_url = "http:" + img_url
            av.preview_img_url = img_url
            av.code = re.search("<div class=\"id\">(.+?)</div>", item).group(1)
            av.title = re.search("<div class=\"title\" >(.+?)</div>", item).group(1)
            res.append(av)
        return res


if __name__ == '__main__':
    print(JavLibraryCom.get_newly_released(1))
