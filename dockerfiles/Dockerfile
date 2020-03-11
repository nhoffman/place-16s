FROM python:3.8-buster

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        autotools-dev libtool flex bison cmake wget \
        automake autoconf make gcc g++ zlib1g-dev

RUN pip3 install pandas==1.0.1 fastalite==0.3

# epa v0.3.6
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    wget --no-check-certificate https://github.com/Pbdas/epa-ng/archive/v0.3.6.tar.gz && \
    tar xf v0.3.6.tar.gz && \
    cd epa-ng-0.3.6 && \
    make && \
    cp bin/epa-ng /usr/local/bin

# gappa v0.6.0
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    wget --no-check-certificate https://github.com/lczech/gappa/archive/v0.6.0.tar.gz && \
    tar xf v0.6.0.tar.gz && \
    cd gappa-0.6.0 && \
    make && \
    cp bin/gappa /usr/local/bin

# infernal 1.1.3
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    wget --no-check-certificate http://eddylab.org/infernal/infernal-1.1.3-linux-intel-gcc.tar.gz && \
    tar xf infernal-1.1.3-linux-intel-gcc.tar.gz && \
    cp infernal-1.1.3-linux-intel-gcc/binaries/* /usr/local/bin

CMD ["echo", "epa-ng v0.3.6\ngappa v0.6.0\npandas 1.0.1"]
