from JavPy.utils.config import Config
import hashlib
import ipaddr


sessions = set()
hashed_password = hashlib.sha256(Config.config['password'].encode('utf-8')).hexdigest()
white_lists_ranges = [ipaddr.IPv4Network(ip_ranges) for ip_ranges in Config.config['permitted-ip'] if "/" in ip_ranges]
white_lists_single = [ipaddr.IPAddress(ip_single) for ip_single in Config.config['permitted-ip'] if "/" not in ip_single]


def check_password(hashed):
    if hashed_password == hashed:
        return True
    return False


def check_ip(ip):
    try:
        ip = ipaddr.IPAddress(ip)
        return bool(sum(map(lambda ip_range: ip in ip_range, white_lists_ranges)) or ip in white_lists_single)
    except ValueError:
        return False


if __name__ == '__main__':
    print(check_ip("192.23456.4.6"))
