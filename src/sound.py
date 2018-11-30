# header file
## class SingleNormalViolin

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os


class SNVln():
    """
    path: directory contains wav, data, A, B
    """
    def __init__(self, path):
        wav_path  = path + '/' + os.path.basename(path) + '.wav'
        data_path = path + '/data.pickle'
        A_path    = path + '/A.pickle'
        B_path    = path + '/B.pickle'

        wav = wavfile.read(wav_path)
        sample_rate = wav[0]
        wav = np.array(wav[1])
        wav = wav / max(wav)   # normalize
        
        # variable
        self.sample_rate = sample_rate
        self.wav    = wav
        self.data   = pickle.load(open(data_path, "rb"))
        self.An = np.array(pickle.load(open(A_path, "rb")))
        self.Bn = np.array(pickle.load(open(B_path, "rb")))

    """
    get_vol_fnum(low, high)
        low: under bound
        high: upper bound
        
        return 'f': list of frame number 
    """
    def get_vol_fnum(self, low, high):
        Frames = self.data['Frames']
        hop    = self.data['hopSize']
        fsize  = self.data['frameSize']

        f = []

        for f_index in range(Frames):
            if f_index*hop+fsize < len(self.wav):
                frame = self.wav[f_index*hop:f_index*hop+fsize]
            else:   # last frame
                frame = self.wav[N*hop:-1]
                fsize = len(self.wav) - f_index*hop

    
            # propotion > 50%
            cnt = 0
            for pt in frame:
                if abs(pt) >= low and abs(pt) < high:
                    cnt += 1

            if cnt >= fsize / 2:
                f.append(f_index)

        return f

    """
    get_fourier_coef(fnum):
        fnum: list of frame index

        return: 2d array
            [[A list],[B list]]
    """
    def get_fourier_coef(self, fnum):
        N    = self.data['N']
        coef = np.zeros((2,N))
        

        a = []
        b = []
        for f_index in fnum:
            a.append(self.An[f_index][0])
            b.append(self.Bn[f_index][0])
        a = np.array(a)
        b = np.array(b)
        plt.plot(a)
        plt.plot(b)
        plt.show()
        

        return coef[0]

