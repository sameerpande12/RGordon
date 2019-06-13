import json
import multiprocessing as mp
import subprocess
import requests
import sys
import re
fileName = sys.argv[1]
server=sys.argv[2]
threshold=80
defaultEmu=100000
json_file = open(fileName)
data = json.load(json_file)

def runJob(i,data):
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
        if(chances_left<=0):
            break
        subprocess.call(["python3 calculate.py \""+url + "\" "+ str(trials)+ " "+str(sigma_cwnd )+ " "+str(cwnd )+ " "+str(rnum) +" "+ str(emuDrop)+" "+str(jobID)+" "+str(delayTime)],shell=True,executable='/bin/bash')

        infile="./RData"+str(jobID)+"/windows"+".csv"
        read=open(infile,'r')
        line=[int (x) for x in read.readline().split(' ')]
        values=line
        postData=''
        path=''
        if (values[1] == 0):
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
            postData={'cwnd':str(values[1]),'sigma_cwnd':str(values[0]),'last_rtt_done':str(values[2]),'url':url,'emudrop':str(emuDrop),'viewpoint':viewPoint,'max_trials':str(trials)}
        headers={'Content-type':'application/json','Accept':'text/plain'}
        requests.post(server+path,data=json.dumps(postData),headers=headers)
        rnum=rnum+1

if data['message']=='JOB':


    pool = mp.Pool(max(mp.cpu_count(), 5))
    print(len(data['data']))
    r=[pool.apply_async(runJob,args=[i,data['data']]) for i in range(len(data['data']))]
    p=[x.wait() for x in r]
    pool.close()
    # for i in range(len(data['data'])):
    #     runJob(i,data['data'])
    subprocess.call(["./clean.sh"],shell=True,executable='/bin/bash')
