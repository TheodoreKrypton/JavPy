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
    def search_by_actress(cls, actress, allow_many_actresses, up_to):
        pass


class ISearchMagnet:
    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def search_magnet(cls, code):
        pass


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
