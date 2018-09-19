import numpy as np
import matplotlib.pyplot as plt
import librosa
from scipy.signal import argrelextrema

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
limit = 2000
group = []
value = [0,0,0]
mode = 0 # 0:not searching , 1:finding
cons_zero = 0
for i, pt in enumerate(abs_spec):
    # start
    if pt!=0 and mode==0:
        value[0] = i
        mode=1
    if mode == 1 and pt==0 and cons_zero<limit:
        cons_zero += 1
    elif mode == 1 and pt!=0:
        value[2] += 1
    elif mode == 1 and cons_zero==limit:
        value[1] = i
        group.append(value)
        value = [0,0,0]
        mode = 0
        

print(group)
print(len(group))
plt.plot(abs_spec)

plt.show()
