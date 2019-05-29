ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
echo $i
sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num $2
sudo ./prober "$1" 2000 3000 1500 $2 $3 $4 $5 -1
