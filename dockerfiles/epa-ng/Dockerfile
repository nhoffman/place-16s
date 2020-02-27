FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        autotools-dev libtool flex bison cmake wget \
        automake autoconf make gcc g++ zlib1g-dev
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    wget --no-check-certificate https://github.com/Pbdas/epa-ng/archive/v0.3.6.tar.gz && \
    tar xf v0.3.6.tar.gz && \
    cd epa-ng-0.3.6 && \
    make && \
    cp bin/epa-ng /usr/local/bin

CMD ["epa-ng", "--help"]
