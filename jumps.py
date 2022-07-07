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
    ## copy of paths for lower loops to ref
    copy2 = paths[:]
    counter1 = 0
    for x in paths:
        ## looking at next system from 1 starting path
        temp = x[-1]
        counter2 = 0
        ## copy path to add into if next jump has value
        copy = x[:]
        ## delete old path
        del(copy2[0])
        counter1 = counter1 + 1
        for y in cons[temp]:
            nexthop = []
            temp2 = y[1]
            ## check if system hop is final dest
            if temp2 == end:
                print('complete')
                print(copy + [temp2])
                print('Jumps '+str(len(copy + [temp2])-1))
                complete = 1
                break
            ## get current path length, check if next system has already been visted by another path
            pathlen = len(x)
            if temp2 in dijkstra.keys():
                ## check if this path is faster to this system if not then no path added back to paths, if so add system and jumps to dict
                if dijkstra[temp2] > pathlen:
                    dijkstra[temp2] = pathlen
                    nexthop = copy[:]
                    nexthop = nexthop + [temp2]
                    ## add new path with this jump in it to paths copy
                    copy2 = copy2 + [nexthop]
                    counter2 = counter2 + 1
            else:
                ## adding system and jumps to dict
                dijkstra[temp2] = pathlen
                nexthop = copy[:]
                nexthop = nexthop + [temp2]
                ## add new path with this jump in it to paths copy
                copy2 = copy2 + [nexthop]
                counter2 = counter2 + 1
    ## once this round of loops is done add all new path into paths and start the while loop over
    paths = copy2[:]
