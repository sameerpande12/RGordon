numTrials=$1
for i in $(seq $numTrials)
do
     index=`expr $i - 1`
     str=$"ls -s ./indexPages/indexPage$index"
     str=$($str)
     IFS=' '
     read -ra size <<< "$str"
     if [ $index -eq 0 ]
     then
       echo $size > ./indexPages/size.txt
     else
       echo $size >> ./indexPages/size.txt
     fi
done
