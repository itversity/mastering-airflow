from ubuntu:18.04

RUN apt update && \
    apt install openjdk-8-jdk openssh-server -y && \
    apt install python3 python3-venv python3-pip -y && \
    apt install sudo telnet groff postgresql-client vim -y && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" itversity && \
    echo "itversity:itversity" | chpasswd && \
    adduser itversity sudo

RUN sed -i "s/%sudo\tALL=(ALL:ALL) ALL/%sudo\tALL=(ALL:ALL) NOPASSWD:ALL/g" /etc/sudoers
COPY --chown=itversity:itversity deploy.sh /deploy.sh
USER itversity
RUN python3 -m pip install jupyterlab

RUN chmod u+x /deploy.sh
CMD ["/deploy.sh"]
