filename=$1
bdp=$2
drop=$3
mmd=$4
delay1=$5
delay2=$6
gnuplot -e "filename='$filename'; bdp='$bdp' ; drop='$drop' ; mmd='$mmd' ; delay1='$delay1' ; delay2='$delay2'" plot.gnuplot
