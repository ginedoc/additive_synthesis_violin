import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy.io.wavfile import  write

# Read sound
snd = librosa.load('../snd/violin_A3_05_forte_arco-normal.mp3')
spectrum = np.fft.fft(snd[0])

# find local maximum
abs_spec = np.abs(spectrum[0:int(len(spectrum)/2)])
## high pass filter
for i, spec in enumerate(abs_spec):
    if spec < 2:
        abs_spec[i] = 0
# group
## convolution, end point detection
epd = abs_spec
conv = [0.5, 1, 0.5]
for _ in range(1):
    for i, spec in enumerate(abs_spec[1:-1]):
        epd[i+1] = np.inner(abs_spec[i:i+3],conv)
## segment
seg = []
mode = 0 # 0: not searching , 1: searching
border = [0,0]
for i, point in enumerate(epd):
    if mode==0 and point>0.1:    # start searching
        border[0] = i
        mode = 1
    elif mode==1 and point<=0.1:  # end searching
        border[1] = i
        mode = 0
        seg.append(border)
        border = [0,0]


# coeffiecint of fourrier
fundamental_f = np.argmax(abs_spec)
fundamental_b = 0
FP = []
for s in seg:
    freq = np.argmax(abs_spec[s[0]:s[1]]) + s[0]
    prop = sum(abs_spec[s[0]:s[1]])
    FP.append([freq, prop])
    fundamental_b += prop
# normalize
for i, s in enumerate(FP):
    FP[i][1] = FP[i][1]/fundamental_b

print(FP)
##

duration = 5 #sec
sample_rate = 44100

wav = [0 for _ in range(0, int(sample_rate*duration))]
for fp in FP:
    wav = np.add(wav, [ fp[1]*np.cos(2*np.pi*(fp[0]*(x/sample_rate))) for x in range(0, int(sample_rate*duration)) ])
#write("../violin", sample_rate, wav)


plt.figure(1)
plt.plot(snd[0])
plt.figure(2)
plt.plot(spectrum)
plt.figure(3)
plt.plot(abs_spec)
plt.figure(4)
plt.plot(wav)
plt.show()
