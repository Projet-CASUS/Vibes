import sys
import vibes
import vibes.View.view as view
import vibes.Model.model as models
import vibes.Controller.transform as trans
from qwt.qt.QtGui import (QApplication)
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMainWindow
from qwt.qt.QtGui import QApplication
from qwt import QwtPlot, QwtPlotCurve
from decimal import Decimal
class Controller():
    def __init__(self,datafile):
        """
        Init:
            reçois les argument sys.argv pour contruire un Qt application

        """
        self.myinterface = view.graphical_interface()
        self.model = models.Model(datafile)
    def add_data(self, type, datafile):
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
        self.model.data.add_transformation(vibes.Filter,index,type)
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

    def show_of_time_graphic(self):
        """
        TODO Philippe
        afficher le graphique en temporelle du model
        :return:
        """

        x = [None]*len(self.model.data.transformations[-1][1])
        y = [None]*len(self.model.data.transformations[-1][1])
        for i in range(0, len(x)):
            x[i] = float(self.model.data.transformations[-1][1].loc[:, "time"][i].replace(',', '.'))

        for i in range(0, len(y)):
            y[i] = float(self.model.data.transformations[-1][1].loc[:, "x"][i].replace(',', '.'))
        curve1 = QwtPlotCurve("Curve 1")
        curve1.setData(x, y)
        curve1.attach(self.myinterface.mytimeplot)
        self.myinterface.mytimeplot.resize(600, 300)
        self.myinterface.mytimeplot.replot()
        self.myinterface.mytimeplot.show()





