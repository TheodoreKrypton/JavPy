FROM ubuntu:18.04

ENV PYTHONIOENCODING=utf8

RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:jonathonf/python-3.6 && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3.6-minimal && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get install -y --no-install-recommends python3-setuptools && \
    pip3 install wheel && \
    pip3 install JavPy && \
    apt-get remove -y --auto-remove software-properties-common python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["javpy"]
