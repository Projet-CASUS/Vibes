import csv

import numpy as np
import scipy

convolve = np.convolve
import scipy.signal as signal
from scipy import fftpack


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
            fourier_complete, fourier_no_complexe = self.defineY(y, count)
        return freq, freq_complete, fourier_complete, fourier_no_complexe,sample_rate

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
        fourier_no_complex = [0] * count;
        for x in range(0, count):
            fourier_no_complex[x] = fourier[x].real
        return fourier, fourier_no_complex


class import_file(fourier):
    """
    Ceci représente la première transformation dans le pipeline elle importe un fichier et le met dans un numpy
    """
    def __init__(self, file_type='csv'):
        """
        :param file_type: ->  string > représente le type de fichier que l'on utilise
        """
        self.type = file_type

    def __call__(self, filename):
        """
        :param filename: -> string > représente le nom du fichier que l'on veut utiliser pour nos données initiales
        :return: -> data or filename
        ici on prend les données qui se retrouve dans le fichier et on les converties dans un numpy
        """
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
        :param num_taps: -> int > un coefficient et une réponse impulsionnaire d'un filtre FIR
        :param cut_off: -> float > le cut_off de la plus petite valeur fréquentielle
        :param cut_off2: -> float > le cut_off2 de la plus grande valeur fréquentielle
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param type: -> type > le type de filtre
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
        :return: -> filtered_numpy
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
    """
    permet de calculer la différentiel de donner temporelle
    """
    def __init__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        """
        self.names = data[0].names
        self.type = "Differential"

    def __call__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :return: -> donnée dériver
        """
        return self.derive(data[1])

    def derive(self, data):
        """
        Derivation numerique
        !!! -> attention cette methode fait perdre la premiere et la derniere donnee du vecteur
        :param data: -> vecteur panda > Contient les donnees a deriver
        :return: -> vecteur panda > vecteur des donnees derivees
        """
        #Initialisation de structure de données
        drv_list = np.zeros(shape=((len(data) - 1), len(data[1])))
        drv_listx = [0] * len(data)
        drv_listy = [0] * len(data)
        # loading arrays with data
        for x in range(len(data)):
            drv_listx[x] = data[x][0]
        for x in range(len(data)):
            drv_listy[x] = data[x][1]
        # caculer la dériver
        dx = np.diff(drv_listx)
        dydx = np.diff(drv_listy) / dx
        #loader le numpy
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
    """
    class en construction qui permet de calculer des integrales poir des données temporelles
    """
    def __init__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        """
        self.names = data[0].names
        self.type = "Integral"

    def __call__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :return: -> integrale des données temporelles
        """
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
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        """
        self.first = first
        self.last = last
        self.type = "range_selection"
        self.names = data[0].names


    def __call__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
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
    """
    permet de prendre une fourchette de données que l'on a modifier et la replacer dans le reste des données
    """
    def __init__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        """
        self.nb_merge = 0
        self.ctp_merge = 0
        self.cpt_search = 0
        self.type = "merge"
        self.first = 0
        self.last = 0
        self.names = data[-1][0].names
        self.transformations = data
        self.new_data = self.define_new_data()

    def define_new_data(self):
        """
        permet de déterminer la grosseur de la structure de données contenant les données qui encapsule celle modifier
        :return: ->  a grosseur de la structure de données contenant les données qui encapsule celle modifier
        """
        for i in range(len(self.transformations)):
            position = self.transformations[len(self.transformations) - 1 - i]
            if (position[0].type == "merge"):
                self.nb_merge = self.nb_merge + 1
            if (position[0].type == "range_selection" or position[0].type == "csv"):
                if (position[0].type == "range_selection"):
                    self.first = position[0].first
                if (self.nb_merge == self.ctp_merge):
                    newData1 = np.zeros(shape=((len(position[1])), len(position[-1][0])))
                    for x in range(len(newData1)):
                        newData1[x] = position[-1][x]
                    return newData1
                else:
                    self.ctp_merge = self.ctp_merge + 1

    def __call__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :return: -> new_data > retourne les données modifier dans la structure la plus large
        """
        length = len(self.transformations[len(self.transformations) - 1][-1])
        for x in range(length):
            if (len(self.new_data) > length + self.first):
                self.new_data[x + self.first] = self.transformations[len(self.transformations) - 1][-1][x]
            else:
                self.new_data[x] = self.transformations[len(self.transformations) - 1][-1][x]
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(self.new_data,
                                                                                                                       self.names)
        return self.new_data


class Filter(fourier):
    """
    Retourne les valeurs filtrees des donnes fournies en parametres
    Cependant ce type de filtre est beaucoup plus efficaces en terme d'atténuation car elle fait toute les modification demander manuellement sur chaque fréquence
    """
    def __init__(self, data, data_fourier, cut_off, cut_off2, attenuation, type):
        """
        :param cut_off: -> float > le cut_off de la plus petite valeur fréquentielle
        :param cut_off2: -> float > le cut_off2 de la plus grande valeur fréquentielle
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param type: -> type > le type de filtre
        :param attenuation: -> float > coefficient d'attenuation des fréquences
        """
        self.data_fourier = data_fourier
        self.names = data[0].names
        self.cut_off = cut_off/2
        self.cut_off2 = cut_off2/2
        self.attenuation = attenuation
        self.type = type

    def __call__(self, data):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :return: -> new_data > retourne les données temporelle filtrée
        """
        new_data = self.filtering(data, self.data_fourier)
        self.freq, self.freq_complete, self.fourier_complete, self.fourier_no_complexe,self.sample_rate = self.fourier(new_data,
                                                                                                      self.names)
        return new_data

    def filtering(self, data, data_fourier):
        """
        :param data_fourier: -> numpy > les données fréquentielle
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :return: -> new_numpy > retourne les données temporelle filtrée
        """

        if (self.type == "passe_bas"):
            for i in range(0, len(data_fourier[0])):
                currentDataTime = data_fourier[0][i]
                currentDataimpulse = data_fourier[1][i]
                if (currentDataTime < 0):
                    if (currentDataTime < -1 * self.cut_off):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse
                elif (currentDataTime >= 0):
                    if (currentDataTime > self.cut_off):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse

        if (self.type == "passe_haut"):
            for i in range(0, len(data_fourier[0])):
                currentDataTime = data_fourier[0][i]
                currentDataimpulse = data_fourier[1][i]
                if (currentDataTime < 0):
                    if (currentDataTime > -1 * self.cut_off):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse
                elif (currentDataTime >= 0):
                    if (currentDataTime < self.cut_off):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse

        if (self.type == "passe_bande"):
            for i in range(0, len(data_fourier[0])):
                currentDataTime = data_fourier[0][i]
                currentDataimpulse = data_fourier[1][i]
                if (currentDataTime < 0):
                    if (currentDataTime > -1 * self.cut_off):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse
                    elif (currentDataTime < -1 * self.cut_off2):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse
                elif (currentDataTime >= 0):
                    if (currentDataTime < self.cut_off):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse
                    elif (currentDataTime > self.cut_off2):
                        data_fourier[1][i] = self.attenuation * currentDataimpulse

        itx = scipy.fft.ifft(data_fourier[1])
        data_numpy = np.zeros(shape=((len(itx)), len(data)))
        for i in range(0, len(itx)):
            data_numpy[i][0] = data[1][i][0]
            data_numpy[i][1] = itx[i]
        return data_numpy
