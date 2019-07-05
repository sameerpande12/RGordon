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
from multiprocessing import Process,Value,Lock
# domain = 'http://10.255.255.1:4000'
# domain = 'http://137.132.83.199:4000'
domain = 'http://localhost:3000'
# domain='http://172.26.191.175:4000'
numParallelJobs=2

path="/api/worker/job"

minimumTrials=5
threshold=80
defaultEmu=100000
viewPoint="Singapore"
def pingServer():
    postData={'viewpoint':viewPoint}
    headers={'Content-type':'application/json','Accept':'text/plain'}
    response = requests.post(domain+path,data=json.dumps(postData),headers=headers)
    response=response.json()
    print(response)
    if(response['message']=='JOB'):
        numParallelJobs=2
        numMaxJobs= len(response['data'])
        lock=Lock()
        nextjobid=Value('i',numParallelJobs-1)#set for initializing the initial batche to the numParallel job size
        procs=[Process(target=runJob,args=(i,response['data'],nextjobid,lock)) for i in range(numMaxJobs)]


        numJobsStarted=0
        lastJobStarted=-1# contains the id (0 based indexing of the last job started)
        while True:
            if(numJobsStarted >= numMaxJobs):# >= instead of == just to be on safe side
                break
            with lock:
                count = 0
                while count < numParallelJobs and lastJobStarted < nextjobid.value:
                    if(lastJobStarted >= numMaxJobs-1):
                        numJobsStarted=numMaxJobs
                        break
                    lastJobStarted+=1
                    procs[lastJobStarted].start()
                    numJobsStarted+=1
                    count = count + 1

            time.sleep(10)#to make sure the runJob function gets enough chances to acquire lock on nextjobid
        for p in procs:
            p.join()


def runJob(i,data,nextjobid,lock):
    print("Entered runJob "+str(i))
    maxJobID=len(data)-1
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
        mtu = int(data[i]['mtu'])
        viewPoint=data[i]['viewpoint']

        rnum=startRTT
        jobID=i
        rnum=startRTT

        targetURL=url
        response=None
        delayTime=50

        if(mtu==-1):
            try:
                subprocess.check_output("mm-delay 1 ./mtuHelper.sh {} {} {} {}".format(1500,url,2,jobID),shell=True,executable='/bin/bash')
                mtu=getMinMTU(url,68,1500,jobID)
            except Exception as e:
                mtu = -1

        if(mtu==-1):
            print("Returning error because faulty website jobID-{}".format(jobID))
            postData={'last_error':'error','last_rtt_done':str(rnum),'url':url,'chances_left':str(chances_left),'viewpoint':viewPoint}
            path='/api/worker/updateError'
            headers={'Content-type':'application/json','Accept':'text/plain'}
            #print("POSTING+________________________________________________+++++++++++++++++++++++++++++++++++++++++++++")
            requests.post(domain+path,data=json.dumps(postData),headers=headers)
        else:## all this done only in the case of valid mtu is possible
            print("mtu test for 1500 successful. Testing for {} value for job {}".format(mtu,jobID))
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
                calculate(url,(trials),(sigma_cwnd),(cwnd),(rnum),(emuDrop),(jobID),(delayTime),(mtu))
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


                    # subprocess.call(["wget --no-check-certificate -t 15 -U 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0' -O indexPages"+str(jobID)+"/index.html -T 10 \""+url+"\""],shell=True,executable='/bin/bash')
                    # page_size = os.path.getsize("indexPages"+str(jobID)+"/index.html")
                    # print("Expected page size:-"+str(page_size))## The idea was dropped because page_size turned out to be zero on single wget for a website which was blocked by NUS but when run multiple times it actually fetched a page in one of 10 trials.
                    #Hence checking page_size = 0 for single wget is not a good way to chek if the page gives error or not
                    max_size=0
                    for i in range(trials):
                        try:
                            temp_size = os.path.getsize("indexPages"+str(jobID)+"/indexPage"+str(i))
                            if(temp_size > max_size):
                                max_size=temp_size
                        except Exception as e:
                            print(e)
                    print("For rtt="+str(j)+" max_page size ="+str(max_size))
                    if( max_size ==0 ):
                        postData={'last_error':'error','last_rtt_done':str(rnum),'url':url,'chances_left':str(chances_left),'viewpoint':viewPoint}
                        path='/api/worker/updateError'
                    else:
                        postData={'last_rtt_done':str(rnum),'viewpoint':viewPoint,'url':url,'mtu':str(mtu)}
                        path = '/api/worker/complete'

                    # postData={'last_error':'error','last_rtt_done':str(rnum),'url':url,'chances_left':str(chances_left),'viewpoint':viewPoint}
                    # path='/api/worker/updateError'

                else:
                    path='/api/worker/update'
                    if(emuDrop==defaultEmu):
                        if(values[1]>threshold):
                            emuDrop=sigma_cwnd
                    cwnd=values[1]
                    sigma_cwnd=values[0]
                    # trials = getNewNumTrials(trials,jobID)
                    # subprocess.call(["echo "+str(trials)+" >> trials.txt"],shell=True,executable='/bin/bash')
                    postData={'cwnd':str(values[1]),'sigma_cwnd':str(values[0]),'last_rtt_done':str(values[2]),'url':url,'emudrop':str(emuDrop),'viewpoint':viewPoint,'max_trials':str(trials),'mtu':str(mtu)}
                    # print(postData)
                headers={'Content-type':'application/json','Accept':'text/plain'}
                #print("POSTING+________________________________________________+++++++++++++++++++++++++++++++++++++++++++++")
                requests.post(domain+path,data=json.dumps(postData),headers=headers)
                if(toBreak):
                    break
                rnum=rnum+1
            ### END OF ALL QUERIED RTTS OF THE GIVEN URL
        with lock:
            if(nextjobid.value <= maxJobID):
                nextjobid.value=nextjobid.value+1

