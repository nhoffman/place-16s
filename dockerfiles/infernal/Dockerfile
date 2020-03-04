FROM ubuntu:18.04
RUN apt-get update -y && apt-get install -y wget
RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    wget --no-check-certificate http://eddylab.org/infernal/infernal-1.1.3-linux-intel-gcc.tar.gz && \
    tar xf infernal-1.1.3-linux-intel-gcc.tar.gz && \
    cp infernal-1.1.3-linux-intel-gcc/binaries/* /usr/local/bin

CMD ["cat", "/usr/local/src/infernal-1.1.3-linux-intel-gcc/README"]
