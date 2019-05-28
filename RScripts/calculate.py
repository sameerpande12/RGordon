import csv
import subprocess
import tcpClassify
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
    subprocess.call(["mm-delay "+ str(delayTime) + " ./runner.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
    #subprocess.call(["./multi-launch.sh "+targetURL+" 10"], shell=True, executable='/bin/bash')
except Exception as e:
    print(e)
finally:
    subprocess.call(["./clean.sh"], shell=True, executable="/bin/bash")
    #subprocess.call(["cp ../Data/windows.csv ../Windows/"+url+".csv"], shell=True, executable="/bin/bash")
