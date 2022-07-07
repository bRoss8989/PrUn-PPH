import requests; import json; import pandas as pd; import numpy as np
file = open('systemcons.json','r')
cons = json.load(file)
file.close()
print(cons['UV-072'])
dijkstra = {}
start = 'OS-456'
end = 'EW-238'
complete = 0
paths = []
dijkstra[start] = 0

for x in cons[start]:
    nexthop = []
    nexthop = [start] + [x[1]]
    paths = paths + [nexthop]
    dijkstra[str(x[1])] = 1

copy2 = paths[:]

while complete == 0:
    copy2 = paths[:]
    counter1 = 0
    for x in paths:
        temp = x[-1]
        counter2 = 0
        copy = x[:]
        del(copy2[0])
        counter1 = counter1 + 1
        for y in cons[temp]:
            nexthop = []
            temp2 = y[1]
            if temp2 == end:
                print('complete')
                print(copy + [temp2])
                print('Jumps '+str(len(copy + [temp2])-1))
                complete = 1
                break
            pathlen = len(x)
            if temp2 in dijkstra.keys():
                if dijkstra[temp2] > pathlen:
                    dijkstra[temp2] = pathlen
                    nexthop = copy[:]
                    nexthop = nexthop + [temp2]
                    copy2 = copy2 + [nexthop]
                    counter2 = counter2 + 1
            else:
                dijkstra[temp2] = pathlen
                nexthop = copy[:]
                nexthop = nexthop + [temp2]
                copy2 = copy2 + [nexthop]
                counter2 = counter2 + 1
    paths = copy2[:]
