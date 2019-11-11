import requests
from JavPy.utils.ping import ping


class fvs_io:
    @staticmethod
    def decode(url):
        retry = 5
        best_latency = 99999
        best_server = ""
        while retry:
            retry -= 1
            rsp = requests.get(url, verify=False, allow_redirects=False)
            location = rsp.headers['Location']
            latency = ping(location.split("//")[1].split("/")[0])
            if latency < best_latency:
                best_latency = latency
                best_server = location
        return best_server


if __name__ == '__main__':
    print(fvs_io.decode("https://fvs.io/redirector?token=T2lWcENmRUZTNGNqR3FMellscWpSbjF1RlFLWXYwRnplRzJ3Yisvb3lDeUVMditZc2FpcTNtSi9OQ1hrRFRnSHcyTXplTmpFZlNrbjlGWnMzTG1wT3MySFVDWEdSK3p3MzZicHdrSmdvc1RReDhmdDBSa2tlcHlYR0I1Y1p2UVVsd0pjekZleU94UlB2cC9jVHByMEtTMElsMGkvazhWYUQwWT06dG9iZDZWL1MvNWE1UVM0akNqa0dPZz09"))
