FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3-setuptools
RUN apt-get install -y curl
RUN apt-get install -y unzip
RUN apt-get clean

RUN alias python=python3.7

RUN curl -sL "https://deb.nodesource.com/setup_10.x" | bash -
RUN apt-get install nodejs -y

RUN curl -o "JavPy.zip" "https://codeload.github.com/TheodoreKrypton/JavPy/zip/master"
RUN unzip "JavPy.zip"
RUN rm -f "JavPy.zip"

WORKDIR JavPy-master
RUN python3 setup.py install

EXPOSE 8081
ENTRYPOINT ["javpy"]
