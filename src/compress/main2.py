import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

window_size = 256
hop_size = int(window_size/2)

snd = librosa.load('../snd/violin_A3_05_forte_arco-normal.mp3')
sample_rate = snd[1]
sound = snd[0]

sw = np.array([])
## windowing
hanning = np.hanning(window_size)
add = 0
for i in range(0,len(sound), hop_size):
    if i+window_size<len(sound):
        w = sound[i:i+window_size]*hanning   
        sw = np.append(sw, w, axis=0)
    else:
        w = np.append(sound[i:-1], np.zeros(window_size-len(sound[i:-1])))
        sw = np.append(sw, w, axis=0)
sw = sw.reshape((window_size, int(len(sound)/hop_size+1)))
print(sw)


## fft
fft = sw
for i, f in enumerate(sw):
    fft[i] = np.fft.fft(f)
### filter
#for i, f in enumerate(fft):
#    for j, ff in enumerate(f):
#        if np.abs(ff) < 0.0005:
#            fft[i][j] = 0

## ifft
wav = np.zeros(len(sound))
ifft = []
if (len(wav)-window_size)%hop_size!=0:
    wav = np.append(wav, np.zeros(len(wav)-len(wav)%hop_size), axis=0)
for i, f in enumerate(fft):
    ifft.append(np.fft.ifft(f, window_size))

for i,f in enumerate(ifft):
    wav[i*hop_size:i*hop_size+window_size] = wav[i*hop_size:i*hop_size+window_size] + f

plt.plot(wav)
plt.show()
## synth
write("../violin.wav", sample_rate, wav)