def getMinMTU(url,lower_lim,upper_lim,jobID):

    if(lower_lim == upper_lim):
        return lower_lim
    midMTU = (int)((lower_lim + upper_lim)/2)
    # print("About to test for {}".format(midMTU))
    isValidMTU= True
    try:
        subprocess.check_output("mm-delay 1 ./mtuHelper.sh {} {} {} {}".format(midMTU,url,2,jobID),shell=True,executable='/bin/bash')
        # print("Successful Test")
    except Exception as e:
        #print(e)
        # print("Failed Test")
        isValidMTU=False

    if(isValidMTU):
        # print("Calling for {}, {}".format(lower_lim,midMTU))
        return getMinMTU(url,lower_lim,midMTU,jobID)
    else:
        print("Calling for {}, {}".format(midMTU+1,upper_lim))
        return getMinMTU(url,midMTU+1,upper_lim,jobID)


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
def calculate(url,numTrials,sigma_cwnd,cwnd,rtt,emuDrop,jobID,delayTime,mtu):
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
        subprocess.call(["sudo rm -f ./RData"+str(jobID)+"/windows*"],shell=True,executable='/bin/bash')
        def runTrial(Trial_Number):
            # print("entering trial "+str(Trial_Number))
            try:
                subprocess.call(["mm-delay "+ str(delayTime) + " ./runner.sh \""+targetURL+"\" "+str(Trial_Number)+" "+str(sigma_cwnd)+ " "+str(cwnd) + " "+str(rtt)+" "+str(emuDrop)+" "+str(jobID)+" "+str(mtu)+" >> Logs"+str(jobID)+"/log"+str(Trial_Number)], shell=True, executable='/bin/bash')
                # print("Exitting trial " +str(Trial_Number))
            except Exception as e:
                print(e)

        for i in range(numTrials):
            runTrial(i)
            # print("Exitted trial "+str(i))
        history_loc="History/job-"+str(jobID)+"/rtt-"+str(rtt)+"/"
        subprocess.call(["mkdir -p "+history_loc],shell=True,executable='/bin/bash')
        subprocess.call(["cp -r indexPages"+str(jobID)+" RData"+str(jobID)+" "+history_loc],shell=True,executable='/bin/bash')

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
