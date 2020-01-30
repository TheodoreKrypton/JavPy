FROM ubuntu:18.04

ENV PYTHONIOENCODING=utf8

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip && \
    apt-get install -y --no-install-recommends nodejs && \
    pip3 install JavPy && \
    apt-get remove -y --auto-remove python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["javpy"]
