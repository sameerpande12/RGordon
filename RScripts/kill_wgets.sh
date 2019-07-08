while IFS=read -r line
do
  kill -9 $line
done < indexPages$j/pids.txt
