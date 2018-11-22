#linear
#apply window function
import numpy as np
from scipy.io import wavfile
import pickle
import sys
from scipy import signal

if len(sys.argv) < 2:
    path = '.'
else:
    path = sys.argv[1]

with open(path+'/A.pickle','rb') as file:
    a=pickle.load(file)
with open(path+'/B.pickle','rb') as file:
    b=pickle.load(file)
with open(path+'/w.pickle','rb') as file:
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

if len(sys.argv) < 3:
    window = np.ones(frameSize)
    window_name = ''
else:
    window = signal.get_window(sys.argv[2], frameSize)
    window_name = '_'+sys.argv[2]
y = np.zeros((len(a)+1)*hopSize)
window_sum = np.zeros((len(a)+1)*hopSize)
t = np.arange(frameSize)
for frame in range(Frames):
    start = frame*frameSize
    end = start+frameSize
    cur = np.zeros(frameSize)
    for i in range(N):
        cur += a[frame][i]*np.sin(2*np.pi*np.array(w[start:end])*(i+1)/fs*t)+b[frame][i]*np.cos(2*np.pi*np.array(w[start:end])*(i+1)/fs*t)
    cur *= window
    y[frame*hopSize:frame*hopSize+frameSize] += cur
    window_sum[frame*hopSize:frame*hopSize+frameSize] += window
y /= window_sum
y *= m
y = y.astype('int16')
wavfile.write(path+'/'+AudioFileName+window_name+'_add.wav',fs,y)
dif = orig[:len(y)]-y
wavfile.write(path+'/'+AudioFileName+window_name+'_dif.wav',fs,dif)
error=np.mean(np.square(orig[:len(y)]-y))
print(error)
