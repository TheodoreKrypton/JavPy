from abc import ABCMeta, abstractmethod


class ISearchByCode:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def search_by_code(cls, code):
        pass


class ISearchByActress:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def search_by_actress(cls, actress, up_to):
        pass


class IGetBrief:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def get_brief(cls, code):
        pass


class ISearchMagnet:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def search_magnet(cls, code):
        pass


class IHistoryNames:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def get_history_names(cls, actress):
        pass


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
