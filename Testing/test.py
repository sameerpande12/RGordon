import pandas as pd
import subprocess

df_link=pd.read_csv('testLinks.csv',delim_whitespace=True)
df_link.set_index('id',inplace=True)

df_network = pd.read_csv('network_profiles.csv',delim_whitespace=True)
df_network.set_index('id',inplace = True)


def runJob(url_id,profile_id):
    url_data = df_link.loc[url_id]
    network_data=df_network.loc[profile_id]

    delayTime = network_data['mm_delay']
    print(delayTime)
    drop = network_data['drop']
    print(drop)
    bneck_delay1 = network_data['delay_1']
    print(bneck_delay1)
    bneck_delay2 = network_data['delay_2']
    print(bneck_delay2)
    bneck_transition= network_data['transition_point']
    print(bneck_transition)

    url = url_data['url']
    print(url)
    trials =url_data['trials']
    print(trials)

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

    command=("mm-delay "+str(delayTime)+" ./mlaunch.sh \""+url+"\" "+ str(trials)+" "+str(bneck_delay1)+" "+str(bneck_delay2)+" "+str(drop)+" "+str(bneck_transition))
    subprocess.call([command],shell=True,executable='/bin/bash')


runJob(0,0)
