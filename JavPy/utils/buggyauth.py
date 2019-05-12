from JavPy.utils.config import Config
import hashlib
import ipaddr
import time
import json


sessions = set()
password = Config.config['password']
hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
white_lists_ranges = [
    ipaddr.IPv4Network(ip_ranges)
    for ip_ranges in Config.config['ip-whitelist']
    if "/" in ip_ranges
]
white_lists_single = [
    ipaddr.IPAddress(ip_single)
    for ip_single in Config.config['ip-whitelist']
    if "/" not in ip_single
]
registered_cookie = set()


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


def generate_cookie(request):
    plain = "/".join((request.remote_addr, hashed_password, str(int(time.time()))))
    cookie = hashlib.sha256(plain.encode('utf-8')).hexdigest()[:24]
    registered_cookie.add(cookie)
    return cookie


def check_request(request):
    if request.method not in ['POST', 'GET']:
        return True
    if not check_ip(request.remote_addr):
        return False
    if not password:
        return True
    data = json.loads(request.data.decode('utf-8'))
    if 'userpass' not in data or data['userpass'] not in registered_cookie:
        return False
    return True


if __name__ == '__main__':
    print(check_ip("192.23456.4.6"))
