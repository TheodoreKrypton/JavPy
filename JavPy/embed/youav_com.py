from JavPy.embed.BaseEmbed import BaseEmbed
import requests
from JavPy.utils.config import proxy
import re

# according to https://www.youav.com/css/object.js
_button2server = {
    1: 7,
    2: 8,
    3: 2,
    101: 2,
    7: 4
}


class youav_com(BaseEmbed):
    @staticmethod
    def decode(url):
        rsp = requests.get(url, proxies=proxy)
        pid = re.search(r'var video_id = "(\d+)"', rsp.text).group(1)
        button = re.search(r'<button id="btn(\d+)"', rsp.text).group(1)
        if int(button) in _button2server:
            server = str(_button2server[int(button)])
        else:
            server = button
        rsp = requests.get("https://www.youav.com/ajax/hls.php?server=%s&pid=%s" % (server, pid), proxies=proxy)

        if rsp.text.startswith("http"):
            return rsp.text

        m3u8 = re.search('file: "(.+?)"', rsp.text).group(1)
        return m3u8

    @staticmethod
    def pattern(url):
        if "youav.com" in url:
            return True
        else:
            return False


if __name__ == '__main__':
    # print(youav_com.decode("https://www.youav.com/video/15022/tokyo-hot-n1338-%E6%9D%B1%E7%86%B1%E6%BF%80%E6%83%85-%E5%B1%88%E8%BE%B1%E7%BE%9E%E6%81%A5%E3%82%AF%E3%82%B9%E3%82%B3-%E7%89%B9%E9%9B%86-part7"))
    # print(requests.get("https://www.youav.com/ajax/hls.php?server=800&pid=36384").text)
    print(youav_com.decode("https://www.youav.com/video/36513/fc2ppv-1293887-%E8%B6%85%E7%A5%9E%E8%84%9A%E3%81%BF%E3%81%9D%E3%81%AE%E3%81%A1%E3%82%83%E3%82%93-j-%E6%9C%8D-%E9%BB%92%E3%83%91%E3%83%B3%E3%82%B9%E3%83%88%E3%81%A7%E7%9D%80%E8%A1%A3%E7%94%9F%E3%83%8F%E3%83%A1-%E3%82%AF%E3%83%81%E3%83%A5%E3%82%AF%E3%83%81%E3%83%A5%E6%B1%81%E3%81%BE%E3%81%BF%E3%82%8C%E4%B8%AD%E5%87%BA%E3%81%97ng%E6%97%A5%E3%81%AB%E3%83%91%E3%82%A4%E3%83%91%E3%83%B3%E3%81%BE%E3%82%93%E3%81%93%E9%AC%BC%E3%83%94%E3%82%B9%EF%BD%97%E8%86%A3%E5%A5%A5%E3%82%A8%E3%82%B0%E3%82%89%E3%82%8C%E3%82%AC%E3%82%AF%E3%82%AC%E3%82%AF%E9%80%9D%E3%81%8D%E3%81%BE%E3%81%8F%E3%82%8A"))
