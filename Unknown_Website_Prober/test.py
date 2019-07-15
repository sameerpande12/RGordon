import pandas as pd
import subprocess
import re
import sys
import os
subprocess.call(["sudo sysctl -w net.ipv4.ip_forward=1"],shell=True,executable='/bin/bash')

df_link=pd.read_csv('testLinks.csv',delim_whitespace=True)
df_link.set_index('id',inplace=True)

df_network = pd.read_csv('network_profiles.csv',delim_whitespace=True)
df_network.set_index('id',inplace = True)


def runJob(url_id,profile_id):
    url_data = df_link.loc[url_id]
    network_data=df_network.loc[profile_id]

    delayTime = (int)(network_data['mm_delay'])
    print(delayTime)
    drop = (int)(network_data['drop'])
    print(drop)
    bneck_delay1 = (int)(network_data['delay_1'])
    print(bneck_delay1)
    bneck_delay2 = (int)(network_data['delay_2'])
    print(bneck_delay2)
    bneck_transition= (int)(network_data['transition_point'])
    print(bneck_transition)
    bdp1 = (int)(network_data['BDP1'])
    print(bdp1)
    bdp2 = (int)(network_data['BDP2'])
    print(bdp2)

    url = url_data['url']
    print(url)
    trials =(int)(url_data['trials'])
    print(trials)
    fname = url_data['name']
    print(fname)
    rtts=(int)(url_data['rtts'])
    print(rtts)

    type = (int)(url_data['type'])
    print(type)

    response = None
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

    if int(pingTime/2) >= delayTime:
        delayTime = 1
    elif pingTime == -1:
        delayTime = delayTime
    else:
        delayTime = delayTime - int(pingTime/2)

    command=("mm-delay "+str(delayTime)+" ./mlaunch.sh \""+url+"\" "+ str(trials)+" "+str(bneck_delay1)+" "+str(bneck_delay2)+" "+str(drop)+" "+str(bneck_transition)+" "+str(rtts))
    subprocess.call([command],shell=True,executable='/bin/bash')

    command="cp Data/windows.csv Observations/Data/"+fname+"-"+str(profile_id)+".csv"
    subprocess.call([command],shell=True,executable='/bin/bash')

    os.chdir("Observations")
    # command="echo "+fname+"-"+str(profile_id)+".csv  "+url+" "+str(drop)+" "+str(delayTime)+" "+str(bneck_delay1)+" "+str(bneck_delay2)+" "+str(bdp1)+" "+str(bdp2)+" "+str(bneck_transition)+" >> file_logs.csv"
    # subprocess.call([command],shell=True,executable='/bin/bash')

    command = "./plot.sh "+str(fname)+"-"+str(profile_id)+" "+str(bdp1)+" "+str(bdp2)+" "+str(drop)+" "+str(delayTime)+" "+str(bneck_delay1)+" "+str(bneck_delay2)+" "+str(type)+" "+str(fname)
    subprocess.call([command],shell=True,executable='/bin/bash')
    os.chdir("..")

# for i in range(10):
#     if(i>4):
#         for j in range(5):
#             runJob(i,j+3)
# index = (int)(sys.argv[1])
# for i in [index,index+1,index+2]:
#     for j in range(5):
#         runJob(i,j+3)

runJob(53,3)
