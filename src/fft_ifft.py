import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

window_size = 256
hop_size = int(window_size/2)

snd = librosa.load('../snd/violin_A3_05_forte_arco-normal.mp3')
sample_rate = snd[1]
sound = snd[0]

sf = np.fft.fft(sound)
snd2 = np.fft.ifft(sf, len(sound))

plt.figure(1)
plt.plot(sf)
plt.figure(2)
plt.plot(snd2)
plt.show()
