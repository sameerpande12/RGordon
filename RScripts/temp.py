import sys
import statistics as stat
import os
import re

numTrials = int(sys.argv[1])
path = sys.argv[2]
if(len(path)>=1):
    if(path[len(path)-1]!="/"):
        path= path+"/"
file = open(path+"analysis.txt","w+")
for i in range(numTrials):
    content=[]
    nonzero_content=[]
    with open(path+str(i)) as f:
        for line in f:
            element=int((line.strip().split(' '))[0])
            content.append( element)
            if(element > 0):
                nonzero_content.append(element)
    count = len(nonzero_content)
    maximum = max(content)
    threshold = 0.1
    relevant_content=[]
    for element in nonzero_content:
        if(element > 0.9*maximum):
            relevant_content.append(element)
    file.write(str(i)+"-> "+str(count)+" "+str(len(content))+" "+str(len(relevant_content)/len(content))+"\n")
file.close()
