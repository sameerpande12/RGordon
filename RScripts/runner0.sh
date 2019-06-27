sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ingress mtu 100
# echo $MAHIMAHI_BASE >> a.txt
# echo $ip >> b.txt
for (( j=0; j<$2; j++ ))
do
  ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
  echo $ip
  sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
  sudo ./prober "$1" 2000 3000 1500 $j $3 $4 $5 $6 $7
  sudo killall wget
  sleep 2
  # rm -f indexPage$7/index*
  sudo iptables --flush

done
#$7 is the job id
#$2 is the trial number
#since now
