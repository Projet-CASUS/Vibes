import vibes.Controller.transform as transform
DEFAULT_HPTFX = "default.hptfx"

# TODO: add del_transformation
# TODO: add undo/redo system
# TODO: load/save/export (strategy pattern)

class DataVibes:
    """

    """

    def __init__(self, datafile, type='csv', funcfile=None):
        """
        Initialise la classe de DataVibes
        :param tempfile: fichier des données temporelles
        :param funcfile: fichier des fonctions de transformation
        """
        if funcfile is None:
            import_func = transform.ImportFile(type=type)
            self.transformations = [[import_func, import_func(datafile)]]
        else:
            self.transformations = []
            self.read_hptfx(funcfile, datafile)
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

    def export_data(self):
        pass

    def export_func(self):
        pass

    def refresh_graphics(self):
        """
        mettre à jour les graphiques du view
        design pattern observer
        :return:
        """
        pass



