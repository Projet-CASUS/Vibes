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

class Differential:
    def __init__(self,data):
        self.data = data
        self.names = data[0].names
        self.type = "Differential"
    def __call__(self,data):
        return self.derive(self.data[1],self.names)
    def derive(self, data,names):
        """
                    Derivation numerique
                    !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
                    TODO Faire recevoir et retourner un vecteur panda
                    :param data: -> vecteur panda > Contient les donnees a deriver
                    :param dt: TODO Louis-Philippe que veux tu dire par "pas de temps" ??
                    :return: -> vecteur panda > vecteur des donnees derivees
                    """
        # Dérivation numérique
        # data = vecteur de données
        # dt   = pas de temps
        dt = 0.001
        drv_list = np.zeros(shape=((len(data)-0),len(data[1])))
        for x in range(len(data)):
            drv_list[x][0] = data[x][0]
        for x in range (1,len(names)):
            for i in range(1,len(data)):
                if i == 0:  # point 1 : dérivé avant
                    drv_list[i][x] = (((data[i + 1][x] - data[i][x]) / dt))
                elif i == (len(data) - 1):  # point final : dérivé arrière
                    drv_list[i][x] = (((data[i][x] - data[i - 1][x]) / dt))
                else:  # point médiants : dérivé centré (plus précis)
                    drv_list[i][x] = (((data[i + 1][x] - data[i - 1][x]) / (2 * dt)))
        return drv_list

class Integral:
    def __init__(self,data):
        self.data = data
        self.names = data[0].names
        self.type = "Integral"
    def __call__(self,data):
        return self.derive(self.data[1],self.names)
    def derive(self, data,names):
        """
                    Derivation numerique
                    !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
                    TODO Faire recevoir et retourner un vecteur panda
                    :param data: -> vecteur panda > Contient les donnees a deriver
                    :param dt: TODO Louis-Philippe que veux tu dire par "pas de temps" ??
                    :return: -> vecteur panda > vecteur des donnees derivees
                    """
        # Dérivation numérique
        # data = vecteur de données
        # dt   = pas de temps
         # vecteur de sortie
        dt = 0.001
        integ_list = np.zeros(shape=((len(data)-0),len(data[1])))
        for x in range(len(data)):
            integ_list[x][0] = data[x][0]
        hs3 = dt / 3  # h/3
        for x in range(1, len(names)):
            for i in range(len(data)):
                if i == 0 or i == (len(data) - 1):  # point 1 ou final : methode des rectangles
                    integ_list[i][x]= ((data[i][x] * dt))
                else:  # point médiants : méthode de simpson (plus précis)
                    # ref: https://en.wikipedia.org/wiki/Simpson's_rule
                    integ_list[i][x] =(((data[i - 1][x] + 4 * data[i][x] + data[i + 1][x]) * hs3))
        return integ_list

class Range_selection:
    """
    Selectionne et retourne un vecteur contenant les valeurs correspondantes a la fourchette de temps selectionnee
    """
    def __init__(self,first,last,data):
        """
        :param first: -> int > premiere donne de temps
        :param last: -> int > derniere donnee de temps
        """
        self.first = first
        self.last = last
        self.type = "range_selection"
        self.names = data[0].names
        self.new_numpy = np.zeros(shape=((last-first),len(data[1][0])))
    def __call__(self, data):
        """

        TODO samedi Philippe
        :param data: La totalite des donnees temporelles en cours d analyse
        :return: -> vecteur panda > Nouveau vecteur de donnees temporelles
        """
        for i in range(len(data[1][0])):
            for e in range(self.first ,self.last):
                self.new_numpy[e][i] = data[1][e][i]
        return self.new_numpy

