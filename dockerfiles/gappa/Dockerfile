FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends wget make cmake gcc g++ zlib1g-dev
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    wget --no-check-certificate https://github.com/lczech/gappa/archive/v0.6.0.tar.gz && \
    tar xf v0.6.0.tar.gz && \
    cd gappa-0.6.0 && \
    make && \
    cp bin/gappa /usr/local/bin

CMD ["gappa", "--help"]
