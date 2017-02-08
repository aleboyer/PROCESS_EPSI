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

ymin, ymax = [ -3,3]
g_ymin, g_ymax = [ -3,3]

rtc_freq=32768

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

def makefft(dataBuffer,Fs):
  T,V    = dataBuffer.shape
  df       = Fs/T;                # Frequential resolution

  # hanning window to get rid of edges influence
  hanning = np.mat(0.5 * (1-np.cos(2*np.pi*np.linspace(0,T-1,T)/(T-1))));
  E=np.ones([1,V]);
  H=np.dot(hanning.T,E);
  wc=1/np.mean(np.array(hanning)**2);            # window correction factor

#TODO very BADDDD  use of matrix and np.dot ect. if time change that ALB 02/07/2017 ... 
  data=np.array(H)*np.array(dataBuffer-np.dot(np.ones([T,1]),np.mat(np.mean(dataBuffer,0))));# detrend  A2=A-mean(A)
  pspec=np.abs(np.fft.fft(data,axis=0))**2;
  pspec=pspec/T**2/df;
  spec=pspec*wc;       # spectrum where variance is sum(spec)*df
  coef = (1/Fs/T);             # duree d'un segment
  if np.mod(T,2)==0:
     k=np.linspace(-T/2*df,T/2*df-df,T);
  else:
     kp=np.linspace(df,df*np.floor(T/2),T/2);
     k=np.concatanate((-kp[::-1],np.array([0]),kp));
  spec_pos=spec[k>=0,:]
  spec_pos=spec_pos[::-1,:]
  k=k[k>=0]
  return k,spec_pos

def bitnoise_24():
    Fs    = 320    # sampling frequency
    Fn    = .5*Fs  # Nyquist frequency
    FR    = 3      # Full range
    Nb_by = 24     # number of bytes
 #= [(full range = 3V)/2^24 ]^2 / f_N where f_N =200 =#
    noise= (FR/2**Nb_by)**2 /Fn
    return noise

def bitnoise_20():
    Fs    = 320    # sampling frequency
    Fn    = .5*Fs  # Nyquist frequency
    FR    = 3      # Full range
    Nb_by = 20     # number of bytes
    noise= (FR/2**Nb_by)**2 /Fn
    return noise




#### read file

fid=open('../../data/data_c_streaming_double.txt','r')
lines=fid.read().split('\n')[1:-1]       

x= []
times = []
temp1, temp2 = [], []
shear1, shear2 = [], []
accelx, accely,accelz = [], [],[]

data=[x.split(',') for x in lines]
for item in data:
    times.append(int(item[8],0)/rtc_freq)
    temp1.append(Count2Volt_bipol(int(item[0])))
    temp2.append(Count2Volt_bipol(int(item[1])))
    shear1.append(Count2Volt_bipol(int(item[2])))
    shear2.append(Count2Volt_bipol(int(item[3])))
    accelx.append(Volt2g(Count2Volt_unipol(int(item[5],0))))
    accely.append(Volt2g(Count2Volt_unipol(int(item[6],0))))
    accelz.append(Volt2g(Count2Volt_unipol(int(item[7],0))))

times=np.array(times)
temp1=np.array(temp1)
temp2=np.array(temp2)
shear1=np.array(shear1)
shear2=np.array(shear2)
accelx=np.array(accelx)
accely=np.array(accely)
accelz=np.array(accelz)


