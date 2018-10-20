import os
import sys
from scipy.io import wavfile
if __name__ == "__main__":
    for root, dirs, files in os.walk(sys.argv[1]):
        for f in files:
            if f.endswith(".wav"):
                fullpath = os.path.join(root, f)
                os.system("python3 optimization.py "+fullpath)
                #print("python optimization.py "+fullpath)
                '''
                fs, orig = wavfile.read(fullpath)
                db_cutoff = -50
                cutoff = int(32768*10**(db_cutoff/20))
                for i in range(len(orig)):
                    if orig[i] > cutoff or orig[i] < -cutoff:
                        left = i
                        break
                for i in range(len(orig)-1, 0, -1):
                    if orig[i] > cutoff or orig[i] < -cutoff:
                        right = i
                        break
                orig = orig[left:right]
                orig = orig.astype('int16')
                wavfile.write(fullpath,fs,orig)
                '''
