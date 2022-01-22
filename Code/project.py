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

f = open("SeriesDataRecording.txt", "r")
arr = []
for line in f:
    arr.append(int(line))

length = len(arr)
sampleRate = 2378

if length < 400:
    print("DATA TOO SMALL")
    sys.exit(1)

fig1 = plt.figure(1)
plt.title("Full data")
plt.plot(arr)
plt.ylabel("analog signal (analogRead())")
plt.xlabel("number of data")
fig1.savefig("FullData.png", dpi = fig1.dpi)

fig2 = plt.figure(2)
plt.title("Full data (small range)")
plt.ylabel("analog signal (analogRead())")
plt.xlabel("number of data")
plt.plot(arr[int(length/2):int(length/2)+100])
fig2.savefig("Zoomed.png", dpi = fig2.dpi)

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
plt.title("Scaled data 16-bit PCM (small range)")
plt.ylabel("signal | int-16")
plt.xlabel("number of data")
plt.plot(scaled[int(length/2):int(length/2)+100])
fig3.savefig("ScaledZoomed.png", dpi = fig3.dpi)

scaled = np.array(scaled)
wavf.write('result2.wav', sampleRate, scaled.astype(np.int16))
# Number of samples in normalized_tone
N = sampleRate * 191#approxiame duration is 191 seconds
yf = fft(scaled)
xf = fftfreq(N, 1 / sampleRate)
yf = yf[0:len(xf)]

fig4 = plt.figure(4)
plt.title("FFT")
plt.ylabel("Magnitude")
plt.xlabel("Frequency")
plt.plot(xf, np.abs(yf))
fig4.savefig("FFT.png", dpi = fig4.dpi)