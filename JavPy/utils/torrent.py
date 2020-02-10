import libtorrent as lt
import time
import tempfile
import shutil
from JavPy.utils.requester import spawn
import requests
from JavPy.utils.config import proxy

__tracker_list_url = (
    "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
)
__tracker_url = ""


def __set_tracker_list(rsp):
    global __tracker_url
    __tracker_url = "".join(("&tr=" + url for url in rsp.text.split()))


spawn(requests.get, __tracker_list_url, proxies=proxy).then(__set_tracker_list)


def modify_magnet(magnet):
    while not __tracker_url:
        pass
    frags = magnet.split("&")
    base_link = "&".join(filter(lambda x: not x.startswith("tr"), frags))
    return base_link + __tracker_url


def get_peers_count_from_magnet(magnet):
    tempdir = tempfile.mkdtemp()

    session = lt.session()

    params = {
        "save_path": tempdir,
        "storage_mode": lt.storage_mode_t(2),
        "auto_managed": True,
        "file_priorities": [0] * 5,
    }

    handle = lt.add_magnet_uri(session, magnet, params)

    print("Downloading Metadata (this may take a while)")
    while not handle.has_metadata():
        print("Waiting ... ")
        time.sleep(1)

    print("Metadata downloaded")

    peers = set()
    start = time.time()

    while not handle.is_seed() and time.time() - start < 5:
        p = handle.get_peer_info()
        for i in p:
            peers.add(i.ip)

    print(peers)
    session.remove_torrent(handle)
    shutil.rmtree(tempdir)

    return len(peers)


if __name__ == "__main__":
    modified_magnet = modify_magnet(
        "magnet:?xt=urn:btih:D02454449497A930D41D3E5ABB1537F473AA907A&dn=%5BThZu.Cc%5DABP-813&tr=udp://tracker.coppersurfer.tk:6969/announce"
    )
    print(modified_magnet)
    print(get_peers_count_from_magnet(modified_magnet))
