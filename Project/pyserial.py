#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 13:26:49 2021

@author: jason
"""

import serial, time
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.signal as ss
import pandas as pd
    
#%%
def plotMag(omega, H, title, xlim, ylim):
    plt.figure(figsize = (11,6))
    H_db = H_db = 20*np.log10(np.abs(H))
    plt.plot(omega, H_db, color = "black", linewidth = 2)
    plt.xlim(xlim)
    plt.xlabel("Frequency (Hz)", fontsize = 12)
    plt.ylim(ylim)
    plt.ylabel("Relative level (dB)", fontsize = 12)
    plt.grid(True, which = "both", color = "black", linestyle = (0, (5, 10)))
    plt.title(title + '\n', fontsize = 16)
    #plt.savefig(title + ".pdf")
    plt.show()

#%%
def print_coeff(coeff, filtname):
    print("<{}>".format(filtname))
    print("b_0:%20d"%coeff[0], " | ", "a_0%20d"%coeff[3])
    print("b_1:%20d"%coeff[1], " | ", "a_1%20d"%coeff[4])
    print("b_2:%20d"%coeff[2], " | ", "a_2%20d"%coeff[5])

#%%
def comp_arr(data1, data2):
    equal = np.array_equal(data1, data2, equal_nan=True)
    
    if not equal:
        diff = np.subtract(data1,data2)
        mse = np.square(diff).mean()
        mae = np.sum(np.absolute(diff))/len(diff)
        diff_idx = np.argwhere(diff!=0).flatten()
        diff = diff[diff!=0]
        print("The ", len(diff_idx), " differences are:")
        print("  index: ", diff_idx)
        print("  diff:  ", diff)
        print("  mae:   ", mae)
        print("  mse:   ", mse)
        return diff_idx, diff, mae, mse
    else:
        print("Exactly the same!")

#%%
fs, data = wavfile.read('Doraemon Sound Effect.wav')
#data_nor = data/(2**15-1)

#%%
#fs = 44100, fc = 7000, Q = 0.7071, Gain = 6
#https://www.earlevel.com/main/2010/12/20/biquad-calculator/
#Bandpass filter

b0 = 0.372644957421416
b1 = 0.
b2 = -0.372644957421416
a0 = 1
a1 = -0.6807382689367104
a2 = 0.25471008515716803

omega, H = ss.freqz([b0,b1,b2], [a0,a1,a2], worN=50000, fs=fs)
plotMag(omega, H, "Response of biquad-highshelf", xlim = [0, fs/2], ylim = [-100, 10])
a = np.array([a0, a1, a2])
b = np.array([b0, b1, b2])

#%%
m1 = np.maximum(a,b)
m = np.max(m1)
A=1
while m >= 1:
    m = m/2
    A=A*2
print("A=",A)

#%%
B=1
n = np.sum(b)/B
while n >= 1:
    B=B*2
    n=np.sum(b)/B
print("B=",B)

#%%
imp = np.zeros(1000) 
imp[0]=1

h = ss.lfilter([1], a, imp)
sf = np.sum(abs(h))
S = 2**int(np.log2(sf)+1.0)
print("sf=",sf, ", S=",S)

#%%
q = 14
b_fxp = np.round(b*2**q,0)
a_fxp = np.round(a*2**q,0)

coeff_fxp = np.array([b_fxp, a_fxp]).flatten()

print_coeff(coeff_fxp, 'bandpass filter')
omega, H = ss.freqz(b_fxp, a_fxp, worN=50000, fs=fs)
plotMag(omega, H, "Response of biquad-highshelf", xlim = [0, fs/2], ylim = [-100, 10])

#%%
data = np.arange(-10, 10, dtype=np.int16)
outfile = open('audio.dat', 'w')
for d in data:
    outfile.write('%d\n' % (d))

#%%
filtered_DI = np.loadtxt('audio_filtered_DI.dat');  #filtered data by direct form i in cpp
filtered_DI = filtered_DI.astype(np.int16)

#%%
data_filt_nor = ss.lfilter(b, a, data)

plt.plot(data)
plt.plot(data_filt_nor)
plt.show()

#%%
data_filt_fxp_s = ss.lfilter(b_fxp, a_fxp, data)
data_filt_fxp = 2.0*np.round(data_filt_fxp_s,0)
b_fxp = b_fxp.astype(np.int16)
a_fxp = a_fxp.astype(np.int16)

plt.plot(data)
plt.plot(data_filt_fxp)
plt.show()

#%%
"""
data_filt_nor = ss.lfilter([b0,b1,b2], [a0,a1,a2], data_nor)
data_filt_nor = data_filt_nor*(2**15-1)
data_filt_nor = data_filt_nor.astype(np.int16)

