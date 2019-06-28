set term png
set output filename.".png"
set title filename." BDP-".bdp." Drop-".drop." mm-delay-".mmd." delay_1-".delay1." delay_2-".delay2
set ylabel "cwnd"
set xlabel "RTT"
plot filename u 3:2 w l notitle
