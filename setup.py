# encoding: utf-8

from setuptools import setup, find_packages
import subprocess

try:
    output = subprocess.check_output("node --version")
    assert output.startswith("v")
except Exception as ex:
    print(ex)
    print("please install Node.JS first at https://nodejs.org/en/")
    exit(0)

try:
    output = subprocess.check_output("lsb_release -a")
    if "Ubuntu" in output:
        subprocess.Popen("sudo apt-get install python-libtorrent")
        subprocess.Popen("sudo apt-get install python3-libtorrent")
except Exception as ex:
    print(ex)
    print("Functions of checking torrents may be incomplete, please install python bindings of libtorrent manually")

setup(
    name='JavPy',
    version='0.1.0',
    description=(
        '漂移过弯'
    ),
    author='Theodore Krypton',
    license='MIT License',
    packages=find_packages(),
    url='https://github.com/TheodoreKrypton/JavPy',
    install_requires=[
        'requests',
        'bs4',
        'python-telegram-bot',
        'urllib3==1.23',
        'pytest',
        'flask',
        'six',
        'flask-cors',
        'gevent',
        'lxml',
    ],

)
