from table import table
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    table = table()
    if not table.is_table_exist():
        table.build_table()
        table.save_table()

    currentAngle = 0
    DeltaAngle = 440*2*3.14/44100
    snd = np.zeros(44100*3)
    sample = 0
    for i in range(44100*3):
        sample = 0
        currentAngle = currentAngle + DeltaAngle
        for j in range(len(table.table[0][0])):
            sample = sample + table.table[11][0][0][j]*np.sin(currentAngle) + table.table[11][0][1][j]*np.cos(currentAngle)
        snd[i] = sample


    wavfile.write("test.wav", 44100, snd)
