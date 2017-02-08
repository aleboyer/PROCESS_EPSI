#!/usr/bin/env python
import time
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

def animate(i):
    fid=open('data_c_streaming_double.txt','r')
    eof=fid.seek(0,2)
    fid.seek(eof-4*1026)
    lines=fid.read().split('\n')
    data=[int(x,0) for x in lines[1:-1]]
    ax.clear()
    ax.plot(range(len(data)),data)
    ax.set_ylim([0,500])

fig=plt.figure()
ax=fig.add_subplot(1,1,1,)

ani=animation.FuncAnimation(fig,animate,interval=10)
plt.show()


