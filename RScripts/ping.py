import requests
import json
import subprocess
import time
import csv
import os
import signal
import multiprocessing as mp
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import sys
domain = 'http://10.255.255.1:4000'
# domain = 'http://137.132.83.199:4000'
# domain = 'http://localhost:3000'
# domain='http://172.26.191.175:4000'
numParallelJobs=5

path="/api/worker/job"
#isFree=True;
minimumTrials=5
threshold=80
defaultEmu=100000


def pingServer():
    postData={'viewpoint':"Singapore"}
    headers={'Content-type':'application/json','Accept':'text/plain'}
    response = requests.post(domain+path,data=json.dumps(postData),headers=headers)
    response=response.json()
    print(response)
    if(response['message']=='JOB'):
        #print(len(response['data']))
        jobNum=0
        while True:
            if(jobNum >= len(response['data'])):
                break
            pool = mp.Pool(max(mp.cpu_count(), 5))
            r=[pool.apply_async(runJob,args=[i+jobNum,response['data']]) for i in range(numParallelJobs)]
            p=[x.wait() for x in r]
            pool.close()
            subprocess.call(["./clean.sh"],shell=True,executable='/bin/bash')
            jobNum=jobNum+numParallelJobs
        #for i in range(len(response['data'])):
        #    print("Calling RunJob "+str(i))
        #    runJob(i,response['data'])


def runJob(i,data):
    # print("Entered runJob "+str(i))
    if i<len(data):
        startRTT=int(data[i]['startRTT'])
        # print("startRTT %d" %(startRTT))
        endRTT=int((data[i]['endRTT']))
        # print("endRTT %d" %(endRTT))
        emuDrop = int((data[i]['start_emudrop']))
        # print("emu %d" %(emuDrop))
        chances_left=int((data[i]['chances_left']))
        # print("chances %d" %(chances_left))
        trials=int((data[i]['trials']))
        # print("trials %d" %(trials))
        cwnd=int((data[i]['cwnd']))
        # print("cwnd %d" %(cwnd))
        sigma_cwnd=int((data[i]['sigma_cwnd']))
        # print("scwnd %d" %(sigma_cwnd))
        url=(data[i]['url'])
        # print("url "+ url)
        viewPoint=data[i]['viewpoint']
        rnum=startRTT
        jobID=i
        rnum=startRTT

        targetURL=url
        response=None
        delayTime=50
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


        for j in range(endRTT-startRTT+1):
            # print("Calling Calculate")
            calculate(url,(trials),(sigma_cwnd),(cwnd),(rnum),(emuDrop),(jobID),(delayTime))
            infile="./RData"+str(jobID)+"/windows"+".csv"
            read=open(infile,'r')
            line=[int (x) for x in read.readline().split(' ')]
            values=line
            print(line)
            postData=''
            path=''
            toBreak=False
            if (values[1] == 0):
                toBreak=True
                chances_left=chances_left-1
                postData={'last_error':'error','last_rtt_done':str(rnum),'url':url,'chances_left':str(chances_left),'viewpoint':viewPoint}
                path='/api/worker/updateError'

            else:
                path='/api/worker/update'
                if(emuDrop==defaultEmu):
                    if(values[1]>threshold):
                        emuDrop=sigma_cwnd
                cwnd=values[1]
                sigma_cwnd=values[0]
                # trials = getNewNumTrials(trials,jobID)
                # subprocess.call(["echo "+str(trials)+" >> trials.txt"],shell=True,executable='/bin/bash')
                postData={'cwnd':str(values[1]),'sigma_cwnd':str(values[0]),'last_rtt_done':str(values[2]),'url':url,'emudrop':str(emuDrop),'viewpoint':viewPoint,'max_trials':str(trials)}
                print(postData)
            headers={'Content-type':'application/json','Accept':'text/plain'}
            #print("POSTING+________________________________________________+++++++++++++++++++++++++++++++++++++++++++++")
            requests.post(domain+path,data=json.dumps(postData),headers=headers)
            if(toBreak):
                break
            rnum=rnum+1

