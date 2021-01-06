import csv

import numpy as np
import scipy

convolve = np.convolve
import scipy.signal as signal
from scipy import fftpack


class fourier:

    def __init__(self):
        pass

    def fourier(self, data, names, data_index=-1):
        x = [0] * len(data)
        for i in range(len(data)):
            x[i] = data[i][0]
        y = [0] * len(data)
        for i in range(len(data)):
            y[i] = data[i][1]
        if (x[-1] <= 1):
            sample_rate = len(x) * 1 / x[-1]
        else:
            sample_rate = len(x) / x[-1]
        columns_name = names
        freq, count, freq_complete = self.defineX(x, sample_rate)
        for n in range(1, len(columns_name)):
            fourier_complete, fourier_no_complexe = self.defineY(y, count)
        return freq, freq_complete, fourier_complete, fourier_no_complexe,sample_rate

    def defineX(self, data, sample_rate):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
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
        Convertie les donnee temporelle en frequentielle
        """
        fourier = fftpack.fft(data)
        fourier_no_complex = [0] * count;
        for x in range(0, count):
            fourier_no_complex[x] = fourier[x].real
        return fourier, fourier_no_complex


class import_file(fourier):
    def __init__(self, file_type='csv'):
        self.type = file_type

    def __call__(self, filename):
        if self.type == 'csv':
            with open(filename, newline='') as f:
                reader = csv.reader(f)
                self.names = next(reader)
                data = np.loadtxt(filename, delimiter=',', skiprows=1)
                self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(data,
                                                                                                              self.names)
            return data
        else:
            return filename


class Filter_Fir(fourier):
    """
    Retourne les valeurs filtrees des donnes fournies en parametres
    """

    def __init__(self, sample_rate, cut_off, cut_off2, data, type, num_taps=5):
        """
        :param sample_rate: -> int > Quantite de donnee par seconde
        :param num_taps: TODO Louis-Philippe decrire le type et l utilite
        """
        self.names = data[0].names
        self.sample_rate = sample_rate
        self.num_taps = num_taps
        self.fir_filter = None
        self.cut_off = cut_off
        self.cut_off2 = cut_off2
        self.type = type

    def __call__(self, data):
        """
        TODO donner un exemple de call
        :param data: -> panda > donnees a filtrer
        :param type: -> string >    type de filtre
        :param cut_off: -> int or list > frequence de coupure
        :return: -> panda > sequence de donnees filtrees
        """

        # On définit le filtre à utiliser
        if self.type == "passe_bas":
            self.fir_filter = self.passe_bas()
        elif self.type == "passe_haut":
            self.fir_filter = self.passe_haut()
        elif self.type == "passe_bande":
            self.fir_filter = self.passe_bande()

        dataY = [0] * len(data[1])
        for i in range(0, len(data[1])):
            dataY[i] = data[1][i][1]
        # On effectue la convolution du filtre FIR
        filtered_data = convolve(dataY, self.fir_filter, 'same')
        filtered_numpy = np.zeros(shape=(len(filtered_data), (len(data))))
        for i in range(0, len(filtered_numpy)):
            filtered_numpy[i][0] = data[1][i][0]
            filtered_numpy[i][1] = filtered_data[i]
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(filtered_numpy,
                                                                                                      self.names)
        return filtered_numpy

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

    def passe_bande(self):  # Définit le vecteur de filtre FIR pour un passe bande
        """
        :return: vecteur de filtre FIR pour un passe bande
        """
        f1 = float(self.cut_off / self.sample_rate)
        f2 = float(self.cut_off2 / self.sample_rate)
        return signal.firwin(self.num_taps, [f1, f2], pass_zero=False)


class Differential(fourier):
    def __init__(self, data):
        self.names = data[0].names
        self.type = "Differential"

    def __call__(self, data):
        return self.derive(data[1])

    def derive(self, data):
        """
        Derivation numerique
        !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
        TODO Faire recevoir et retourner un vecteur panda
        :param data: -> vecteur panda > Contient les donnees a deriver
        :param dt: TODO Louis-Philippe que veux tu dire par "pas de temps" ??
        :return: -> vecteur panda > vecteur des donnees derivees
        """
        drv_list = np.zeros(shape=((len(data) - 1), len(data[1])))
        drv_listx = [0] * len(data)
        drv_listy = [0] * len(data)
        for x in range(len(data)):
            drv_listx[x] = data[x][0]
        for x in range(len(data)):
            drv_listy[x] = data[x][1]
        dx = np.diff(drv_listx)
        dydx = np.diff(drv_listy) / dx
        maxValue = 0
        minValue = 0
        for i in range(len(dydx)):
            drv_list[i][0] = drv_listx[i]
            if (drv_listy[i] > maxValue):
                maxValue = drv_listy[i]
            if (drv_listy[i] < minValue):
                minValue = drv_listy[i]
            if (dx[i] == 0):
                if (drv_listy[i] > 0):
                    drv_list[i][1] = maxValue
                else:
                    drv_list[i][1] = minValue
            else:
                drv_list[i][1] = dydx[i]
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(drv_list,
                                                                                                      self.names)
        return drv_list


class Integral(fourier):
    def __init__(self, data):
        self.names = data[0].names
        self.type = "Integral"

    def __call__(self, data):
        return self.integral(data[1], self.names)

    def integral(self, data, names):
        """
        Derivation numerique
        !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
        TODO Faire recevoir et retourner un vecteur panda
        :param data: -> vecteur panda > Contient les donnees a deriver
        :param dt: TODO Louis-Philippe que veux tu dire par "pas de temps" ??
        :return: -> vecteur panda > vecteur des donnees derivees
        """
        dt = 0.001
        integ_list = np.zeros(shape=((len(data) - 0), len(data[1])))
        for x in range(len(data)):
            integ_list[x][0] = data[x][0]
        hs3 = dt / 3  # h/3
        for x in range(1, len(names)):
            for i in range(len(data)):
                if i == 0 or i == (len(data) - 1):  # point 1 ou final : methode des rectangles
                    integ_list[i][x] = ((data[i][x] * dt))
                else:  # point médiants : méthode de simpson (plus précis)
                    # ref: https://en.wikipedia.org/wiki/Simpson's_rule
                    integ_list[i][x] = (((data[i - 1][x] + 4 * data[i][x] + data[i + 1][x]) * hs3))
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(integ_list,
                                                                                                      self.names)
        return integ_list


class Range_selection(fourier):
    """
    Selectionne et retourne un vecteur contenant les valeurs correspondantes a la fourchette de temps selectionnee
    """

    def __init__(self, first, last, data):
        """
        :param first: -> int > premiere donne de temps
        :param last: -> int > derniere donnee de temps
        """
        self.first = first
        self.last = last
        self.type = "range_selection"
        self.names = data[0].names


    def __call__(self, data):
        """

        TODO samedi Philippe
        :param data: La totalite des donnees temporelles en cours d analyse
        :return: -> vecteur panda > Nouveau vecteur de donnees temporelles
        """
        new_numpy = np.zeros(shape=((self.last - self.first), len(data[1][0])))
        for i in range(len(data[1][0])):
            for e in range(self.first, self.last):
                new_numpy[e - self.first][i] = data[1][e][i]
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(new_numpy,
                                                                                                      self.names)
        return new_numpy


class Merge(fourier):

    def __init__(self, data):
        self.nbMerge = 0
        self.ctpMerge = 0
        self.cptsearch = 0
        self.type = "merge"
        self.first = 0
        self.last = 0
        self.names = data[-1][0].names
        self.transformations = data
        self.newData = self.defineNewData()

    def defineNewData(self):
        for i in range(len(self.transformations)):
            position = self.transformations[len(self.transformations) - 1 - i]
            if (position[0].type == "merge"):
                self.nbMerge = self.nbMerge + 1
            if (position[0].type == "range_selection" or position[0].type == "csv"):
                if (position[0].type == "range_selection"):
                    self.first = position[0].first
                if (self.nbMerge == self.ctpMerge):
                    newData1 = np.zeros(shape=((len(position[1]) - 1), len(position[-1][0])))
                    for x in range(len(newData1)):
                        newData1[x] = position[-1][x]
                    return newData1
                else:
                    self.ctpMerge = self.ctpMerge + 1

    def __call__(self, data):

        length = len(self.transformations[len(self.transformations) - 1][-1])
        for x in range(length):
            if (len(self.newData) > length + self.first):
                self.newData[x + self.first] = self.transformations[len(self.transformations) - 1][-1][x]
            else:
                self.newData[x] = self.transformations[len(self.transformations) - 1][-1][x]
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(self.newData,
                                                                                                      self.names)
        return self.newData


class Filter(fourier):

    def __init__(self, data, datafourier, cut_off, cut_off2, attenuation, type):
        self.state = True
        self.dataFourier = datafourier
        self.names = data[0].names
        self.cut_off = cut_off/2
        self.cut_off2 = cut_off2/2
        self.attenuation = attenuation
        self.type = type

    def __call__(self, data):
        new_data = self.filtering(data,self.dataFourier)
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(new_data,
                                                                                                      self.names)
        return new_data

    def filtering(self,data, dataFourier):
        # TODO modification manuelle des signaux

        if (self.type == "passe_bas"):
            for i in range(0, len(dataFourier[0])):
                currentDataTime = dataFourier[0][i]
                currentDataimpulse = dataFourier[1][i]
                if (currentDataTime < 0):
                    if (currentDataTime < -1 * self.cut_off):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse
                elif (currentDataTime >= 0):
                    if (currentDataTime > self.cut_off):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse

        if (self.type == "passe_haut"):
            for i in range(0, len(dataFourier[0])):
                currentDataTime = dataFourier[0][i]
                currentDataimpulse = dataFourier[1][i]
                if (currentDataTime < 0):
                    if (currentDataTime > -1 * self.cut_off):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse
                elif (currentDataTime >= 0):
                    if (currentDataTime < self.cut_off):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse

        if (self.type == "passe_bande"):
            for i in range(0, len(dataFourier[0])):
                currentDataTime = dataFourier[0][i]
                currentDataimpulse = dataFourier[1][i]
                if (currentDataTime < 0):
                    if (currentDataTime > -1 * self.cut_off):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse
                    elif (currentDataTime < -1 * self.cut_off2):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse
                elif (currentDataTime >= 0):
                    if (currentDataTime < self.cut_off):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse
                    elif (currentDataTime > self.cut_off2):
                        dataFourier[1][i] = self.attenuation * currentDataimpulse

        itx = scipy.fft.ifft(dataFourier[1])
        dataNumpy = np.zeros(shape=((len(itx)), len(data)))
        for i in range(0, len(itx)):
            dataNumpy[i][0] = data[1][i][0]
            dataNumpy[i][1] = itx[i]
        return dataNumpy
