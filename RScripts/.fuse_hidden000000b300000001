import requests
import json
import subprocess
import time
domain = 'http://137.132.83.199:4000'
# domain = 'http://localhost:3000'
# domain='http://172.26.191.175:4000'

path="/api/worker/job"
isFree=True;

def pingServer():
    postData={'viewpoint':"Singapore"}
    headers={'Content-type':'application/json','Accept':'text/plain'}
    response = requests.post(domain+path,data=json.dumps(postData),headers=headers)
    json_response=response.json()
    if(json_response['message']=='JOB'):
        file=open("jobs.json","w+")
        file.write(json.dumps(json_response))
        file.close()
        subprocess.call(["python3 work.py jobs.json "+domain],shell=True,executable='/bin/bash')

while(True):
    time.sleep(2)
    try:
        pingServer()
    except Exception as e:
        print(e)
