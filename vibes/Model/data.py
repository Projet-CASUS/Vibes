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
            import_func = transform.ImportFile(type=type)
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

    def export_data(self, data, freq):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        wavef = wave.open(filename + '.wav','w')
        wavef.setnchannels(1) # mono
        wavef.setsampwidth(2)
        wavef.setframerate((1/freq))
        for i in range(len(data)):
            wavefile = struct.pack('<h', data[i])
            wavef.writeframesraw(wavefile)
        wavef.close()
        print('Fichier wav généré au répertoire: ')


    def export_func(self):
        pass

    def refresh_graphics(self):
        """
        mettre à jour les graphiques du view
        design pattern observer
        :return:
        """
        pass



