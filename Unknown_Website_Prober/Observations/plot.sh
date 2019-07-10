filename=$1
bdp1=$2
bdp2=$3
drop=$4
mmd=$5
delay1=$6
delay2=$7
index=$8
domain=$9
mkdir -p Plots/$index/$domain
gnuplot -e "data_path='Data/';filename='$filename'; bdp1='$bdp1';bdp2='$bdp2' ; drop='$drop' ; mmd='$mmd' ; delay1='$delay1' ; delay2='$delay2'; index='$index';domain='$domain'" plot.gnuplot
