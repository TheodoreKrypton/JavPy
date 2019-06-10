class Magnet:
    def __init__(self, url):
        self.url = url
        self.trackers = []
        self.urn = ""

        params = (s.split("=") for s in self.url.split("&"))
        for param in params:



def download_torrent(magnet_link, dst_dir):

    pass



if __name__ == '__main__':
    url = "magnet:?xt=urn:btih:D02454449497A930D41D3E5ABB1537F473AA907A&dn=%5BThZu.Cc%5DABP-813&tr=udp://tracker.coppersurfer.tk:6969/announce"
    mg = Magnet(url)
    download_torrent(mg)
