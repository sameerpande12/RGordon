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

RUN sudo apt-get install -y python python3 python3-pip && \
    python3 -m pip install numpy && \
    sudo add-apt-repository ppa:keithw/mahimahi -y && \
    sudo apt-get update && \
    sudo apt-get install -y mahimahi && \
    sudo dpkg-reconfigure -p critical dash && \
    sudo sysctl -w net.ipv4.ip_forward=1 && \
    sudo apt-get install -y libnetfilter-queue-dev iputils-ping wget psmisc net-tools screen tmux

# make /bin/sh symlink to bash instead of dash:
RUN sudo echo "dash dash/sh boolean false" | sudo debconf-set-selections
RUN sudo DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

ADD ./RScripts/ /home/tester
ADD ./quick_dependancies.sh /home/tester

CMD ["/bin/bash"]