data_filt_fxp = ss.lfilter(b_fxp, a_fxp, data)
data_filt_fxp = data_filt_fxp.astype(np.int16)
"""

ser = serial.Serial()
ser.port = "COM5" 

ser.baudrate = 256000
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check
ser.stopbits = serial.STOPBITS_ONE #number of stop bits

#%%
ser.timeout = None          #non-block read 0.5s
ser.writeTimeout = 0.5     #timeout for write 0.5s
ser.xonxoff = False    #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control

#%%
try: 
    ser.open()
except Exception as ex:
    print ("open serial port error " + str(ex))
    
#%%
coef_cmd = np.uint8([ord('c'), ord('o'), ord('e'), ord('f')])
#data_cmd = np.uint8([ord('d'), ord('a'), ord('t'), ord('a')])
done_cmd = np.uint8([ord('d'), ord('o'), ord('n'), ord('e')])

#%%
coeff_fpga = np.array([coeff_fxp[0], coeff_fxp[1], coeff_fxp[2], 14, coeff_fxp[4], coeff_fxp[5]], dtype=np.int16)
#coeff_fpga = np.array([1,1,1,1,1], dtype=np.int16)
data_in_fpga = np.append(data, np.array([0,0], dtype=np.int16))
data_out_fpga = np.array([], dtype=np.int16)

#%%
ser.flushInput()
ser.flushOutput()

for tx in coef_cmd:
    numb = ser.write(tx.tobytes())

for tx in coeff_fpga:
    numb = ser.write(tx.tobytes())

for tx in data_in_fpga:
    numb = ser.write(tx.tobytes())
    while (ser.in_waiting >= 2):
        rxb = ser.read(2)
        rxb = rxb[::-1]
        print(rxb)
        rx = np.frombuffer(rxb, dtype='int16')
        data_out_fpga = np.append(data_out_fpga, rx)
        
for tx in done_cmd:
    numb = ser.write(tx.tobytes())
    while (ser.in_waiting >= 2):
        rxb = ser.read(2)
        rxb = rxb[::-1]
        print(rxb)
        rx = np.frombuffer(rxb, dtype='int16')
        data_out_fpga = np.append(data_out_fpga, rx)
        
#%%
data_out_fpga = data_out_fpga[3:3+len(data)]
        
#%%
diff_idx, diff, mae, mse = comp_arr(data_filt_nor, data_filt_fxp)

#%%
diff_idx, diff, mae, mse = comp_arr(data_out_fpga, data_filt_fxp)

#%%
diff_idx, diff, mae, mse = comp_arr(data_filt_nor, data_out_fpga)







#%%
coef = np.random.randint(-32767, 32767, size=5, dtype=np.int16)
#coef = np.array([1,2,1,2,2], dtype=np.int16)
data = np.arange(-10, 10, dtype=np.int16)
#data = np.random.randint(-32767, 32767, size=4000, dtype=np.int16)

#%%
#data_fxp = ss.lfilter([coef[0], coef[1], coef[2]], [32767., coef[3], coef[4]], data)
data_fxp = ss.lfilter([6143., 12205., 6143.], [16383., 24902., 10485.], data)
data_fxp = data_fxp.astype(np.int16)
#data = np.append(data, np.array([0], dtype=np.int16))
data_out = np.array([], dtype=np.int16)

#%%
ser.flushInput()
ser.flushOutput()

for tx in coef_cmd:
    numb = ser.write(tx.tobytes())
    while (ser.in_waiting >= 2):
        rxb = ser.read(2)
        rxb = rxb[::-1]
        rx = np.frombuffer(rxb, dtype='int16')
        data_out = np.append(data_out, rx)

for tx in coef:
    numb = ser.write(tx.tobytes())
    while (ser.in_waiting >= 2):
        rxb = ser.read(2)
        rxb = rxb[::-1]
        rx = np.frombuffer(rxb, dtype='int16')
        data_out = np.append(data_out, rx)

for tx in data:
    numb = ser.write(tx.tobytes())
    while (ser.in_waiting >= 2):
        rxb = ser.read(2)
        rxb = rxb[::-1]
        rx = np.frombuffer(rxb, dtype='int16')
        data_out = np.append(data_out, rx)

for tx in done_cmd:
    numb = ser.write(tx.tobytes())
    while (ser.in_waiting >= 2):
        rxb = ser.read(2)
        rxb = rxb[::-1]
        rx = np.frombuffer(rxb, dtype='int16')
        data_out = np.append(data_out, rx)
        
#%%
data_out = data_out[3:3+len(data)]

#%%
comp_arr(data_out, data_fxp)
        
        
        
        
        
#%%
def K_filter_fxp(data, fs):
    # apply K filtering as specified in EBU R-128 / ITU BS.1770-4

    # pre-filter 1
    f0 = 1681.9744509555319
    G  = 3.99984385397
    Q  = 0.7071752369554193
    K  = np.tan(np.pi * f0 / fs)
    Vh = np.power(10.0, G / 20.0)
    Vb = np.power(Vh, 0.499666774155)
    a0_ = 1.0 + K / Q + K * K
    b0 = (Vh + Vb * K / Q + K * K) / a0_
    b1 = 2.0 * (K * K -  Vh) / a0_
    b2 = (Vh - Vb * K / Q + K * K) / a0_
    a0 = 1.0
    a1 = 2.0 * (K * K - 1.0) / a0_
    a2 = (1.0 - K / Q + K * K) / a0_
    b_fixed_s1 = np.array([np.trunc(i * 32767.0) for i in [b0,b1,b2]])
    a_fixed_s1 = np.array([np.trunc(i * 32767.0) for i in [a0,a1,a2]])
    coeff = np.array([b_fixed_s1, a_fixed_s1]).flatten()
    print_coeff(coeff, 'stage-1')
    data_1 = ss.lfilter(b_fixed_s1, a_fixed_s1,data)

    # pre-filter 2
    f0 = 38.13547087613982
    Q  = 0.5003270373253953
    K  = np.tan(np.pi * f0 / fs)
    a0 = 1.0
    a1 = 2.0 * (K * K - 1.0) / (1.0 + K / Q + K * K)
    a2 = (1.0 - K / Q + K * K) / (1.0 + K / Q + K * K)
    b0 = 1.0
    b1 = -2.0
    b2 = 1.0
    b_fixed_s2 = np.array([np.trunc(i * 32767.0) for i in [b0,b1,b2]])
    a_fixed_s2 = np.array([np.trunc(i * 32767.0) for i in [a0,a1,a2]])
    coeff = np.array([b_fixed_s2, a_fixed_s2]).flatten()
    print_coeff(coeff, 'stage-2')
    data_2 = ss.lfilter(b_fixed_s2, a_fixed_s2,data_1)

    return data_2, b_fixed_s1, a_fixed_s1, b_fixed_s2, a_fixed_s2
    # return data passed through 2 pre-filters
    
#%%  
data_2, b_fixed_s1, a_fixed_s1, b_fixed_s2, a_fixed_s2 = K_filter_fxp(data, 48000)
