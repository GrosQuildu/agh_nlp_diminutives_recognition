FROM ubuntu:18.04

RUN groupadd -r user && useradd --no-log-init -r -g user user
RUN apt update && apt -y install ca-certificates \
    python3 python3-setuptools wget gnupg2 software-properties-common

RUN wget -O - http://download.sgjp.pl/apt/sgjp.gpg.key| apt-key add - && \
    apt-add-repository http://download.sgjp.pl/apt/ubuntu && \
    apt update && \
    apt -y install morfeusz2 python3-morfeusz2 && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /home/user && chown user:user -R /home/user 
ADD . /home/user/

USER user
WORKDIR /home/user/

RUN python3 ./setup.py install --user
ENV PATH="${PATH}:/home/user/.local/bin"
ENV PYTHONIOENCODING=UTF-8

CMD ["rozpoznawaczek"]