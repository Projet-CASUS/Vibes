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
        super().__init__()
        self.type = type

    def __call__(self, filename):
        if self.type == 'csv':
            return pd.read_csv(filename, delimiter=';')
        else:
            return filename


class frenquency_transformation():
    pass

class Filter(Transformation):

    def __init__(self, sample_rate, numtaps = 5):
        super().__init__()
        self.sample_rate = sample_rate
        self.numtaps = numtaps

    def __call__(self, data, type, cutoff):
        self.data =data
        self.cutoff = cutoff

        # On définit le filtre à utiliser
        if type == "passe_bas":
            fir_filter = self.passe_bas()
        elif type == "passe_haut":
            fir_filter = self.passe_haut()
        elif type == "passe_bande":
            fir_filter = self.passe_bande()

        # On effectue la convolution du filtre FIR
        filtered_data = convolve(data, fir_filter, 'same')
        return filtered_data


    def passe_bas(self): # Définit le vecteur de filtre FIR pour un passe bas
        f = self.cutoff/self.sample_rate
        return signal.firwin(self.numtaps, f)

    def passe_haut(self):# Définit le vecteur de filtre FIR pour un passe haut
        f = self.cutoff/self.sample_rate
        return signal.firwin(self.numtaps, f, pass_zero=False)

    def passe_bande(self):# Définit le vecteur de filtre FIR pour un passe bande
        f1 = float(self.cutoff[0]/self.sample_rate)
        f2 = float(self.cutoff[1]/self.sample_rate)
        return signal.firwin(self.numtaps, self.cutoff, pass_zero=False)


class RangeSelection(Transformation):
    """
    TODO philippe
    """
    def __init__(self,first,last):
        super().__init__()
        self.first = first
        self.last = last
        self.NameArray = ["time", "x", "y", "z", "gforce"]
        self.type = "RangeSelection"
        self.savedUpData =[[0 for x in range(len(self.NameArray))] for i in range((self.last - self.first))]
    def __call__(self,data):
        for x in range(0, len(self.NameArray)):
            self.data_relocation(x,data)
        newData = pd.DataFrame(self.savedUpData, columns=['time','x','y','z','gforce'])
        return newData

    def data_relocation(self,i,data):
        for x in range(0, self.last - self.first):
             self.savedUpData[x][i] = data.loc[:, self.NameArray[i]][x + self.first]

    def merge(self):
        """
        merge time together
        :return:
        """
        pass
class FiltreParralele():
    """
    TODO Louis-Philippe
    """
    pass
