import numpy as np
import os
from sound import SNVln
import pickle


class table():
    def __init__(self, dir_path='../linear_v2.2/NOMM'):
        self.dir_path = dir_path
        self.table = []

    """
    load table from path(default = ../linear_v2.2/NOMM)
    """
    def build_table(self, vol_level=5):
        self.table = [[[] for _ in range(vol_level)] for _ in range(64)]
        for directory in os.listdir(self.dir_path):
            sound = SNVln(self.dir_path+'/'+directory)
            note  = sound.note
            for vol in range(vol_level):
                frame = sound.get_vol_fnum(vol/vol_level, vol/vol_level+1/vol_level)
                coef  = sound.get_fourier_coef(frame)
                self.table[note-1][vol] = coef

        return self.table

    #------------------------------------------------------#
    """
    save table to pickle
    """
    def save_table(self, A_name='A_coef.pkl', B_name='B_coef.pkl', info_name='info.pkl'):
        A    = open('../' + A_name, 'wb')
        B    = open('../' + B_name, 'wb')
        info = open('../' + info_name, 'w')
            
        for i,note in enumerate(self.table):
            info.write(str(len(note[0][0]))+' ')
            for j,vol in enumerate(note):
                for element in vol[0]:
                    A.write(element)
                for element in vol[1]:
                    B.write(element)
        A.close()
        B.close()
        info.close()
                

    #------------------------------------------------------#
    """
    check if table is built
        return true if established
               false if not established
    """
    def is_table_exist(self, A_name='A_coef.pkl', B_name='B_coef.pkl', info_name='info.pkl'):
        if os.path.isfile('../'+A_name) and os.path.isfile('../'+B_name) and os.path.isfile('../'+info_name):
            return True
        else: return False

