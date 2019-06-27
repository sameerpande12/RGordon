import multiprocessing as mp
import time
def runJob(i):
    for j in range(5):
        print(j)
        time.sleep(1)
    print("Ending job "+str(i))


jobs=[(i) for  i in range(100)]
pool=mp.Pool(max(mp.cpu_count(),5))
r=[]
maxJobs=5
index = 0
for i in range(maxJobs):
    r.append(pool.apply_async(runJob,args=[jobs[index]]))
    index=index+1
size = len(r)
