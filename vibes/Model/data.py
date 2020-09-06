from IPython.external.qt_for_kernel import QtGui

import vibes.Controller.transform as transform
import wave, struct
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
        if transform_func_file is None:
            # TODO philipe: decrire ce qui se passe
            import_func = transform.import_file(file_type=file_type)
            self.transformations = [[import_func, import_func(data_file)]]
        else:
            # TODO philipe: decrire ce qui se passe
            self.transformations = []
            self.read_hptfx(transform_func_file, data_file)
            self.currentIndex = 0

    def read_hptfx(self, funcfile, datafile=None):
        """
        Peupler la liste transformations à partir d'un fichier hptfx
        :param funcfile: Path d'un fichier hptfx
        :param datafile: Path d'un fichier de données
        :return:
        """
        pass

    def add_data(self):
        """
        TODO philipe: est-ce encore utile?
        todo Daniel Ajouter un importfile dans le transformation pipline
        :return:
        """
        pass

    def add_transformation(self, cls,index = -1 ,*args, **kwargs, ):
        """
        TODO Philipe: Est-ce encore utile?
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
        TODO philipe: Utilise nulle part jusqu a maintenant... encore utile?
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
        TODO philipe: On la garde??? > semble n etre utilise que par la fonction juste avant qui elle n est utilisee nulle part... est-ce elle que tu utilise ou on s en debarasse>
        Recalculer les données dans la liste de transformations
        chaque fois qu une transformation est ajoutee ou retiree
        :param idx: Endroit à partir du quel on recalcule
        """
        for i in range(idx, len(self.transformations)):
            self.transformations[i][1] = self.transformations[i][0](self.transformations[i-1][1])

    def export_wav(self, data, sample_rate, file_name):
        """
        TODO Adapter cette fonction pour recevoir un vecteur panda
        TODO creer un repertoire par defaut dans le filesystem de Vibes dans lequel generer les fichiers wav - gerer le .gitignore afin que son contenu ne soit pas partage
        :param data: -> vecteur panda > donnees permettant de generer un fichier .wav
        :param sample_rate: quantite de donnees par secondes contenues dans le vecteur data
        :param file_name: -> string > nom du fichier a sauvegarder
        """
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        f = wave.open(filename + '{}.wav'.format(file_name), 'w')
        f.setnchannels(1) # mono (donc non-stereo)
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



