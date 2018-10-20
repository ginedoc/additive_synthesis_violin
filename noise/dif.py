#linear
import numpy as np
from scipy.io import wavfile
import pickle
import sys
import os

if len(sys.argv) < 2:
    path = '.'
else:
    path = sys.argv[1]

with open(path+'/A.pickle','rb') as file:
    a=pickle.load(file)
with open(path+'/B.pickle','rb') as file:
    b=pickle.load(file)
with open(path+'/W.pickle','rb') as file:
    w=pickle.load(file)
with open(path+'/data.pickle','rb') as file:
    data=pickle.load(file)
N = data['N']
AudioFileName = data['AudioFileName']
frameSize = data['frameSize']
hopSize = data['hopSize']
Frames = data['Frames']
f  = data['f']
fs, orig = wavfile.read(path+'/'+AudioFileName+'.wav')
m = max(max(orig),abs(min(orig)))

directory = path+'/dif'
if not os.path.exists(directory):
    os.makedirs(directory)
directory = path+'/harm'
if not os.path.exists(directory):
    os.makedirs(directory)
y = np.zeros((len(a)+1)*hopSize)
t = np.arange(frameSize)
for frame in range(Frames):
    start = frame*frameSize
    end = start+frameSize
    cur = np.zeros(frameSize)
    for i in range(N):
        cur += a[frame][i]*np.sin(2*np.pi*np.array(w[start:end])*(i+1)/fs*t)+b[frame][i]*np.cos(2*np.pi*np.array(w[start:end])*(i+1)/fs*t)
    cur = (cur*m).astype('int16')
    dif = orig[frame*hopSize:frame*hopSize+frameSize]-cur
    wavfile.write(path+'/harm/'+AudioFileName+'_harm_'+str(frame)+'.wav',fs,cur)
    wavfile.write(path+'/dif/'+AudioFileName+'_dif_'+str(frame)+'.wav',fs,dif)