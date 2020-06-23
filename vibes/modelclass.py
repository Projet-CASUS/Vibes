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
        func = cls(*args, **kwargs)
        self.transformations.append([func, func(self.transformations[-1][1])])

    def export_data(self):
        pass

    def export_func(self):
        pass

