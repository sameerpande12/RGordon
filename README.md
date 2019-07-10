# RGordon
Localised bottlenecks for server transport layer protocol analysis.  

# Dependancies:
```quick_dependancies.sh```

# Actual Runs
1. To configure as well as run the worker
```$ cd RScripts```
```$ ./start.sh```
2. To use dummyServer for testing, follow 
```cd dummyServer```
```npm start```

# Project Structure -> RScripts

## A) ping.py
### Important variables
1. numParallelJobs : number of jobs (urls) that your worker will carry out
2. threshold : the value of cwnd after which we emulate drop
3. defaultEmu :  100000 (*Note that the value 100000 is mutually agreed upon by both scheduler and worker. Changing this will require it to be changed on both sides. This is used to check when for the first time cwnd crossed threshold*)
4.viewPoint: String represents the viewpoint
5.nextjobid : the variable storing the minimum index of jobs which have not been assigned yet
6. lock: used the lock to make sure that the variable "nextjobid" could be shared among multiple parallel processses and can be updated by any of the processes without any error.

### Control Flow:-
### 1.pingServer() :
The function performs the following things-
1. requests for a job from the scheduler
2. initialize appropriate number of jobs
3. starts job represented by "nextjobid" once any of current jobs ends

### 2.runJob(index,data,nextjobid,lock):
The function performs the following steps:
1. Checks if the "mtu" provided by the server is -1. If not then use this mtu to perform the calculations
2. If mtu = -1, then perform "mtuProbing" to get minimum mtu that works. (Begin by checking 68, since most websites work for this. Check for 1500 to check if a website works at all)
### 3.calculate(url,numTrials,.....):
1. Given appropriate inputs it performs all the trials for a "single" rtt.
2. Makes sure all the unkilled wgets are killed once all trials of single rtt are completed since (*it was observed that some wgets are not killed even if they have completed their downloads*)

## B) mtuHelper.sh
```mm-link <tracefile> <tracefile> ./mtuHelper.sh <mtu_value> <url> <num_chances for wget> <subscript>```
It applies wget on the url form mm-link shell. Gives wget specified number of chances. Saves output in "index<subscript>.html".
Used while "mtu-probing"
  
## C)runner.sh
```mm-delay <delayTime> ./runner.sh <url> <trial_number> <sigma_cwnd> <cwnd> <rtt-number> <emuDrop> <job_id> <mtu-value>```
1. Sets the mtu of the mm-delay shell. Modifies the iptables to store direct the packets to ***NFQUEUE*** numbered same as ***JOB ID***
2. Performs calculations for ***a given RTT and a given Trial*** by calling probe.c
3. emuDrop = 100000 **(defaultEMU)** means no drop emulated (*note that the value 100000 is hardcoded as emuDrop. do not change the value to anything else*)

### D)


