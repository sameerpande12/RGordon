#!/bin/sh

sudo sysctl -w net.ipv4.ip_forward=1
gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm
python3 ping.py
