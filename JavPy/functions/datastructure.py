import datetime
from JavPy.utils.common import try_evaluate


class AV:
    def __init__(self):
        self.code = ""
        self.video_url = ""
        self.preview_img_url = ""
        self.actress = ""
        self.release_date = None
        self.title = ""

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
        self.__release_date = None

    @property
    def release_date(self):
        return self.__release_date

    @release_date.setter
    def release_date(self, date):
        if isinstance(date, datetime.datetime):
            self.__release_date = date
        else:
            self.__release_date, _ = try_evaluate(lambda: datetime.datetime.strptime(date, "%Y-%m-%d"), None)

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
