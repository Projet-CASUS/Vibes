import sys
import vibes
import vibes.View.view as view
import vibes.Model.model as models
import vibes.Controller.transform as trans
from qwt.qt.QtGui import (QApplication)
import pandas as pd
class Controller():
    def __init__(self,datafile):
        """
        Init:
            reçois les argument sys.argv pour contruire un Qt application

        """
        self.app = QApplication(sys.argv)
        self.view = view.GraphicalInterface()
        self.model = models.Model(datafile)

    def add_data(self,type ,datafile):
        """
        todo Daniel
        instancier un objet de data dans le datavibes du model
        Note: is it useful if so we need to modify add_transformation to review the tuple
        :return: none
        """
        self.model.data.add_transformation(vibes.ImportFile,type,datafile)


    def add_transform(self, type,index =-1):
        """
        TODO Vianney
        ajouter une transformation dans l'objet datavibes du model
        """
        self.model.data.add_transformation(vibes.Filter,index ,type)
        pass

    def data_range_selections(self, first, last , index = -1):
         """
         TODO Philippe
         fait une selection de donnée dans la section des données temporelles.
         update le view en mettant en evidence les limites
         ***definire comment modifier datavibes en conséquence***
         :param self:
         :return:
         """
         self.model.data.add_transformation(vibes.Controller.transform.RangeSelection,index,first,last)


    def pop_up_graphic(self):
        """
        TODO philippe
        retire le graphics du model
        :return:
        """
        pass


