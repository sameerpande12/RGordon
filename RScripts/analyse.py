import subprocess
import os
import sys
import re

url = sys.argv[1]
folder = sys.argv[2]
numTrials = int(sys.argv[3])
threshold = 80

emuUpdated = False

subprocess.call(["mkdir -p ./Analysis/"+folder],shell=True,executable='/bin/bash')

sigma_cwnd = 0
cwnd = 0
rtt = 0
emuDrop = 100000

for i in range(numTrials):
    subprocess.call(["python3 calculate.py "+url+" "+str(numTrials)+" "+str(sigma_cwnd)+" "+str(cwnd)+" "+str(rtt)+" "+str(emuDrop)],shell=True,executable='/bin/bash')
    infile = './RData/windows.csv'
    try:
        read = open(infile,'r')
        line =[int(x) for x in read.readline().split(' ')]
        if(line[1]>80 and (not emuUpdated)):
            emuDrop = sigma_cwnd
            emuUpdated = True
        sigma_cwnd = int(line[0])
        cwnd = int(line[1])
        rtt = int(line[2])+1
        read.close()
        file = open("./Analysis/"+folder+"/"+str(rtt-1),"w+")
        for j in range(numTrials):
            read = open("./RData/windows"+str(j)+".csv","r")
            line =[int(x) for x in read.readline().split(' ')]
            read.close()
            file.write("%d\n" % line[1])
        file.close()

        for j in range(numTrials):
            subprocess.call(["ls -s ./indexPages/indexPage"+str(j)+" >> ./Analysis/"+folder+"/size.txt"],shell=True,executable='/bin/bash')



    except Exception as e:
        print(e)


path="./Analysis/"+folder+"/"
file = open(path+"analysis.txt","w+")
for i in range(numTrials):
    contents=[]
    with open(path+str(i)) as f:
        for line in f:
            contents.append( int((line.strip().split(' '))[0]))
    count = 0
    for j in contents:
        if(j>0):
            count=count+1
    file.write(str(i)+"-> "+str(count)+" "+str(len(contents))+"\n")
file.close()
