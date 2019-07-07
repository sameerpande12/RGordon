sudo ifconfig ingress mtu $1
#ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
#sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num $4
echo "sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num $4"
echo "wget  --no-check-certificate -t $3 -U 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0' -O index$4.html -T 10 \"$2\""
wget  --no-check-certificate -t $3 -U 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0' -O index$4.html -T 10 "$2"
#sudo iptables --flush
