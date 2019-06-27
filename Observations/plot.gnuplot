set term png
set output filename.".png"
set title filename
set ylabel "cwnd"
set xlabel "RTT"
plot filename u 3:2 w l notitle
