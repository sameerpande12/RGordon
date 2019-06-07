#input format is  python3 calculate.py <url-without http eg. www.youtube.com> <numTrials>

import csv
import subprocess
import os
import signal
import multiprocessing as mp
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
import time
import re
import sys

url = sys.argv[1]
numTrials=int(sys.argv[2])
sigma_cwnd= (sys.argv[3])
cwnd = (sys.argv[4])
rtt = (sys.argv[5])
emuDrop = (sys.argv[6])

targetURL = sys.argv[1]
response = None
delayTime = 50

try:
    response = subprocess.check_output(
        ['ping', '-c', '1', url],
        stderr=subprocess.STDOUT,  # get all output
        universal_newlines=True  # return string not bytes
    )
except subprocess.CalledProcessError:
    response = None

if response == None:
    pingTime = -1
else:
    pingTime = float(re.search('time=.*', response).group().replace(" ms", '')[5:])

if int(pingTime/2) >= 50:
    delayTime = 1
elif pingTime == -1:
    delayTime = 50
else:
    delayTime = 50 - int(pingTime/2)

print(targetURL, delayTime)

try:
    subprocess.call(["rm -f index*"],shell=True,executable='/bin/bash')
    subprocess.call(["mkdir -p ./RData"],shell=True,executable='/bin/bash')
    #subprocess.call(["sudo sysctl -w net.ipv4.ip_forward=1"],shell=True,executable='/bin/bash')
    #subprocess.call(["sudo sysctl net.ipv4.tcp_sack=0"],shell=True,executable='/bin/bash')
    #subprocess.call(["gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm"],shell=True,executable='/bin/bash')
    subprocess.call(["sudo rm ./RData/windows*"],shell=True,executable='/bin/bash')
except Exception as e:
    print(e)


def runTrial(Trial_Number):
    try:
        subprocess.call(["mm-delay "+ str(delayTime) + " ./runner.sh \""+targetURL+"\" "+str(Trial_Number)+" "+sigma_cwnd+ " "+cwnd + " "+rtt+" "+emuDrop+" >> log"+str(Trial_Number)], shell=True, executable='/bin/bash')

    except Exception as e:
        print(e)


        #subprocess.call(["cp ../Data/windows.csv ../Windows/"+url+".csv"], shell=True, executable="/bin/bash")

pool = mp.Pool(mp.cpu_count())
r=[pool.apply_async(runTrial,args=[i]) for i in range(numTrials)]
p=[x.wait() for x in r]
#r=[pool.apply(runTrial,args=[i]) for i in range(numTrials)]
pool.close
subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")


####calculating the max from here on"
windows = list()
counter=0
for i in range(numTrials):
    infile="./RData/windows"+str(i)+".csv"
    read=open(infile,'r')
    line=[int(x) for x in read.readline().split(' ')]

    windows.append((line[0],line))
    read.close()

windows.sort(key=lambda tup: tup[0], reverse=True)

maxValues = windows[0][1]
subprocess.call(["echo \""+str(maxValues[0])+" "+str(maxValues[1])+" "+str(maxValues[2]) +"\" > ./RData/windows.csv"],shell=True,executable='/bin/bash')

#sys.stdout.flush()
