from setuptools import setup, find_packages
import subprocess
from JavPy.utils.common import version
from deployment import docker, github

if docker.in_build():
    ver = docker.generate_version()
elif github.in_publish():
    ver = github.get_current_tag()[1:].strip()
else:
    ver = version

try:
    output = subprocess.check_output("node --version", shell=True)
    assert output.decode("utf-8").startswith("v")
except Exception as ex:
    print(ex)
    print("please install Node.JS first at https://nodejs.org/en/")
    exit(0)

with open("requirements.txt") as f:
    install_req = f.read().splitlines()


setup(
    name="JavPy",
    version=ver,
    description="漂移过弯",
    author="Theodore Krypton",
    author_email="wheatcarrier@gmail.com",
    license="Apache-2.0 License",
    packages=find_packages(),
    url="https://github.com/TheodoreKrypton/JavPy",
    install_requires=install_req,
    entry_points={"console_scripts": ["javpy = JavPy.serve:serve"]},
    include_package_data=True,
    exclude_package_data={"": [".gitignore"]},
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
