#!/usr/bin/env python
import time
import numpy as np
import matplotlib.pyplot as plt
import numpy as np


fid=open('data_c_streaming_double.txt','r')
ax=plt.axes([.1, .1, .8, .8])
dataBuffer=np.zeros([4*1026])
plt.ion()
plt.show()
while True:
    try:
        eof=fid.seek(0,2)
        fid.seek(eof-4*1026)
        lines=fid.read().split('\n')
        data=[int(x,0) for x in lines[1:-1]]
        dataBuffer[-len(data):]=data

        plt.cla()
        ax.plot(range(4*1026),dataBuffer)
        ax.set_ylim([0,70000])
        plt.draw()
        time.sleep(0.0001) 
    except KeyboardInterrupt:
        break




