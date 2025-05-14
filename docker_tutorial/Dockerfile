FROM ubuntu:22.04

RUN apt-get update &&\
    apt-get install -y libgl1-mesa-dev && \
    apt-get install -y python3.11-dev && \
    apt-get install -y python3-pip && \
    apt-get install -y wget

RUN python3.11 -m pip install minizinc && \
    python3.11 -m pip install minizinc[dzn] && \
    python3.11 -m pip install z3-solver && \
    python3.11 -m pip install matplotlib

RUN mkdir cdmo

WORKDIR ./cdmo

ARG MINIZINC_VERSION=2.7.2

RUN wget https://github.com/MiniZinc/MiniZincIDE/releases/download/$MINIZINC_VERSION/MiniZincIDE-$MINIZINC_VERSION-bundle-linux-x86_64.tgz
RUN tar -xvf MiniZincIDE-$MINIZINC_VERSION-bundle-linux-x86_64.tgz
ENV PATH="${PATH}:/cdmo/MiniZincIDE-$MINIZINC_VERSION-bundle-linux-x86_64/bin"

ADD . .

RUN echo "python3.11 /cdmo/main.py" >> ~/.bashrc

CMD ["/bin/bash"]
