# encoding: utf-8

from setuptools import setup, find_packages
import subprocess

try:
    output = subprocess.check_output("node --version")
    assert output.decode('utf-8').startswith("v")
except Exception as ex:
    print(ex)
    print("please install Node.JS first at https://nodejs.org/en/")
    exit(0)

setup(
    name='JavPy',
    version='0.2.0',
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
    include_package_data=True,
    exclude_package_data={'': ['.gitignore']}
)
