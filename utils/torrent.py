import os.path as pt
import libtorrent as lt
from time import sleep
import sys
import tempfile
import shutil
import time


def modify_magnet(magnet):
    segments = magnet.split("/")
    pass


def get_peers_count_from_magnet(magnet):
    tempdir = tempfile.mkdtemp()

    session = lt.session()

    params = {
        'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2),
        'auto_managed': True,
        'file_priorities': [0] * 5
    }

    handle = lt.add_magnet_uri(session, magnet, params)

    print("Downloading Metadata (this may take a while)")
    while not handle.has_metadata():
        print "Waiting ... "
        sleep(1)

    print("Metadata downloaded")

    peers = set()
    start = time.time()

    while not handle.is_seed() and time.time()-start < 5:
        p = handle.get_peer_info()
        for i in p:
            peers.add(i.ip)

    session.remove_torrent(handle)
    shutil.rmtree(tempdir)

    return len(peers)


if __name__ == '__main__':
    print get_peers_count_from_magnet("magnet:?xt=urn:btih:637136C082395A9888A7BFA104C7734608F2842E&dn=ssni00351mp4&tr=udp://tracker.coppersurfer.tk:6969/announce")