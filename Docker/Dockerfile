FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y python3-pip
RUN apt-get clean

RUN curl -sL "https://deb.nodesource.com/setup_10.x" | bash -
RUN apt-get install nodejs -y

RUN pip3 install JavPy

EXPOSE 8081
ENTRYPOINT ["javpy"]
