sudo ifconfig ingress mtu 100
ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
echo $i
sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num $7
sudo ./prober "$1" 2000 3000 1500 $2 $3 $4 $5 $6 $7
#$7 is the job id
#$2 is the trial number
#since now
