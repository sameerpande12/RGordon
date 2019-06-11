#!/bin/bash

numTrials=$1
folder=$2
mkdir -p "./Analysis/$folder/plots"
for i in $(seq $numTrials)
do
index=`expr $i - 1`
path="./Analysis/$folder"
gnuplot -e "set terminal png size 1000,500;set output '$path/plots/$index.png';plot '$path/$index' u 1 w lines"
done
