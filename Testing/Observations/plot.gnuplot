set term png
set output "Plots/".filename.".png"
set title filename." BDP1-".bdp1." BDP2-".bdp2." Drop-".drop." mm-delay-".mmd." delay_1-".delay1." delay_2-".delay2
set ylabel "cwnd"
set xlabel "RTT"
plot "Data/".filename.".csv" u 3:2 w l notitle
