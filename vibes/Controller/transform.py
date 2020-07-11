import numpy as np
import scipy.signal as signal
import numpy as np
convolve = np.convolve
import pandas as pd


class Transformation:
    def __init__(self):
        pass
    def __call__(self, input):
        return input


class ImportFile(Transformation):
    def __init__(self, type='csv'):
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            return pd.read_csv(filename, delimiter=';')
        else:
            return filename


class Filter(Transformation):
    def __init__(self, sample_rate, numtaps = 5):
        self.sample_rate = sample_rate
        self.numtaps = numtaps

    def __call__(self, data, type, cutoff):
        self.data =data
        self.cutoff = cutoff

        # On définit le filtre à utilisé
        if type == "passe_bas":
            fir_filter = passe_bas()
        elif type == "passe_haut":
            fir_filter = passe_haut()
        elif type == "passe_bande":
            fir_filter = passe_bande()

        # On effectue la convolution du filtre FIR
        filtered_data = convolve(data, fir_filter, 'same')
        return filtered_data


    def passe_bas(): # Définit le vecteur de filtre FIR pour un passe bas
        f = self.cutoff/self.sample_rate
        return signal.firwin(self.numtaps, f)

    def passe_haut():# Définit le vecteur de filtre FIR pour un passe haut
        f = self.cutoff/self.sample_rate
        return signal.firwin(self.numtaps, f, pass_zero=False)

    def passe_bande():# Définit le vecteur de filtre FIR pour un passe bande
        f1 = float(self.cutoff[0]/self.sample_rate)
        f2 = float(self.cutoff[1]/self.sample_rate)
        return signal.firwin(self.numtaps, cutoff, pass_zero=False)




class RangeSelection(Transformation):
    """
    TODO philippe
    """
    def __init__(self,first,last):
            self.first = first
            self.last = last
            self.NameArray = ["time", "x", "y", "z", "gforce"]
    def __call__(self,data):
        for x in range(0, len(self.NameArray)):
            self.data_relocation(x,data)
        return data

    def data_relocation(self,i,data):
        for x in range(0, self.last - self.first):
             data.loc[:,self.NameArray[i]][x] = data.loc[:, self.NameArray[i]][x + self.first]

class FiltreParralele():
    """
    TODO Louis-Philippe
    """
    pass
