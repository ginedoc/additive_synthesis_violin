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
        p = os.path.basename(path)
        self.note = int(p[p.find('_')+1:p.find('_')+3])

    """
    * get_vol_fnum(low, high)
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
                frame = self.wav[f_index*hop:-1]
                fsize = len(self.wav) - f_index*hop

    
            # maximum in range
            if max(frame)>=low and max(frame)<high:
                f.append(f_index)

        return f

    """
    * get_fourier_coef(fnum, average):
        fnum: list of frame index
        average: if true, return average coefficient

        return: 2d or 3d array
            [[A list],[B list]]
    """
    def get_fourier_coef(self, fnum, average=True):
        N    = self.data['N']
        coef = np.zeros((2,N))

        a = []
        b = []
        for f_index in fnum:
            a.append(self.An[f_index])
            b.append(self.Bn[f_index])

        a = np.array(a)
        b = np.array(b)
     
        for i in range(len(a)):
            a[i] = a[i]/a[i][0]
            b[i] = b[i]/b[i][0]

        if average is True:
            return np.array([sum(a)/len(a), sum(b)/len(b)])
        elif average is False:
            return np.array([a, b])

    


