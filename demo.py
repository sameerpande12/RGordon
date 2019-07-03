import time
from multiprocessing import Process, Value, Lock

# def func(val, lock):
#     for i in range(50):
#         time.sleep(0.01)
#         with lock:
#             val.value += 1
#
# if __name__ == '__main__':
#     v = Value('i', 0)
#     lock = Lock()
#     procs = [Process(target=func, args=(v, lock)) for i in range(10)]
#
#     for p in procs: p.start()
#     for p in procs: p.join()
#
#     print (v.value)



def run(i,timeList,nextjobid,lock):
    # global procs

    maxjobs=len(timeList)
    print('enter '+str(i))
    time.sleep(timeList[i])
    print('exit '+str(i))
    with lock:
        if(nextjobid.value<=maxjobs-1):
            # jobsToRun.append(nextjobid.value)
            # procs[nextjobid.value].start()
            nextjobid.value=nextjobid.value+1

timeList=[2,2,7,12,20]
numParallelJobs=2
nextjobid=Value('i',numParallelJobs)


lock=Lock()

procs=[Process(target=run,args=(i,timeList,nextjobid,lock)) for i in range(len(timeList))]
for i in range(numParallelJobs):
    procs[i].start()

numJobsStarted=numParallelJobs
lastJobStarted=numParallelJobs-1
while True:
    if(numJobsStarted>=len(timeList)):
        break
    time.sleep(10)#in order to ensure the run function gets its fare share of the list as well
    with lock:
        count = 0
        while count<numParallelJobs and lastJobStarted<nextjobid.value:
            if(lastJobStarted>=len(timeList)-1):
                numJobsStarted=len(timeList)
                break
            lastJobStarted+=1
            procs[lastJobStarted].start()
            numJobsStarted+=1
            count = count + 1
# i=0
# for p in procs:
#     # print("about to join "+str(i))
#     p.join()
#     print("joined "+str(i))
#     i=i+1
for p in procs:
    p.join()
