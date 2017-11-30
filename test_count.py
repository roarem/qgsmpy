import numpy as np
filepath = '/home/roar/DISKS/1/19-31_oct/4mln/code_recieved_2810/900/build/data/NPOM.dat'
with open(filepath,'r') as f:
    sl,hl = [],[]
    for line in f:
        s,h = map(int,line.split())
        if h==0:
            sl.append(s)
            hl.append(h)
            
    sl = np.asarray(sl)
    hl = np.asarray(hl)
    print(np.unique(sl,return_counts=True))


