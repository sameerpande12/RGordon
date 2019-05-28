import csv
import subprocess
import multiprocessing as mp
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
import time
import re
import sys

url = sys.argv[1]
targetURL = "http://"+sys.argv[1]
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
    subprocess.call(["sudo sysctl -w net.ipv4.ip_forward=1"],shell=True,executable='/bin/bash')
    subprocess.call(["sudo sysctl net.ipv4.tcp_sack=0"],shell=True,executable='/bin/bash')
    subprocess.call(["sudo ifconfig ingress mtu 100"],shell=True,executable='/bin/bash')
    subprocess.call(["gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm"],shell=True,executable='/bin/bash')
except Exception as e:
    print(e)


def runTrial(Trial_Number):
    try:
        subprocess.call(["mm-delay "+ str(delayTime) + " ./runner.sh "+targetURL+" "+str(Trial_Number)], shell=True, executable='/bin/bash')

    except Exception as e:
        print(e)
    

        #subprocess.call(["cp ../Data/windows.csv ../Windows/"+url+".csv"], shell=True, executable="/bin/bash")

pool = mp.Pool(mp.cpu_count())
r=[pool.apply_async(runTrial,args=[i]) for i in range (10)]
p=[x.wait() for x in r]
pool.close
subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
