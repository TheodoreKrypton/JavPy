from sources.BaseSource import BaseSource, SourceException
import requests
import re
import bs4
import json
from embed.decode import decode
from functions.datastructure import AV


class JavMostCom(BaseSource):
    def __init__(self):
        BaseSource.__init__(self)
        self.select_part_regex = re.compile(r"select_part\((.+?)\)")
        self.data_regex = re.compile(r"get_source/\",(.+?)\}", re.S)
        self.value_regex = re.compile(r"value: \"(.+?)\",")
        self.sound_regex = re.compile(r"sound: \"(.+?)\",")

    def search(self, code):
        url = "https://www5.javmost.com/" + code
        rsp = requests.get(url, verify=False)
        if rsp.status_code != 200:
            raise SourceException(code + " not found in javmost.com")

        img = "http:" + re.search("<meta property=\"og:image\" content=\"(.+?)\"", rsp.text).group(1)

        bs = bs4.BeautifulSoup(rsp.text, "lxml")

        button = bs.find(name='li', attrs={'class': 'active'})
        params = re.search(self.select_part_regex, button.a.attrs['onclick']).group(1)
        e, t, a, o, l, r, d = [x.replace("\'", "") for x in params.split(",")]

        data = re.search(self.data_regex, rsp.text).group(1)
        value = re.search(self.value_regex, data).group(1)
        sound = re.search(self.sound_regex, data).group(1)

        url = "https://www5.javmost.com/get_code/"
        rsp = requests.post(url, data={
            "code": value
        }, verify=False)
        _code = rsp.text

        url = "https://www5.javmost.com/get_source/"
        rsp = requests.post(url, data={
            "group": t,
            "part": e,
            "code": l,
            "code2": r,
            "code3": d,
            "value": value,
            "sound": sound,
            "code4": _code
        }, verify=False)

        json_obj = json.loads(rsp.text)
        url = json_obj["data"][0]

        url = decode(url)

        av = AV()
        av.preview_img_url = img
        av.video_url = url
        av.code = code

        return av