from abc import ABCMeta, abstractmethod


class ISearchByCode:
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_by_code(self, code):
        pass


class ISearchByActress:
    __metaclass__ = ABCMeta

    @abstractmethod
    def search_by_actress(self, actress, allow_many_actresses, up_to):
        pass


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
