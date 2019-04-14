# encoding: utf-8

from __future__ import print_function, unicode_literals, absolute_import
# from builtins import str
from JavPy.sources.BaseSource import IHistoryNames
import requests
from JavPy.utils.common import urlencode, try_evaluate
import re


class AVHelpMemoWiki(IHistoryNames):
    current_name_pattern = re.compile(u"名前：(.+?)\n")
    history_name_pattern = re.compile(u"別名.*?：(.+?)\n")
    kana_pattern = re.compile(u"（.+?）")
    move_pattern = re.compile(u"href=\"(.+?)\".+?へ移動する")

    @classmethod
    def get_history_names(cls, actress):
        url = "https://av-help.memo.wiki/d/" + urlencode(actress, 'EUC-JP')
        rsp = requests.get(url)
        html = rsp.text
        pre = re.search(r"<pre.+?</pre>", html, re.S)

        if pre is None:
            moved_to = re.search(cls.move_pattern, html)
            print(moved_to)
            moved_to = moved_to.group(1)
            rsp = requests.get(moved_to)
            pre = re.search(r"<pre.+?</pre>", rsp.text, re.S)

        pre = pre.group(0)

        names = [re.sub(cls.kana_pattern, "", name) for name in re.search(
            cls.history_name_pattern, pre
        ).group(1).split(u"／")]

        current_name = re.search(cls.current_name_pattern, pre)
        if current_name:
            current_name = re.sub(cls.kana_pattern, "", current_name.group(1))
            names.append(current_name)

        return names


if __name__ == '__main__':
    print(AVHelpMemoWiki.get_history_names("唯川みさき"))
