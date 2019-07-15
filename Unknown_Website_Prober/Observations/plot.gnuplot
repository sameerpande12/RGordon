set term png size 1024,768
set output "Plots/".index."/".domain."/".filename.".png"
set title filename."    BDP_1-".bdp1." packets     BDP_2-".bdp2." packets     Drop-".drop."     mm-delay-".mmd." ms    delay_1-".delay1." us    delay_2-".delay2." us"
set ylabel "cwnd"
set xlabel "RTT"
plot "Data/".filename.".csv" u 3:2 w l notitle
