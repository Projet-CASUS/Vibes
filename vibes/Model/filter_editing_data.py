from IPython.external.qt_for_kernel import QtGui
import vibes.Controller.transform as transform
import wave, struct
import numpy as np

import vibes.Model.filter_editor as filter_editor

DEFAULT_HPTFX = "default.hptfx"


class Data:

    def __init__(self, data_in, data_out, transform_func_file=None):
        """
        Initialise la classe de Data
        :param data_file: fichier des données temporelles
        :param transform_func_file: -> fichier de type .xml > contient des fonctions de transformation sauvegardees
        """
        """
        import_func_type: -> string > le type de fonction dans la pipeline par exemple: csv
        transformations: -> transformation[] > ceci est la pipeline browser contenant toute les objets data et leur type de transformation subie.
        """
        import_func_type = filter_editor.filter_editor()
        self.transformations = [[import_func_type, import_func_type(data_in,data_out)]]

    def insert_transformation(self, cls, index=-1):
        """
        Insert une transformation dans la liste des transformations
        :param cls: une classe de type Tranformation (mais pas ImportFile)
        :param index: indice où insérer la nouvelle transformation dans la liste
        :param args: arguments pour l'initialisation de la classe cls
        :param kwargs: arguments pour l'initialisation de la classe cls
        :return:
        """
        func = cls()
        if index == -1:
            self.transformations.append([func, func(self.transformations[index])])
        else:
            self.transformations.insert(index, [func, func(self.transformations[index])])
            self.recalculate_data_through_pipeline(index)

    def recalculate_data_through_pipeline(self, idx=0):
        """
        Recalculer les données dans la liste de transformations
        chaque fois qu une transformation est ajoutee ou retiree
        :param idx: Endroit à partir du quel on recalcule
        """
        for i in range(idx, len(self.transformations)):
            self.transformations[i][1] = self.transformations[i][0](self.transformations[i - 1][1])
