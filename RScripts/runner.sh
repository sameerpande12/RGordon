sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ingress mtu 100
gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm
ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
echo $i
sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num $2
sudo ./prober "$1" 2000 3000 1500 $2 143 48 19 -1
sudo killall wget
rm -f index*
sudo iptables --flush
