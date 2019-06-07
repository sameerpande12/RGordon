import sys
file =  open(sys.argv[1],'r')
count = 0
mlist = []
while True:
    line = file.readline()
    if not line:
        break
    mlist.append((count,line.strip().split(',')))
    count=count+1

myval = True
str1=""
str2=""
ofile=open("output.txt","a+")
for tup in mlist:
    str1 = str(tup[0])
    str2=""
    i=2
    j=len(tup[1])-2
    while(i <= j):
        str2+=tup[1][i]
        if(i<j):
            str2+=','
        i=i+1
    ofile.write(str1+" "+str2+"\n")
ofile.close()
file.close()
