#!/usr/bin/env python
import time

# for Mac OSX
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import random

from matplotlib import style
style.use('ggplot')

fig = plt.figure(figsize=(30,20))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

ymin, ymax = [ -3,3]
g_ymin, g_ymax = [ -3,3]

rtc_freq=32768

bufferSize=3200

#======================#
# check out doc AD7124; using unipolar, gain 1, sync4,N=24 bits
# code=2^N * Ain(Volts) /Full_Range
#======================#
def Count2Volt_unipol(count,N=24,Full_Range=2.5,Gain=1):
    Vin=Full_Range*np.array(count)/2**N/Gain;
    return Vin.tolist();

def Count2Volt_bipol(count,N=24,Full_Range=2.5,Gain=1):
    Vin=Full_Range/Gain*(np.array(count)/2**(N-1)-1);
    return Vin.tolist();

def Volt2g(V,offset=1.65):
    #1000 mV/g check out kionics
    #gin=1e-3.*(V-offset);
    g_in=(np.array(V)-offset)/.66;
    #g_in=(np.array(V)-offset);
    return g_in.tolist()





def test_fps(use_blit=True):

    fid=open('../../data/data_c_streaming_double.txt','r')
    eof=fid.seek(0,2)
    fid.seek(eof-465);
   
    # set up subplot 
    ax1.cla()
    ax1.set_title('Temperature vs. Time ')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Sensor Input (V)')

    ax2.cla()
    ax2.set_title('Shear vs. Time ')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Sensor Input (V)')
    
    ax3.cla()
    ax3.set_title('Acceleration vs. Time ')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Accel (g)')

    # show fig and enable interactive mode so we can do something else 
    plt.ion()  # Set interactive mode ON, so matplotlib will not be blocking the window
    plt.show(False)  # Set to false so that the code doesn't stop here
    
    cur_time = time.time()
    ax1.hold(True)
    ax2.hold(True)
    ax3.hold(True)
  
    line_init=fid.read().split('\n')[:-2][2].split(',')
    x= []
    times = []
    temp1, temp2 = [], []
    shear1, shear2 = [], []
    accelx, accely,accelz = [], [],[]
    #times = [time.time() - cur_time]  # Create blank array to hold time values
    temp1.append(Count2Volt_unipol(int(line_init[0])))
    temp2.append(Count2Volt_unipol(int(line_init[1])))
    shear1.append(Count2Volt_unipol(int(line_init[2])))
    shear2.append(Count2Volt_unipol(int(line_init[3])))
    accelx.append(Volt2g(Count2Volt_bipol(int(line_init[5]))))
    accely.append(Volt2g(Count2Volt_bipol(int(line_init[6]))))
    accelz.append(Volt2g(Count2Volt_bipol(int(line_init[7]))))
    times.append(int(line_init[8])/rtc_freq)
    #print(times)
    line11, = ax1.plot(times, temp1, '.-', alpha=0.8, color="gray", markerfacecolor="red")
    line12, = ax1.plot(times, temp2, '.-', alpha=0.8, color="gray", markerfacecolor="blue")
    line21, = ax2.plot(times, shear1, '.-', alpha=0.8, color="gray", markerfacecolor="red")
    line22, = ax2.plot(times, shear2, '.-', alpha=0.8, color="gray", markerfacecolor="blue")
    line31, = ax3.plot(times, accelx, '.-', alpha=0.8, color="gray", markerfacecolor="red")
    line32, = ax3.plot(times, accely, '.-', alpha=0.8, color="gray", markerfacecolor="blue")
    line33, = ax3.plot(times, accelz, '.-', alpha=0.8, color="gray", markerfacecolor="green")
    #print(len(times))
    xmin, xmax = [0, bufferSize*103/rtc_freq]  # define by hand 103 sample because the nember of cycle between each "sample" is 103 
    ax1.set_xlim([xmin, xmax])
    ax2.set_xlim([xmin, xmax])
    ax3.set_xlim([xmin, xmax])
    ax1.set_ylim([ymin, ymax])
    ax2.set_ylim([ymin, ymax])
    ax3.set_ylim([g_ymin, g_ymax])



    fig.show()
    fig.canvas.draw()

    if use_blit:
        background1 = fig.canvas.copy_from_bbox(ax1.bbox) # cache the background
        background2 = fig.canvas.copy_from_bbox(ax2.bbox) # cache the background
        background3 = fig.canvas.copy_from_bbox(ax3.bbox) # cache the background

    tic = time.time()

    niter = 2000
    i = 0
    lenline=75
    while i < niter:
        cur_pos=fid.tell()
        eof=fid.seek(0,2);
        if (eof-cur_pos)>2*lenline:
          fid.seek(cur_pos)
          lines=fid.read().split('\n')
          data=[x.split(',') for x in lines[1:-1]]
          #times += list(times[-1] + np.arange(len(data))+(time.time()-cur_time)/len(data) )
          for item in data:
              times.append(int(item[8],0)/rtc_freq)
              temp1.append(Count2Volt_bipol(int(item[0])))
              temp2.append(Count2Volt_bipol(int(item[1])))
              shear1.append(Count2Volt_bipol(int(item[2])))
              shear2.append(Count2Volt_bipol(int(item[3])))
              accelx.append(Volt2g(Count2Volt_unipol(int(item[5],0))))
              accely.append(Volt2g(Count2Volt_unipol(int(item[6],0))))
              accelz.append(Volt2g(Count2Volt_unipol(int(item[7],0))))
          #print(times)
          # print(y)
          # this removes the tail of the data so you can run for long hours. You can cache this
          # and store it in a pickle variable in parallel.

          if len(times) > bufferSize:
             del times[:-bufferSize]
             del temp1[:-bufferSize]
             del temp2[:-bufferSize]
             del shear1[:-bufferSize]
             del shear2[:-bufferSize]
             del accelx[:-bufferSize]
             del accely[:-bufferSize]
             del accelz[:-bufferSize]
   
          #xmin, xmax, ymin, ymax = [min(times) / 1.05, max(times) * 1.1, 0,500]
          xmin, xmax = [times[0], times[-1]]

          ax1.set_xlim([xmin, xmax])
          ax2.set_xlim([xmin, xmax])
          ax3.set_xlim([xmin, xmax])
          # feed the new data to the plot and set the axis limits again

          line11.set_xdata(times)
          line12.set_xdata(times)
          line11.set_ydata(temp1)
          line12.set_ydata(temp2)

          line21.set_xdata(times)
          line22.set_xdata(times)
          line21.set_ydata(shear1)
          line22.set_ydata(shear2)

          line31.set_xdata(times)
          line32.set_xdata(times)
          line33.set_xdata(times)
          line31.set_ydata(accelx)
          line32.set_ydata(accely)
          line33.set_ydata(accelz)
  
          ax1.set_xlim([xmin, xmax])
          ax2.set_xlim([xmin, xmax])
          ax3.set_xlim([xmin, xmax])
          #ax1.axis([xmin, xmax,ymin, ymax])          
          #ax2.axis([xmin, xmax,ymin, ymax])          
          #ax3.axis([xmin, xmax,g_ymin, g_ymax])          
 
          if use_blit:
              fig.canvas.restore_region(background1)    # restore background
              fig.canvas.restore_region(background2)    # restore background
              fig.canvas.restore_region(background3)    # restore background
              ax1.draw_artist(line11)                   # redraw just the points
              ax1.draw_artist(line12)                   # redraw just the points
              ax2.draw_artist(line21)                   # redraw just the points
              ax2.draw_artist(line22)                   # redraw just the points
              ax3.draw_artist(line31)                   # redraw just the points
              ax3.draw_artist(line32)                   # redraw just the points
              ax3.draw_artist(line33)                   # redraw just the points
              fig.canvas.blit(ax1.bbox)                # fill in the axes rectangle
              fig.canvas.blit(ax2.bbox)                # fill in the axes rectangle
              fig.canvas.blit(ax3.bbox)                # fill in the axes rectangle
          else:
              fig.canvas.draw()

          i += 1

          ax1.set_xlim([xmin, xmax])
          ax2.set_xlim([xmin, xmax])
          ax3.set_xlim([xmin, xmax])

          ax1.set_ylim([ymin, ymax])
          ax2.set_ylim([ymin, ymax])
          ax3.set_ylim([g_ymin, g_ymax])

    fps = niter / (time.time() - tic)
    return fps,data

fps1,data = test_fps(use_blit=True)

