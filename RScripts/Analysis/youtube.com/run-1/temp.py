import sys
import statistics as stat
import os
import re

numTrials = int(sys.argv[1])
file = open("analysis.txt","w+")
for i in range(numTrials):
    contents=[]
    nonzero_content=[]
    with open(str(i)) as f:
        for line in f:
            element=int((line.strip().split(' '))[0])
            contents.append( element)
            if(element > 0):
                nonzero_content.append(element)
    count = len(nonzero_content)
    cv = 0
    if (count > 1):
        cv = (stat.stdev(nonzero_content)/(stat.mean(nonzero_content)))
    file.write(str(i)+"-> "+str(count)+" "+str(len(contents))+" "+str(cv)+"\n")
file.close()
