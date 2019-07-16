# RGordon
Localised bottlenecks for server transport layer protocol analysis.  

# Dependancies:

```quick_dependancies.sh```

# Actual Runs
1. To configure as well as run the worker

```$ cd RScripts```

```$ ./start.sh```

2. To use dummyServer for testing, follow 

```$ cd dummyServer```

```$ npm start```

# Project Structure 

# I. Scripts

## 1. ping.py
* ### Important variables
  1. numParallelJobs : number of jobs (urls) that your worker will carry out
  2. threshold : the value of cwnd after which we emulate drop
  3. defaultEmu :  100000 (*Note that the value 100000 is mutually agreed upon by both scheduler and worker. Changing this will require it to be changed on both sides. This is used to check when for the first time cwnd crossed threshold*)  
  4. viewPoint: String represents the viewpoint  
  5. nextjobid : the variable storing the minimum index of jobs which have not been assigned yet  
  6. lock: used the lock to make sure that the variable "nextjobid" could be shared among multiple parallel processses and can be updated by any of the processes without any error.

* ### Control Flow:-
  ### 1. pingServer() :
    The function performs the following things-
    1. requests for a job from the scheduler
    2. initialize appropriate number of jobs
    3. starts job represented by "nextjobid" once any of current jobs ends

  ### 2. runJob(index,data,nextjobid,lock):
    The function performs the following steps:
    1. Checks if the "mtu" provided by the server is -1. If not then use this mtu to perform the calculations
    2. If mtu = -1, then perform "mtuProbing" to get minimum mtu that works. (Begin by checking 68, since most websites work for this. Check for 1500 to check if a website works at all)
  ### 3. calculate(url,numTrials,.....):
    1. Given appropriate inputs it performs all the trials for a "single" rtt.
    2. Makes sure all the unkilled wgets are killed once all trials of single rtt are completed since (*it was observed that some wgets are not killed even if they have completed their downloads*)

## 2. mtuHelper.sh
* ```mm-link <tracefile> <tracefile> ./mtuHelper.sh <mtu_value> <url> <num_chances for wget> <subscript>```

* It applies wget on the url form mm-link shell. Gives wget specified number of chances. Saves output in "index<subscript>.html".
Used while "mtu-probing"
  
## 3. runner.sh
* ```mm-delay <delayTime> ./runner.sh <url> <trial_number> <sigma_cwnd> <cwnd> <rtt-number> <emuDrop> <job_id> <mtu-value>```
  1. Sets the mtu of the mm-delay shell. Modifies the iptables to store direct the packets to ***NFQUEUE*** numbered same as ***JOB ID***
  2. Performs calculations for ***a given RTT and a given Trial*** by calling probe.c
  3. emuDrop = 100000 **(defaultEMU)** means no drop emulated (*note that the value 100000 is hardcoded as emuDrop. do not change the value to anything else*)

### 4. probe.c
* ```./prober "<url>" <delay1> <delay2> <transition_packet> <trial_number> <sigma_cwnd> <cwnd> <rtt-number> <emuDrop> <jobID> ```

*  ***delay1***:- the delay in the nfqueue to localise the bottleneck before number of packets received in total for this rtt is less than the transition_packet

*  ***delay2***:- the delay in the nfqueue to localise the bottleneck before number of packets received in total for this rtt crosses the transition_packet

 * ***transition_packet***:- the value of sigma_cwnd which determines which delay to be used to localise the bottleneck in the mm-delay shell

* ***Implementation Details***
    1. global definitions of ***DROPWINDOW***- set to 80
    2. uses defaultEMU = 100000 to check for the case when no emulated drop occurs
    3. Creates nfqueue with id same as the job id passed to it
    4. saves the computation in the files RScripts/RData<jobID>/windows<trial_number>.csv
       windows.csv saves the value with the maximum value of cwnd
    5. wget timeout has been set to 10 and retries to 15 ( -T 10 -t 15)
    6. appends the "PID" of the wget used to the end file "RScripts/indexPages<jobID>/pids.txt