def getNewNumTrials(trials,jobID):


    try:
        fileName='./RData'+str(jobID)+'/windows'
        cwnds=[]
        cwnds_nz=[]
        for i in range(trials):
            file = open(fileName+str(i)+".csv",'r')
            line=[int(x)  for x in file.readline().split(' ')]
            file.close()
            cwnds.append(line[1])
            if(line[1]>0):
                cwnds_nz.append(line[1])
        max_cwnd=max(cwnds)
        if(len(cwnds_nz)>0.3*len(cwnds)):
            if(max_cwnd > 10):
                values_in_range=0
                for i in cwnds_nz:
                    if(i > 0.9* max_cwnd):
                        values_in_range=values_in_range+1
                if(values_in_range > 0.2*len(cwnds)):
                    trials=trials-2
                elif(values_in_range < 0.1*len(cwnds)):
                    trials=trials+2
        else:
            trials=trials+2

        if(trials < minimumTrials ):
            trials=minimumTrials
        return trials
    except Exception as e:
        print(e)
def calculate(url,numTrials,sigma_cwnd,cwnd,rtt,emuDrop,jobID,delayTime):
    # print("Entering Calculate")
    targetURL=url
    response=None
    try:
        subprocess.call(["rm -f indexPages"+str(jobID)+"/index*"],shell=True,executable='/bin/bash')
        subprocess.call(["rm -f indexPages"+str(jobID)+"/size.txt"],shell=True,executable='/bin/bash')
        subprocess.call(["rm -f Logs"+str(jobID)+"/log*"],shell=True,executable='/bin/bash')
        subprocess.call(["mkdir -p ./RData"+str(jobID)],shell=True,executable='/bin/bash')
        subprocess.call(["mkdir -p ./Logs"+str(jobID)],shell=True,executable='/bin/bash')
        subprocess.call(["mkdir -p ./indexPages"+str(jobID)],shell=True,executable='/bin/bash')
        subprocess.call(["mkdir -p ./stats"+str(jobID)],shell=True,executable='/bin/bash')
        #subprocess.call(["sudo sysctl -w net.ipv4.ip_forward=1"],shell=True,executable='/bin/bash')
        #subprocess.call(["sudo sysctl net.ipv4.tcp_sack=0"],shell=True,executable='/bin/bash')
        #subprocess.call(["gcc -Wall -o prober ./probe.c -lnfnetlink -lnetfilter_queue -lpthread -lm"],shell=True,executable='/bin/bash')
        subprocess.call(["sudo rm ./RData"+str(jobID)+"/windows*"],shell=True,executable='/bin/bash')
        def runTrial(Trial_Number):
            # print("entering trial "+str(Trial_Number))
            try:
                subprocess.call(["mm-delay "+ str(delayTime) + " ./runner.sh \""+targetURL+"\" "+str(Trial_Number)+" "+str(sigma_cwnd)+ " "+str(cwnd) + " "+str(rtt)+" "+str(emuDrop)+" "+str(jobID)+" >> Logs"+str(jobID)+"/log"+str(Trial_Number)], shell=True, executable='/bin/bash')
                # print("Exitting trial " +str(Trial_Number))
            except Exception as e:
                print(e)

        for i in range(numTrials):
            runTrial(i)
            # print("Exitted trial "+str(i))
        windows = list()
        counter=0
        for i in range(numTrials):

            infile="./RData"+str(jobID)+"/windows"+str(i)+".csv"
            try:
                read=open(infile,'r')
                line=[int(x) for x in read.readline().split(' ')]
                windows.append((line[0],line))
                read.close()
            except Exception as e:
                print(e)

        windows.sort(key=lambda tup: tup[0], reverse=True)

        maxvalues=[]
        try:
            maxValues = windows[0][1]
            subprocess.call(["echo \""+str(maxValues[0])+" "+str(maxValues[1])+" "+str(maxValues[2]) +"\" > ./RData"+str(jobID)+"/windows.csv"],shell=True,executable='/bin/bash')
        except Exception as e:
            print(e)
            subprocess.call(["echo \""+str(0)+" "+str(0)+" "+str(rtt) +"\" > ./RData"+str(jobID)+"/windows.csv"],shell=True,executable='/bin/bash')



    except Exception as e:
        print(e)

while(True):
    time.sleep(2)
    try:
        pingServer()
    except Exception as e:
        print(e)
