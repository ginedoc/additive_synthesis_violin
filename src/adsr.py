from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

s = wavfile.read('../cctest.wav')
print(s[0], len(s[:,1]))
plt.plot(s[:,1])
plt.show()
#wavfile.write('adsr.wav', s[0], s[1]*m)

