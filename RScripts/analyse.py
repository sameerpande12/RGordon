import subprocess
import os
import sys
import re


folder = sys.argv[1]
numTrials = int(sys.argv[2])
jobID = sys.argv[3]
threshold = 80



subprocess.call(["mkdir -p ./Analysis/"+folder+"("jobID+")"],shell=True,executable='/bin/bash')

for i in range(numTrials):
    #subprocess.call(["python3 calculate.py "+url+" "+str(numTrials)+" "+str(sigma_cwnd)+" "+str(cwnd)+" "+str(rtt)+" "+str(emuDrop)+" "+jobID],shell=True,executable='/bin/bash')
    infile = './RData'+jobID+'/windows.csv'
    try:
         read = open(infile,'r')
         line =[int(x) for x in read.readline().split(' ')]
        # if(line[1]>80 and (not emuUpdated)):
        #     emuDrop = sigma_cwnd
        #     emuUpdated = True
        # sigma_cwnd = int(line[0])
        #cwnd = int(line[1])
        rtt = int(line[2])
        read.close()
        file = open("./Analysis/"+folder+"("jobID+")"+"/"+str(rtt),"w+")
        for j in range(numTrials):
            read = open("./RData"+jobID+"/windows"+str(j)+".csv","r")
            line =[int(x) for x in read.readline().split(' ')]
            read.close()
            file.write("%d\n" % line[1])
        file.close()

        for j in range(numTrials):
            subprocess.call(["cp ./indexPages"+jobID+"/indexPage"+str(j)+"/size.txt >> ./Analysis/"+folder+"("+jobID+")"+"/size.txt"],shell=True,executable='/bin/bash')



    except Exception as e:
        print(e)


path="./Analysis/"+folder+"("+jobID+")/"
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
