class BaseSource:
    def __init__(self):
        pass

    def search(self, code):
        pass


class SourceException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
