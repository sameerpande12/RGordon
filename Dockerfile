FROM ubuntu:16.04

ENV TERM linux

RUN apt-get update && \
    apt-get install -y sudo software-properties-common apt-utils dnsmasq git && \
    adduser --disabled-password tester && \
    gpasswd -a tester sudo && \
    echo "tester ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/tester && \
    chmod 0440 /etc/sudoers.d/tester

USER tester
WORKDIR /home/tester

# make /bin/sh symlink to bash instead of dash:
RUN sudo echo "dash dash/sh boolean false" | sudo debconf-set-selections
RUN sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

ADD ./RScripts /home/tester
COPY ./quick_dependancies.sh /home/tester/

CMD ["/bin/bash"]

RUN sudo apt-get update && \
	sudo apt-get install -y locales && sudo locale-gen en_US.UTF-8 && \
    sudo chmod +x /home/tester/quick_dependancies.sh && \
    sudo sh -c "./quick_dependancies.sh" && sudo rm -rf /var/lib/apt/lists/*
