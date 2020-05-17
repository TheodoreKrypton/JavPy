from JavPy.functions.sources import Sources
from JavPy.utils.requester import submit, wait_until


class ActressInfo:
    @staticmethod
    def get_actress_info(actress):
        return wait_until([submit(source.get_actress_info, actress) for source in Sources.ActressInfo])


if __name__ == "__main__":
    print(ActressInfo.get_actress_info("唯川みさき"))
    # print(ActressInfo.get_actress_info("Eimi Fukada").to_dict())
