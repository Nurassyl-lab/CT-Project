#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 15:11:15 2022

@author: 0810981
"""

import scipy.io.wavfile as wavf
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.fft import fft, fftfreq
import math


name = "sin400Hz.txt"
f = open(name, "r")
arr = []
for line in f:
    arr.append(int(line))

sampleRate = 2379

duration = int(math.floor(len(arr)) / sampleRate)#calculate duration in seconds

d = sampleRate * duration#d represents number of samples that perfectly correspond to duration
                        #because I physically cannot record exact time in integer seconds
                        #time will be always (for example 20.1 sec or 15.7 sec)
                        #since it is not an integer it will always add some extra value 
                        #d helps to set a range optimal for an integer duration

arr = arr[0:d]#modify data 
time = np.linspace(0, duration, d)#create time array for plotting

length = len(arr)
if length < 400:
    print("DATA TOO SMALL")
    sys.exit(1)

fig1 = plt.figure(1)
title = name + " | Full data"
plt.title(title)
plt.plot(time, arr)
plt.ylabel("analog signal (analogRead())")
plt.xlabel("time(sec)")
title+=".png"
fig1.savefig(title, dpi = fig1.dpi)

fig2 = plt.figure(2)
title = name + " | Full data (small range)"
plt.title(title)
plt.ylabel("analog signal (analogRead())")
plt.xlabel("time(sec)")
plt.plot(time[int(length/2):int(length/2)+100],arr[int(length/2):int(length/2)+100])
title += "_ZOOMED.png"
fig2.savefig(title, dpi = fig2.dpi)

scaled = []
for i in arr:
    x = (i - 512) * 64
    if x < 0:
        scaled.append(x + 1)
    elif x > 0:
        scaled.append(x-1)
    else:
        scaled.append(0)    

fig3 = plt.figure(3)
title = name + " | Scaled data 16-bit PCM (small range)"
plt.title(title)
plt.ylabel("signal | int-16")
plt.xlabel("time(sec)")
plt.plot(time[int(length/2):int(length/2)+100], scaled[int(length/2):int(length/2)+100])
title += "_ZOOMED.png"
fig3.savefig(title, dpi = fig3.dpi)

scaled = np.array(scaled)

scaled = scaled[0:d]
wavf.write('400Hz.wav', sampleRate, scaled.astype(np.int16))
# Number of samples in normalized_tone
N = sampleRate * duration#approxiame duration is 191 seconds
yf = fft(scaled)
xf = fftfreq(N, 1 / sampleRate)
if len(yf) > len(xf):
    yf = yf[0:len(xf)]
else : xf = xf[0:len(yf)]
fig4 = plt.figure(4)
title = name + " | FFT"
plt.title(title)
plt.ylabel("Magnitude")
plt.xlabel("Frequency (Hz)")
plt.plot(xf, np.abs(yf))
title+=".png"
fig4.savefig(title, dpi = fig4.dpi)