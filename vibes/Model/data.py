from IPython.external.qt_for_kernel import QtGui

import vibes.Controller.transform as transform
import wave, struct
DEFAULT_HPTFX = "default.hptfx"

# TODO: add del_transformation
# TODO: add undo/redo system
# TODO: load/save/export (strategy pattern)

class data:
    """

    """

    def __init__(self, data_file, type='csv', func_file=None):
        """
        Initialise la classe de DataVibes
        :param tempfile: fichier des données temporelles
        :param func_file: fichier des fonctions de transformation
        """
        if func_file is None:
            import_func = transform.import_file(type=type)
            self.transformations = [[import_func, import_func(data_file)]]
        else:
            self.transformations = []
            self.read_hptfx(func_file, data_file)
            self.currentIndex =0;

    def read_hptfx(self, funcfile, datafile=None):
        """
        Peupler la liste transformations à partir d'un fichier hptfx
        :param funcfile: Path d'un fichier hptfx
        :param datafile: Path d'un fichier de données
        :return:
        """
        pass
        # TODO: parser hptfx

    def add_data(self):
        """
        todo Daniel Ajouter un importfile dans le transformation pipline
        :return:
        """
        pass

    def add_transformation(self, cls,index = -1 ,*args, **kwargs, ):
        """
        Ajoute une transformation à la fin de la liste de transformations
        :param cls: une classe de type Tranformation (mais pas ImportFile)
        :param args: arguments pour l'initialisation de la classe cls
        :param kwargs: arguments pour l'initialisation de la classe cls
        :return:
        """
        func = cls(*args, **kwargs)
        self.transformations.append([func, func(self.transformations[index][1])])

    def insert_transformation(self, cls, idx, *args, **kwargs):
        """
        Insert une transformation dans la liste des transformations
        :param cls: une classe de type Tranformation (mais pas ImportFile)
        :param idx: indice où insérer la nouvelle transformation dans la liste
        :param args: arguments pour l'initialisation de la classe cls
        :param kwargs: arguments pour l'initialisation de la classe cls
        :return:
        """
        func = cls(*args, **kwargs)
        self.transformations.insert(idx, [func, None])
        self.recalculate(idx)

    def recalculate(self, idx=0):
        """
        Recalculer les données dans la liste de transformations
        :param idx: Endroit à partir du quel on recalcule
        :return:
        """
        for i in range(idx, len(self.transformations)):
            self.transformations[i][1] = self.transformations[i][0](self.transformations[i-1][1])

    def export_wav(self, data, sample_rate):
        """
        TODO Adapter cette fonction pour recevoir un vecteur panda
        :param data: -> vecteur panda > donnees permettant de generer un fichier .wav
        :param sample_rate: quantite de donnees par secondes contenues dans le vecteur data
        """
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        f = wave.open(filename + '.wav', 'w')
        f.setnchannels(1) # mono
        f.setsampwidth(2) # two bytes / sample
        f.setframerate((1 / sample_rate)) # TODO Louis-Philipe es tu certain que c est 1/sample_rate? sample_rate et frame_rate semblent etre les deux en Hz
        for i in range(len(data)):
            # Permet de mettre les donnees dans le bon format afin de les ecrire en .wav
            wave_data = struct.pack('<h', data[i])
            f.writeframesraw(wave_data)
        f.close()
        print('Fichier wav généré au répertoire: ')


    def export_func(self):
        """
        todo Philipe : On en avait besoin pour quoi deja ca???
        """
        pass

    def refresh_graphics(self):
        """
        TODO Philippe: en as-t-on vraiment besoin?
        mettre à jour les graphiques du view
        design pattern observer
        :return:
        """
        pass



