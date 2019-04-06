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
    version='0.2.3',
    description=(
        '漂移过弯'
    ),
    author='Theodore Krypton',
    author_email='theodorekrypton@outlook.com',
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
        'lxml',
    ],
    include_package_data=True,
    exclude_package_data={'': ['.gitignore']},
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