rtc_freq=32768
Fs = rtc_freq/103 # should around 320Hz sample frequency\n",
T20s=np.floor(20*Fs)
T=times.shape[0]
nb_segment=np.floor(T/T20s)
segments_shear1 = np.zeros([T20s, nb_segment])
segments_shear2 = np.zeros([T20s, nb_segment])
segments_T1     = np.zeros([T20s, nb_segment])
segments_T2     = np.zeros([T20s, nb_segment])
segments_Ax     = np.zeros([T20s, nb_segment])
segments_Ay     = np.zeros([T20s, nb_segment])
segments_Az     = np.zeros([T20s, nb_segment])
i=0
for l in np.arange(0,nb_segment*T20s,T20s):
        segments_shear1[:,i]=shear1[l:l+T20s]
        segments_shear2[:,i]=shear2[l:l+T20s]
        segments_T1[:,i]=temp1[l:l+T20s]
        segments_T2[:,i]=temp2[l:l+T20s]
        segments_Ax[:,i]=accelx[l:l+T20s]
        segments_Ay[:,i]=accely[l:l+T20s]
        segments_Az[:,i]=accelz[l:l+T20s]
        i+=1


[k,spec_shear1]=makefft(segments_shear1,Fs)
[k,spec_shear2]=makefft(segments_shear2,Fs)
[k,spec_T1]=makefft(segments_T1,Fs)
[k,spec_T2]=makefft(segments_T2,Fs)
[k,spec_Ax]=makefft(segments_Ax,Fs)
[k,spec_Ay]=makefft(segments_Ay,Fs)
[k,spec_Az]=makefft(segments_Az,Fs)
mspec_shear1=np.mean(spec_shear1,1)
mspec_shear2=np.mean(spec_shear2,1)
mspec_T1=np.mean(spec_T1,1)
mspec_T2=np.mean(spec_T2,1)
mspec_Ax=np.mean(spec_Ax,1)
mspec_Ay=np.mean(spec_Ay,1)
mspec_Az=np.mean(spec_Az,1)

fig = plt.figure(figsize=(20,10))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

   # set up subplot 
ax1.set_title('Temperature vs. freq ')
ax1.set_ylabel('Sensor Input (V^2/Hz)')

ax2.set_title('Shear vs. freq ')
ax2.set_ylabel('Sensor Input (V^2/Hz)')

ax3.set_title('Acceleration vs. freq ')
ax3.set_xlabel('Hz')
ax3.set_ylabel('Accel (g^2/Hz)')


ax1.loglog(k,mspec_T1,'b',label="T1")
ax1.loglog(k,mspec_T2,'r',label="T2-dummy")

ax2.loglog(k,mspec_shear1,'b',label="SH1")
ax2.loglog(k,mspec_shear2,'r',label="SH2-dummy")

ax3.loglog(k,mspec_Ax,'b',label="Ax")
ax3.loglog(k,mspec_Ay,'r',label="Ay")
ax3.loglog(k,mspec_Az,'g',label="Az")

noise24= bitnoise_24();
noise20= bitnoise_20();
fs     = 320
f      = np.pi*k/fs
sinc4  = (np.sin(f)/f)**4;

ax1.loglog(k,noise24+0*k,'k',label="noise 24 bit",lw=1)
ax1.loglog(k,noise20+0*k,'k--',label="noise 20 bit",lw=1)
ax1.loglog(k,1e-13*sinc4,'c',label="sinc4")
ax1.legend()

ax2.loglog(k,noise24+0*k,'k',label="noise 24 bit",lw=1)
ax2.loglog(k,noise20+0*k,'k--',label="noise 20 bit",lw=1)
ax2.loglog(k,1e-12*sinc4,'c',label="sinc4")
ax2.legend()

ax3.loglog(k,noise24+0*k,'k',label="noise 24 bit",lw=1)
ax3.loglog(k,noise20+0*k,'k--',label="noise 20 bit",lw=1)
ax3.loglog(k,1e-8*sinc4,'c',label="sinc4")
ax3.loglog(k,45e-6**2+0*k,'y',label="spec noise",lw=1)
ax3.legend()

ax1.set_ylim([0.8*noise24,1e-10])
ax2.set_ylim([0.8*noise24,1e-10])
ax3.set_ylim([0.8*noise24,1e-6])

plt.savefig("../FIGURE/noise_plot.png")
plt.close()






