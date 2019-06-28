sudo sysctl net.ipv4.tcp_sack=0
sudo ifconfig ingress mtu 100
gcc -Wall -o mprober mprobe.c -lnfnetlink -lnetfilter_queue -lpthread -lm


URL=$1
START=1
END=$2
DELAY1=$3
DELAY2=$4
EMUDROP=$5

for (( c=$START; c<=$END; c++ ))
do
echo "0 0 0" > Data/windows$c.csv
done

echo "0 0 0" > Data/windows.csv
echo "0 0" > Data/buff.csv

for i in {1..50}
do
#sudo iptables -I INPUT -p tcp -d 100.64.0.2 -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
#python getmedian.py $i
	for (( j=$START; j<=$END; j++ ))
	do
		sudo iptables -I INPUT -p tcp -d 100.64.0.2 -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
		echo "--------------------------------- RTT-$i, TRIAL-$j ----------------------"
		sudo ./mprober "$1" $DELAY1 $DELAY2 1500 "$j" $EMUDROP >> Data/buff.csv
		sudo killall wget
		rm -f index*
		sudo iptables --flush
	done
python Scripts/getmedian.py $i $END
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
