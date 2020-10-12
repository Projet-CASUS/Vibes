import csv

import numpy as np
convolve = np.convolve
import pandas as pd
import scipy.signal as signal


class import_file:
    def __init__(self, file_type='csv'):
        self.type = file_type

    def __call__(self, filename):
        if self.type == 'csv':
            with open(filename, newline='') as f:
                reader = csv.reader(f)
                self.names = next(reader)
            return np.loadtxt(filename, delimiter=',',skiprows=1)
        else:
            return filename


class Filter:
    """
    Retourne les valeurs filtrees des donnes fournies en parametres
    """
    def __init__(self, sample_rate, num_taps = 5):
        """
        :param sample_rate: -> int > Quantite de donnee par seconde
        :param num_taps: TODO Louis-Philippe decrire le type et l utilite
        """
        self.sample_rate = sample_rate
        self.num_taps = num_taps
        self.fir_filter = None

    def __call__(self, data, type, cut_off):
        """
        TODO donner un exemple de call
        :param data: -> panda > donnees a filtrer
        :param type: -> string >    type de filtre
        :param cut_off: -> int or list > frequence de coupure
        :return: -> panda > sequence de donnees filtrees
        """
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

    def passe_bas(self):
        """
        :return: vecteur de filtre FIR pour un passe bas
        """
        f = self.cut_off / self.sample_rate
        return signal.firwin(self.num_taps, f)

    def passe_haut(self):
        """
        :return: vecteur de filtre FIR pour un passe haut
        """
        f = self.cut_off / self.sample_rate
        return signal.firwin(self.num_taps, f, pass_zero=False)

    def passe_bande(self):# Définit le vecteur de filtre FIR pour un passe bande
        """
        :return: vecteur de filtre FIR pour un passe bande
        """
        f1 = float(self.cut_off[0] / self.sample_rate)
        f2 = float(self.cut_off[1] / self.sample_rate)
        return signal.firwin(self.num_taps, self.cut_off, pass_zero=False)

class Range_selection:
    """
    Selectionne et retourne un vecteur contenant les valeurs correspondantes a la fourchette de temps selectionnee
    """
    def __init__(self,first,last):
        """
        :param first: -> int > premiere donne de temps
        :param last: -> int > derniere donnee de temps
        """
        self.first = first
        self.last = last
        self.type = "range_selection"
        self.data = {}
        self.new_panda = None

    def __call__(self, data):
        """

        TODO samedi Philippe
        :param data: La totalite des donnees temporelles en cours d analyse
        :return: -> vecteur panda > Nouveau vecteur de donnees temporelles
        """
        for i in range(len(data.columns)):
            self.data[data.columns[i]]= [0] *(self.last-self.first)
        self.new_panda = pd.DataFrame(self.data)
        print(self.new_panda)
        for i in range(0, len(data.columns)):
            self.data_realocation(i, data)
        return self.new_panda

    def data_realocation(self, i, data):
        """
        TODO samedi Philippe
        :param i:
        :param data:
        :return:
        """
        for x in range(0, self.last - self.first):
            self.new_panda = data.loc[:,data.columns[i]][x + self.first]
