import datetime
from JavPy.utils.common import noexcept, assign
from typing import Union, Optional, List


class AV:
    __slots__ = ['code', 'video_url', 'preview_img_url', 'actress', '__release_date', 'title']

    def __init__(self):
        self.code = ""
        self.video_url = ""
        self.preview_img_url = ""
        self.actress = ""
        self.__release_date = None  # type: Optional[datetime.datetime]
        self.title = ""

    @property
    def release_date(self) -> datetime.datetime:
        return self.__release_date

    @release_date.setter
    def release_date(self, date: Union[str, datetime.datetime]):
        if isinstance(date, datetime.datetime):
            self.__release_date = date
        else:
            self.__release_date = noexcept(
                lambda: datetime.datetime.strptime(date, "%Y-%m-%d"), None
            )

    def to_dict(self):
        return {
            "code": self.code,
            "video_url": self.video_url,
            "preview_img_url": self.preview_img_url,
            "actress": self.actress,
            "release_date": self.release_date.strftime("%Y-%m-%d")
            if self.release_date
            else "",
            "title": self.title,
        }


class Brief:
    __slots__ = ['code', 'preview_img_url', 'actress', 'title', '__release_date']

    def __init__(self):
        self.code = ""
        self.preview_img_url = ""
        self.actress = ""
        self.title = ""
        self.__release_date = None

    @property
    def release_date(self) -> datetime.datetime:
        return self.__release_date

    @release_date.setter
    def release_date(self, date: Union[str, datetime.datetime]):
        if isinstance(date, datetime.datetime):
            self.__release_date = date
        else:
            self.__release_date = noexcept(
                lambda: datetime.datetime.strptime(date, "%Y-%m-%d"), None
            )

    @staticmethod
    def reduce_briefs(briefs: List['Brief']) -> dict:
        res = {}
        without_code = []
        for brief in briefs:
            if not brief.code:
                without_code.append(brief)
            elif brief.code in res:
                assign(res[brief.code], brief)
            else:
                res[brief.code] = brief
        return res

    def to_dict(self):
        return {
            "code": self.code,
            "preview_img_url": self.preview_img_url,
            "actress": self.actress,
            "title": self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d")
            if self.release_date
            else "",
        }


class Magnet:
    __slots__ = ['magnet', 'description', 'peers']

    def __init__(self):
        self.magnet = ""
        self.description = ""
        self.peers = 0

    def to_dict(self):
        return {"magnet": self.magnet, "description": self.description}


class Actress:
    __slots__ = ['birth_date', 'img', 'height', 'weight', 'other']

    def __init__(self):
        self.birth_date = None
        self.img = ""
        self.height = ""
        self.weight = ""
        self.other = {
            "history_names": []
        }

    def to_dict(self):
        return {
            "birth_date": self.birth_date,
            "img": self.img,
            "height": self.height,
            "weight": self.weight,
            "other": self.other,
        }
