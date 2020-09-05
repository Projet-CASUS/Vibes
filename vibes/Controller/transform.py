import numpy as np
convolve = np.convolve
import pandas as pd
import scipy.signal as signal


class import_file:
    def __init__(self, type='csv'):
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            return pd.read_csv(filename, delimiter=';')
        else:
            return filename


class Filter:

    def __init__(self, sample_rate, num_taps = 5):
        self.sample_rate = sample_rate
        self.num_taps = num_taps
        self.fir_filter = None

    def __call__(self, data, type, cut_off):
        self.data = data
        self.cut_off = cut_off

        # On définit le filtre à utiliser
        if type == "passe_bas":
            self.fir_filter = self.passe_bas()
        elif type == "passe_haut":
            self.fir_filter = self.passe_haut()
        elif type == "passe_bande":
            self.fir_filter = self.passe_bande()

        # On effectue la convolution du filtre FIR
        filtered_data = convolve(data, self.fir_filter, 'same')
        return filtered_data

    def passe_bas(self): # Définit le vecteur de filtre FIR pour un passe bas
        f = self.cut_off / self.sample_rate
        return signal.firwin(self.num_taps, f)

    def passe_haut(self):# Définit le vecteur de filtre FIR pour un passe haut
        f = self.cut_off / self.sample_rate
        return signal.firwin(self.num_taps, f, pass_zero=False)

    def passe_bande(self):# Définit le vecteur de filtre FIR pour un passe bande
        f1 = float(self.cut_off[0] / self.sample_rate)
        f2 = float(self.cut_off[1] / self.sample_rate)
        return signal.firwin(self.num_taps, self.cut_off, pass_zero=False)

class Range_selection:
    """
    TODO philippe
    """
    def __init__(self,first,last):
        self.first = first
        self.last = last
        self.type = "range_selection"
        self.name_array = ["time", "x", "y", "z", "gforce"]
        self.saved_data = [[0 for x in range(len(self.name_array))] for i in range((self.last - self.first))]
        data = {'time':[None] , 'x':[None], 'y':[None], 'z':[None], 'gforce':[None]}
        self.new_panda = pd.DataFrame(data)

    def __call__(self,data):
        for x in range(0, len(self.name_array)):
            self.data_relocation(x,data)
        return self.new_panda

    def data_relocation(self,i,data):
        for x in range(0, self.last - self.first):
            self.new_panda.loc[:, self.name_array[i]][x] = data.loc[:, self.name_array[i]][x + self.first]

class Filtre_parrallele:
    """
    TODO Louis-Philippe
    """
    pass
