while IFS= read -r line
do
  kill -9 $line
done < indexPages$1/pids.txt
