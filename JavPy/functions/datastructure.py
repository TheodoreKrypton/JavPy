from __future__ import absolute_import, print_function, unicode_literals
import datetime
from JavPy.utils.common import try_evaluate, update_object


class AV:
    def __init__(self):
        self.code = ""
        self.video_url = ""
        self.preview_img_url = ""
        self.actress = ""
        self.release_date = None
        self.title = ""

    def set_release_date(self, release_date):
        if isinstance(release_date, datetime.datetime):
            self.release_date = release_date
        else:
            self.release_date, _ = try_evaluate(lambda: datetime.datetime.strptime(release_date, "%Y-%m-%d"), None)

    def to_dict(self):
        return {
            "code": self.code,
            "video_url": self.video_url,
            "preview_img_url": self.preview_img_url,
            "actress": self.actress,
            "release_date": self.release_date.strftime("%Y-%m-%d") if self.release_date else "",
            "title": self.title
        }


class Brief:
    def __init__(self):
        self.code = ""
        self.preview_img_url = ""
        self.actress = ""
        self.title = ""
        self.release_date = None

    def set_release_date(self, release_date):
        if isinstance(release_date, datetime.datetime):
            self.release_date = release_date
        else:
            self.release_date, _ = try_evaluate(lambda: datetime.datetime.strptime(release_date, "%Y-%m-%d"), None)

    @staticmethod
    def reduce_briefs(briefs):
        res = {}
        without_code = []
        for brief in briefs:
            if not brief.code:
                without_code.append(brief)
            elif brief.code in res:
                update_object(res[brief.code], brief)
            else:
                res[brief.code] = brief
        return res

    def to_dict(self):
        return {
            "code": self.code,
            "preview_img_url": self.preview_img_url,
            "actress": self.actress,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d") if self.release_date else ""
        }


class Magnet:
    def __init__(self):
        self.magnet = ""
        self.description = ""
        self.peers = 0

    def to_dict(self):
        return {
            "magnet": self.magnet,
            "description": self.description
        }
