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

    def addData(self, datafile):
        """
        instancier un objet de data dans le datavibes du model
        Note: is it useful if so we need to modify add_transformation to review the tuple
        :return: none
        """
        self.model.data.add_transformation(vibes.ImportFile,None,datafile)


    def addTransform(self,type):
        """
        ajouter une transformation dans l'objet datavibes du model
        """
        self.model.data.add_transformation(vibes.Filter,type)
        pass

    def dataRangeSelections(self,first,last):
         """
         fait une selection de donnée dans la section des données temporelles.
         update le view en mettant en evidence les limites
         ***definire comment modifier datavibes en conséquence***
         :param self:
         :return:
         """
        # self.model.data.transformations[len(self.model.data.transformations) - 1].RangeMarkUp = True
         #self.model.data.transformations[len(self.model.data.transformations) - 1].first = first
         #self.model.data.transformations[len(self.model.data.transformations) - 1].last = last
         print(self.model.data.transformations[len(self.model.data.transformations)-1][1])
         NameArray = ["time","x","y","z","gforce"]
         for x in range(0,len(NameArray)):
             self.DataSeparation(first, last, NameArray[x])
         print(self.model.data.transformations[len(self.model.data.transformations)-1][1])
         self.addData(self.model.data.transformations[len(self.model.data.transformations)-1][1])
         self.model.data.transformations[len(self.model.data.transformations) - 1][1].first = first

    def DataSeparation(self,first,last,Name):
        for x in range(0, last - first):
            self.model.data.transformations[len(self.model.data.transformations)-1][1].loc[:, Name][x] = self.model.data.transformations[len(self.model.data.transformations)-1][1].loc[:, Name][x + first]


    def popUpGraphic(self):
        """
        retire le graphics du model
        :return:
        """
        pass


