import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

window_size = 16
hop_size = 2
#hop_size = window_size

snd =librosa.load('../snd/violin_A3_05_forte_arco-normal.mp3')
#snd =librosa.load('../snd/clarinet.mp3')
sample_rate = snd[1]
sound = snd[0]


#swin = np.zeros((int(len(sound)/hop_size), len(sound)))
swin = np.zeros((int(len(sound)/hop_size), window_size))
#hanning = np.hanning(window_size)
hanning = np.bartlett(window_size)

## window
print('windowing...')
for i in range(int(len(sound)/hop_size)):
    if i*hop_size+window_size < len(sound):
        #swin[i][i*hop_size:i*hop_size+window_size] = sound[i*hop_size:i*hop_size+window_size]*hanning
        swin[i] = sound[i*hop_size:i*hop_size+window_size]*hanning
## fft
print('ffting...')
fftwin = np.zeros(swin.shape)
for i, win in enumerate(swin):
    fftwin[i] = np.fft.fft(win)

## sinwave
print('sinwaving...')
sinsynth = np.zeros(len(sound))
for i, win in enumerate(fftwin):
    if i*hop_size+window_size<len(sound):
        for j, pt in enumerate(win):
            pt1 = np.argmax(win[0:int(len(win)/2)])
            freq1 = pt1/(window_size/sample_rate)
            gain1 = win[pt1]
            print(freq1)
            
            sinsynth[i*hop_size+j] = sinsynth[i*hop_size+j] + gain1*np.sin(2*np.pi*freq1*j/sample_rate)
"""
## ifft
print('iffting...')
ifft = np.zeros(fftwin.shape)
for i, win in enumerate(fftwin):
    ifft[i] = np.fft.ifft(win)

## resyn
print('resyn...')
synth = np.zeros(len(sound))
for i, win in enumerate(ifft):
    if i*hop_size+window_size<len(sound):
        synth[i*hop_size:i*hop_size+window_size] = synth[i*hop_size:i*hop_size+window_size] + win 
"""


write("../violin.wav", sample_rate, sinsynth/7)
plt.figure(1)
plt.plot(sound)
plt.figure(3)
plt.plot(sinsynth/7)
plt.show()
