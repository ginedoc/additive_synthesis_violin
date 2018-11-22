import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import librosa

def karplus_strong(wavetable, n_samples, decay):
    
    samples = np.array([0]*n_samples,'float32')
    
    # ring buffer
    for i in range(n_samples):
        
        samples[i] = wavetable[0] 
        avg = decay*0.5*(wavetable[0]+wavetable[1])
        # 增右邊，刪左邊
        wavetable = np.append(wavetable,avg)
        wavetable = np.delete(wavetable,0)
        
    return samples

fs = 44100
decay_factor = 0.995
wavetable = librosa.load('../violin')[0]
wavetable = wavetable*2
result = karplus_strong(wavetable, 5 * fs, decay_factor)

plt.plot(result)
plt.show()
result = result.astype('float32')
wavfile.write('../result.wav', fs, result)
