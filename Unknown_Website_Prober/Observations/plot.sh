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
input=Data/$filename.csv
y='-1'
x='-1'
while IFS= read -r line
do
  z=`echo $line|cut -d ' ' -f 1`
  if [ $z -gt 1500 ]
  then
    y=`echo $line|cut -d ' ' -f 2`
    x=`echo $line|cut -d ' ' -f 3`
    break
  fi
done < "$input"

gnuplot -e "data_path='Data/';filename='$filename'; bdp1='$bdp1';bdp2='$bdp2' ; drop='$drop' ; mmd='$mmd' ; delay1='$delay1' ; delay2='$delay2'; index='$index';domain='$domain';x='$x';y='$y'" plot.gnuplot
