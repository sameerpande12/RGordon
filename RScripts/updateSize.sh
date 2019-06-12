numTrials=$1
jobID=$2
for i in $(seq $numTrials)
do
     index=`expr $i - 1`
     str=$"ls -s ./indexPages$jobID/indexPage$index"
     str=$($str)
     IFS=' '
     read -ra size <<< "$str"
     if [ $index -eq 0 ]
     then
       echo $size > ./indexPages$jobID/size.txt
     else
       echo $size >> ./indexPages$jobID/size.txt
     fi
done
