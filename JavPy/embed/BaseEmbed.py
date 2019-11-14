from abc import ABCMeta, abstractmethod


class BaseEmbed:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def decode(url):
        pass

    @staticmethod
    @abstractmethod
    def pattern(url):
        return False
