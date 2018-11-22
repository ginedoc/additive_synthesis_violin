# average
## 取各Frame的平均做為Fourier Series的係數
import numpy as np
from scipy.io import wavfile
import pickle
import sys

if len(sys.argv) < 2:
    path = '.'
else:
    path = sys.argv[1]

a = pickle.load(open(path+'/A.pickle', 'rb'))
b = pickle.load(open(path+'/B.pickle', 'rb'))
w = pickle.load(open(path+'/W.pickle', 'rb'))
d = pickle.load(open(path+'/data.pickle', 'rb'))

a = np.array(a)
b = np.array(b)
w = np.array(w)
f = d['f']
print(f)


# information
samplerate = 44100
length     = 1  #sec

# calculate average
an = sum(a)/len(a)
bn = sum(b)/len(b)

# synthesize
buf = np.zeros(samplerate*length)
for t in range(samplerate*length):
    for i in range(len(an)):
        buf[t] += an[i]*np.sin(2*np.pi*f/samplerate *t) + bn[i]*np.cos(2*np.pi*f/samplerate *t)

print(buf)

wavfile.write('synth.wav', samplerate, buf)
