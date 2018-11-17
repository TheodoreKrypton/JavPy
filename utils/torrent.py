import libtorrent as lt
import time


link = "magnet:?xt=urn:btih:CEED13C074063BF6F3FECA43E3297416CDD342BB&dn=ipx232&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fpublic.popcorn-tracker.org%3A6969%2Fannounce"

params = {
        "save_path": '.',
        "duplicate_is_error": True
    }

sess = lt.session()
sess.add_dht_router('router.bittorrent.com', 6881)
sess.add_dht_router('router.utorrent.com', 6881)
sess.add_dht_router('router.bitcomet.com', 6881)
sess.add_dht_router('dht.transmissionbt.com', 6881)
sess.start_dht()

handle = lt.add_magnet_uri(sess, link, params)

# waiting for metadata
while (not handle.has_metadata()):
    time.sleep(5)

# create a torrent
torinfo = handle.get_torrent_info()
torfile = lt.create_torrent(torinfo)

print(torinfo)