FROM ubuntu:20.04

ENV PYTHONIOENCODING=utf8

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        nodejs \
        npm \
        python3-setuptools \
        git && \
    git clone --depth 1 https://github.com/TheodoreKrypton/JavPy.git && \
    cd /JavPy && \
    git submodule init && \
    git submodule update && \
    cd /JavPy/JavPy/app/webfe/ && npm install && npm run build && \
    cd /JavPy && \
    pip3 install -r requirements.txt && \
    DOCKER=1 VERSION=$(git tag --points-at HEAD | cut -c 2-) python3 setup.py install && \
    cd / && rm -rf /JavPy && \
    apt-get autoremove -y --purge \
        python3-pip \
        npm \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["javpy"]
