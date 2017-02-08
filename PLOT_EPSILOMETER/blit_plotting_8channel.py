#!/usr/bin/env python
import time

# for Mac OSX
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import random

from matplotlib import style
style.use('ggplot')

fig = plt.figure(figsize=(30,20))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

def test_fps(use_blit=True):

    ax1.cla()
    ax1.set_title('Temperature vs. Time ')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Sensor Input (mV)')

    ax2.cla()
    ax2.set_title('Shear vs. Time ')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Sensor Input (mV)')
    
    ax3.cla()
    ax3.set_title('Acceleration vs. Time ')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Accel (g)')


    plt.ion()  # Set interactive mode ON, so matplotlib will not be blocking the window
    plt.show(False)  # Set to false so that the code doesn't stop here

    cur_time = time.time()
#    ax1.hold(True)
#    ax2.hold(True)
#    ax3.hold(True)

    x, y1, y2, y3 = [], [], [], []
    times = [time.time() - cur_time]  # Create blank array to hold time values
    y1.append(0)
    y2.append(0)
    y3.append(0)

    line1, = ax1.plot(times, y1, '.-', alpha=0.8, color="gray", markerfacecolor="red")
    line2, = ax2.plot(times, y2, '.-', alpha=0.8, color="gray", markerfacecolor="red")
    line3, = ax3.plot(times, y3, '.-', alpha=0.8, color="gray", markerfacecolor="red")

    xmin, xmax, ymin, ymax = [min(times) / 1.05, max(times) * 1.1, -5,110]
    ax1.set_xlim([xmin, xmax])
    ax2.set_xlim([xmin, xmax])
    ax3.set_xlim([xmin, xmax])
    ax1.set_ylim([ymin, ymax])
    ax2.set_ylim([10*ymin, 10*ymax])
    ax3.set_ylim([20*ymin, 20*ymax])

    fig.show()
    fig.canvas.draw()

    if use_blit:
        background1 = fig.canvas.copy_from_bbox(ax1.bbox) # cache the background
        background2 = fig.canvas.copy_from_bbox(ax2.bbox) # cache the background
        background3 = fig.canvas.copy_from_bbox(ax3.bbox) # cache the background

    tic = time.time()

    niter = 200
    i = 0
    while i < niter:

        fields = random.random() * 100

        times.append(time.time() - cur_time)
        y1.append(fields)
        y2.append(fields)
        y3.append(fields)

        # this removes the tail of the data so you can run for long hours. You can cache this
        # and store it in a pickle variable in parallel.

        if len(times) > 50:
           del y1[0]
           del y2[0]
           del y3[0]
           del times[0]

        xmin, xmax, ymin, ymax = [min(times) / 1.05, max(times) * 1.1, -5,110]

        # feed the new data to the plot and set the axis limits again
        line1.set_xdata(times)
        line1.set_ydata(y1)
        
        line2.set_xdata(times)
        line2.set_ydata(y2)
        
        line3.set_xdata(times)
        line3.set_ydata(y3)
       
        if use_blit:
            fig.canvas.restore_region(background1)    # restore background
            fig.canvas.restore_region(background2)    # restore background
            fig.canvas.restore_region(background3)    # restore background
            ax1.draw_artist(line1)                   # redraw just the points
            ax2.draw_artist(line2)                   # redraw just the points
            ax3.draw_artist(line3)                   # redraw just the points
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
        ax2.set_ylim([10*ymin, 10*ymax])
        ax3.set_ylim([20*ymin, 20*ymax])
    fps = niter / (time.time() - tic)
    print("Blit [{0:3s}] -- FPS: {1:.1f}, time resolution: {2:.4f}s".format("On" if use_blit else "Off", fps, 1/fps))
    return fps

fps1 = test_fps(use_blit=True)
