import csv
from decimal import Decimal
from tokenize import Double

import numpy as np
import scipy

convolve = np.convolve
import scipy.signal as signal
from scipy import fftpack
from scipy import integrate

class fourier:
    """
    cette class sert à calculer les éléments nécessaires pour le fonctionnement de certaine manipulation avec les filtres
    ainsi que les éléments nécessaires pour l'affichages des graphiques
    """
    def fourier(self, data, names):
        """
        :param data: -> numpy > des données temporelles d'une transformations
        :param names: -> listes > de noms des colonnes représentant les différentes y
        :return: -> freq, freq_complete, fourier_complete, fourier_no_complexe, sample_rate
        Orchestrer et calculer les information nécessaires pour tout ce qui entoure le fréquentiel
        """
        #ici on fait la convertion de numpy à un simple array
        x = [0] * len(data)
        for i in range(len(data)):
            x[i] = data[i][0]
        y = [0] * len(data)
        for i in range(len(data)):
            y[i] = data[i][1]
        #ici on calcule le sample rate
        if (x[-1] <= 1):
            sample_rate = len(x) * 1 / x[-1]
        else:
            sample_rate = len(x) / x[-1]
        columns_name = names
        # cette fonction retourne toute les frequences et celle seulement positives pour l'affichages. Count est un paramêtre utile pour calculer seulement les amplitudes des fréquences positives
        freq, count, freq_complete = self.defineX(x, sample_rate)
        for n in range(1, len(columns_name)):
        # Ici on calcule toute les amplitude de fourier ainsi que ceux positives sans nombre complexe pour l'affichage
            fourier_complete, fourier_no_complexe, fourier_no_complexe_positive = self.defineY(y, count)
        return freq, freq_complete, fourier_complete, fourier_no_complexe,fourier_no_complexe_positive,sample_rate

    def defineX(self, data, sample_rate):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
        :return: -> freq_return, count, freq
        Convertie les donnee temporelle en frequentielle

        """
        n = len(data)
        freq = fftpack.fftfreq(n) * sample_rate
        i = 0
        while (freq[i] >= 0):
            i = i + 1
        freq_return = [0] * i
        for x in range(0, i):
            freq_return[x] = freq[x]
        return freq_return, i, freq

    def defineY(self, data, count):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
        :return: -> fourier, fourier_no_complex
        Convertie les donnee temporelle en frequentielle
        """
        fourier = fftpack.fft(data)
        fourier_no_complex = [0] *len(fourier);
        fourier_no_complex_positive = [0] * count
        for x in range(0, len(fourier)):
            fourier_no_complex[x] = fourier[x].real
        for x in range(0,count):
            fourier_no_complex_positive[x] = fourier[x].real
        return fourier, fourier_no_complex,fourier_no_complex_positive
