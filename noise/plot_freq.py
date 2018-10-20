#linear
import numpy as np
from scipy.io import wavfile
import pickle
import sys
import matplotlib.pyplot as plt


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
if len(sys.argv) < 4:
    frame_start = 0
    frame_end = Frames
else:
    frame_start = int(sys.argv[2])
    frame_end = Frames-int(sys.argv[3])
y = np.zeros((len(a)+1)*hopSize)
t = np.arange(frameSize)
for frame in range(frame_start, frame_end):
    start = frame*frameSize
    end = start+frameSize
    x = [i for i in range(frame*hopSize, frame*hopSize+frameSize)]
    if frame%2 == 0:
        plt.plot(x, w[start:end], 'b')
    else:
        plt.plot(x, w[start:end], 'r')
    plt.ylabel('frequency(Hz)')
    plt.xlabel('samples')
#plt.show()
plt.savefig(path+'/freq.png')