import vibes.transform as transform
DEFAULT_HPTFX = "default.hptfx"


class DataVibes:
    """

    """

    def __init__(self, datafile, type='csv', funcfile=DEFAULT_HPTFX):
        """
        Initialise la classe de DataVibes
        :param tempfile: fichier des données temporelles
        :param funcfile: fichier des fonctions de transformation
        """
        import_func = transform.ImportFile(type=type)
        self.transformations = [[import_func, import_func(datafile)]]

    def add_transformation(self, cls, *args, **kwargs):
        """
        Ajoute une transformation à la fin de la liste de transformations
        :param cls: une classe de type Tranformation (mais pas ImportFile)
        :param args: arguments pour l'initialisation de la classe cls
        :param kwargs: arguments pour l'initialisation de la classe cls
        :return:
        """
        func = cls(*args, **kwargs)
        self.transformations.append([func, func(self.transformations[-1][1])])

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

