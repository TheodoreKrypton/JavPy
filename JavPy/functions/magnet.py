from JavPy.functions.sources import Sources


class Magnet:
    @staticmethod
    def get_magnet(code):
        return Sources.Magnet[0].search_magnet(code)


if __name__ == '__main__':
    print(Magnet.get_magnet("ABP-123"))
