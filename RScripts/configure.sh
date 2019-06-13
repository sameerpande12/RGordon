sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl net.ipv4.tcp_sack=0
gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm
