import datetime


class AV:
    def __init__(self):
        self.code = ""
        self.video_url = ""
        self.preview_img_url = ""
        self.actress = ""


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
            self.__release_date = datetime.datetime.strptime(date, "%Y-%m-%d")


class Magnet:
    def __init__(self):
        self.magnet = ""
        self.description = ""
        self.peers = 0