### 5. start.sh
  Peforms initial configuration
  Compiles the probe.c 
  Calls ping.py

### 6. clean.sh
  Flushes the iptables
  kills all unkilled wget and prober processes


# II. Data-

  ## 1. RData -
  The folder **"RData<jobID>/windows<trial_number>.csv"** stores a single line in the format ***"sigma_cwnd cwnd rtt_number".***

  **"RData<jobID>/window.csv"** contains a single line in the above format corresponding to the maximum cwnd value seen.

  ## 2. indexPages-
  ***"indexPages<jobID>/indexPage<trial_number>"*** saves the page downloaded by wget corresponding to given trial of the given job.

***"indexPages<jobID>/pids.txt"*** contains a list of pids of wgets started within probe.c for job with jobID
  

# III. API for Server-Worker Interaction

1. **Requesting  jobs:-**
  **POST at '<server_address>/api/worker/job'**
    ```javascript
      {'viewpoint':viewPoint}
     ```
   **Response**
   ```javascript
      {'message':"JOB",'data':[{job1},{job2},......<array of jobs>]}
    ```
   **Job-structure for jobs inside 'data'**
   ```javascript
    {
    'url':url
    
    'viewpoint': location
    
    'sigma_cwnd': the value of sigma_cwnd for rtt number "startRTT -1"
    
    'cwnd': the value for rtt number "startRTT -1" 
    
    'startRTT': the first rtt to be computed
    
    'endRTT': the last rtt to be computed
    
    'trials': number of trials to perform
    
    'start_emudrop': the value of emuDrop just before starting from "startRTT". If it is 100000 then  no emulated drop
    
    'chances_left': number of chances left (to complete its data collection) for the current job
    
    'mtu': mtu value to be used ( if -1 worker does mtu Probing for itself )
    }
    ```
    
2. **Updating Data for a single rtt:-**
    **POST at '<server_address>/api/worker/update'**
    ```javascript
      {
      'cwnd':cwnd,

      'sigma_cwnd':sigma_cwnd
 
      'last_rtt_done':(rtt whose data is being sent),
  
      'url':url,
  
      'emudrop':emuDrop  (* set to 100000 when no emuDrop *)
  
      'viewpoint': viewPoint,
      
      'max_trials': number of trials,
      
      'mtu': mtu value used
      }
      ```
      
    
3. **Updating Data Collection Completed:-**
    **POST at '<server_address>/api/worker/complete'**
    ```javascript
      {
      'last_rtt_done':(rtt whose data is being sent),
  
      'url':url,
  
      'viewpoint': viewPoint,
      
      'mtu': mtu value used
      }
      ```
      
4. **Reporting error**
    **POST at '<server_address>/api/worker/updateError'**
     ```javascript
      {
      'last_rtt_done':(rtt whose data is being sent),
  
      'url':url,
  
      'viewpoint': viewPoint,
      
      'mtu': mtu value used,
      
      'chances_left': chances left for this job
      }
       ```
  
# IV Dummy Server

``` $ cd dummyServer```

``` $ npm start```

There are various arrays named "sigma_cwnd", "cwnd",  etc. These represent values of the parameters of various jobs. 

For e.g, url[0] is url for job number 0

To send the 'n' number of jobs
  1. Fill all the arrays with corresponding data
  2. set variable **batchSize = n**
  3. Update the following part of code as follows:
    
    ```javascript
     app.post('/api/worker/job',function(req,res){

      .....

      data: [ {job0},{job1},.....,{job n-1}]

      ......

      }
     ```
# V Unknown_Website_Prober

* It consists of simpler implementation of tool which just launches tests for a given url and a network profiles.

* **network_profiles.csv** contains network profiles to be used

* **testLinks.csv** contains links that can be tested and their parameters

* **Data** folder contains data for currently running job 

* **Observations/Data** contains data of completed jobs.

* **Observations/Plots** contains plots of completed jobs. 

* **file_logs.csv** consists of logs of files with their names, url and other parameters those files were created from

* **plot.sh and plot.gnuplot** used to plot the graphs given the values of parameters and input data files
