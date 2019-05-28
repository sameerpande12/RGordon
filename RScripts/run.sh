sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ingress mtu 100
gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm
ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
echo $ip
sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
sudo ./probe https://youtube.com 2000 3000 1500 0 143 48 19 -1
sudo killall wget
rm -f index*
sudo iptables --flush
