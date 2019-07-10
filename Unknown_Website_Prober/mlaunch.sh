sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ingress mtu 100
gcc -Wall -o mprober mprobe.c -lnfnetlink -lnetfilter_queue -lpthread -lm


URL=$1
START=1
END=$2
DELAY1=$3
DELAY2=$4
DROP=$5
TRANSITION_POINT=$6
RTTS=$7
#Transition point is the point after which delay is changed to delay_2
mkdir -p Data
cat "0 0 0">Data/windows.csv
for (( c=$START; c<=$END; c++ ))
do
echo "0 0 0" > Data/windows$c.csv
done

echo "0 0 0" > Data/windows.csv
echo "0 0" > Data/buff.csv
for  (( i=0; i< $RTTS; i++ ))
do
	for (( j=$START; j<=$END; j++ ))
	do
		ip="$(ifconfig | grep -A 1 'ingress' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
		sudo iptables -I INPUT -p tcp -d $ip -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
		sudo ./mprober "$1" $DELAY1 $DELAY2 $TRANSITION_POINT "$j" $DROP >> Data/buff.csv
		sudo killall wget
		rm -f index*
		sudo iptables --flush
	done
	python getMax.py $i $END
	if [ `tail -n 1 Data/windows.csv | cut -d" " -f2` == "0" ]; then
	exit 0
  fi
#sudo iptables --flush
done

rm -f index*
#mkdir ../Data/fb-$2
#mv ../Data/windows* ../Data/fb-$2/

#mv windows.csv "testResults/windows-$1-$2.csv"
#sudo iptables --flush
