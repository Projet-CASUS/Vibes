from IPython.external.qt_for_kernel import QtGui
from scipy import fftpack

from scipy.interpolate import interp1d
import vibes.Controller.transform as transform
import wave, struct
import numpy as np
DEFAULT_HPTFX = "default.hptfx"

# TODO: add del_transformation
# TODO: add undo/redo system
# TODO: load/save/export (strategy pattern)

class Data:
    """

    """
    def __init__(self, data_file, file_type='csv', transform_func_file=None):
        """
        Initialise la classe de Data
        :param data_file: fichier des données temporelles
        :param transform_func_file: -> fichier de type .xml > contient des fonctions de transformation sauvegardees
        """
        self.transformations_fourier = []
        if transform_func_file is None:
            """
            import_func_type: -> string > le type de fonction dans la pipeline par exemple: csv
            transformations: -> transformation[] > ceci est la pipeline browser contenant toute les objets data et leur type de transformation subie.
            """
            import_func_type = transform.import_file(file_type=file_type)
            self.transformations = [[import_func_type, import_func_type(data_file),self.fourier()]]
        else:
            """
            si transform_func_file contient deja des data
            """
            self.transformations = []
            self.read_hptfx(transform_func_file, data_file)
            self.currentIndex = 0

    def fourier(self,data_index = -1):
        x = [0]*len(self.transformations[-1][1])
        for i in range(len(self.transformations[-1][1])):
            x[i] = self.transformations[-1][1][i][0]
        y = [0] * len(self.transformations[-1][1])
        for i in range(len(self.transformations[-1][1])):
            y[i] = self.transformations[-1][1][i][1]
        if (x[-1] <= 1):
            sample_rate = len(x) * 1 / x[-1]
        else:
            sample_rate = len(x) / x[-1]
        columns_name = self.model.data.transformations[data_index][0].names
        freq, count, freq_complete = self.defineX(x, sample_rate)
        for n in range(1, len(columns_name)):
            fourier_complete, fourier_no_complexe = self.defineY(y, count)
            self.model.data.insert_transformation_fourier([freq_complete, fourier_complete])
        return fourier_no_complexe

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
        freqreturn = [0] * i
        for x in range(0, i):
            freqreturn[x] = freq[x]
        return freqreturn, i, freq

    def defineY(self, data, count):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
        Convertie les donnee temporelle en frequentielle
        """
        fourier = fftpack.fft(data)
        fourierNoComplex = [0] * count;
        for x in range(0, count):
            fourierNoComplex[x] = fourier[x].real
        return fourier, fourierNoComplex

    def read_hptfx(self, funcfile, datafile=None):
        """
        Peupler la liste transformations à partir d'un fichier hptfx
        :param funcfile: Path d'un fichier hptfx
        :param datafile: Path d'un fichier de données
        :return:
        """
        pass

    def insert_transformation(self, cls, index=-1, *args, **kwargs):
        """
        Insert une transformation dans la liste des transformations
        :param cls: une classe de type Tranformation (mais pas ImportFile)
        :param index: indice où insérer la nouvelle transformation dans la liste
        :param args: arguments pour l'initialisation de la classe cls
        :param kwargs: arguments pour l'initialisation de la classe cls
        :return:
        """
        func = cls(*args, **kwargs)
        if index == -1:
            self.transformations.append([func, func(self.transformations[index])])
        else:
            self.transformations.insert(index,[func, func(self.transformations[index])])
            self.recalculate_data_through_pipeline(index)

    def insert_transformation_fourier(self,data):
        self.transformations_fourier.append(data)

    def recalculate_data_through_pipeline(self, idx=0):
        """
        Recalculer les données dans la liste de transformations
        chaque fois qu une transformation est ajoutee ou retiree
        :param idx: Endroit à partir du quel on recalcule
        """
        for i in range(idx, len(self.transformations)):
            self.transformations[i][1] = self.transformations[i][0](self.transformations[i-1][1])

    def export_wav(self, data, max=np.power(2, 15)):
        """
        TODO creer un repertoire par defaut dans le filesystem de Vibes dans lequel generer les fichiers wav + gerer le .gitignore afin que son contenu ne soit pas partage
        :param data: -> vecteur panda > donnees permettant de generer un fichier .wav
        :param sample_rate: quantite de donnees par secondes contenues dans le vecteur data
        :param file_name: -> string > nom du fichier a sauvegarder
        """
        max_value = data.transformations[-1][-1][-1][0]

        for x in range(1,len(data.transformations[-1][-1][0])):
            for i in range(len(data.transformations[-1][-1])):
                if(data.transformations[-1][-1][i][x] > max_value):
                    max_value = data.transformations[-1][-1][i][x]
        x_data =[0]*len(data.transformations[-1][-1])
        for x in range(len(data.transformations[-1][-1])):
            x_data[x] =  data.transformations[-1][-1][x][0]

        sample_rate = 0
        if (x_data[-1] <= 1):
            sample_rate = len(x_data) * 1 / x_data[-1]
        else:
            sample_rate = len(x_data) / x_data[-1]
        #if (data.transformations[-1][-1][-1][0] <= 1):
        #    sample_rate = len(data.transformations[-1][-1]) * 1 / data.transformations[-1][-1][-1][0]
        #else:
        #    sample_rate = len(data.transformations[-1][-1]) / data.transformations[-1][-1][-1][0]
        filename = QtGui.QFileDialog.getSaveFileName()[0]
        f = wave.open(filename, 'wb')
        f.setnchannels(1) # mono (donc non-stereo)
        f.setsampwidth(2) # two bytes / sample
        f.setframerate(sample_rate)

        for x in range(1, len(data.transformations[-1][-1][0])):
            # Permet de mettre les donnees dans le bon format afin de les ecrire en .wav
            for i in range(len(data.transformations[-1][-1])):
                value = int((data.transformations[-1][-1][i][x]/max_value)*max)
                wave_data = struct.pack('<h', value)
                f.writeframesraw(wave_data)

        f.close()
        print('Fichier wav généré au répertoire: ')




"""
    def arr_to_wav(vect, sampleRate=44100.0, title='bacon', min=(-1 * (np.power(2, 15))), max=np.power(2, 15)):

        mon_repertoire = os.getcwd()

        if main.debug:

        print('FX: arr_to_wav')

        print('sampleRate = ' + str(sampleRate))

        print('min ; max = ' + str(min) + ' ; ' + str(max))

        # sampleRate = 44100.0 # hertz

        # frequency = 900.0 # hertz

        wavef = wave.open(mon_repertoire + title + '.wav', 'w')

        wavef.setnchannels(1)  # mono

        wavef.setsampwidth(2)

        wavef.setframerate(sampleRate)

        for i in range(len(vect)):

        value = int((((vect[i] - min) * 65533) / (max - min)) - 32767)

        data = struct.pack('<h', value)

        wavef.writeframesraw(data)

        wavef.close()

        print('Fichier wav généré au répertoire: ' + mon_repertoire)
"""




