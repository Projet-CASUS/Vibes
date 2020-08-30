import sys
import vibes
import vibes.View.view as view
import vibes.Model.model as models
import vibes.Controller.transform as trans
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QFrame, QSlider, QHBoxLayout
from PyQt5.Qt import QApplication
from qwt import QwtPlot, QwtPlotCurve
from decimal import Decimal
class Controller():
    def __init__(self, datafile):
        """
        Init:
            reçois les argument sys.argv pour contruire un Qt application

        """
        self.app = QApplication(sys.argv)
        self.model = models.Model(datafile)
        self.myinterface = view.graphical_interface()
        self.myinterface.mainWindow.widget.pipelineSlider = QSlider()
        self.myinterface.mainWindow.widget.pipelineIndex = len(self.model.data.transformations[0])
        self.myinterface.mainWindow.widget.pipelineSlider.valueChanged.connect(self.value_changed)

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

    def show_of_freq_graphic(self, w=-1):
        NameArray = ["time", "x","y"]
        length = len(self.model.data.transformations[w][1])
        if (self.model.data.transformations[w][0].type == "RangeSelection"):
            length = self.model.data.transformations[w][0].last - self.model.data.transformations[w][0].first
        x = [None] * length
        for i in range(0, len(x)):
            x[i] = float(self.model.data.transformations[w][1].loc[:, NameArray[0]][i].replace(',', '.'))
            freq = self.myinterface.myfourierplot.defineX(x, 200)

        for n in range(1, len(NameArray)):
            y = [None] * length
            for i in range(0, len(y)):
                y[i] = float(self.model.data.transformations[w][1].loc[:, NameArray[n]][i].replace(',', '.'))
                fourier = self.myinterface.myfourierplot.defineY(y, 200)
            curve = QwtPlotCurve(NameArray[n])
            curve.setData(freq, fourier)
            curve.attach(self.myinterface.myfourierplot)
        self.myinterface.show_of_freq_plot()

    def show_of_time_graphic(self , w = -1):
        """
        TODO Philippe
        afficher le graphique en temporelle du model
        :return:
        """
        NameArray = ["time", "x", "y", "z", "gforce"]
        if(w == -2):
            self.myinterface.mytimeplot.close()
        else:

            self.myinterface.mytimeplot.close()
            self.myinterface.mytimeplot = view.time_plot()
            length =len(self.model.data.transformations[w][1])
            if(self.model.data.transformations[w][0].type == "RangeSelection"):
                length = self.model.data.transformations[w][0].last - self.model.data.transformations[w][0].first
            x = [None]*length
            for i in range(0, len(x)):
                x[i] = float(self.model.data.transformations[w][1].loc[:, NameArray[0]][i].replace(',', '.'))
            for n in range(1,len(NameArray)-1):
                y = [None]*length
                for i in range(0, len(y)):
                    y[i] = float(self.model.data.transformations[w][1].loc[:, NameArray[n]][i].replace(',', '.'))
                curve = QwtPlotCurve(NameArray[n])
                curve.setData(x, y)
                curve.attach(self.myinterface.mytimeplot)

            self.myinterface.show_of_time_plot()

    def value_changed(self):
        self.update_pipeline()

    def update_pipeline(self):
        isNull = True
        plotIndex = 0
        for x in range(0,len(self.model.data.transformations[0])):
            f= len(self.model.data.transformations[0]) - self.myinterface.mainWindow.widget.pipelineSlider.value()
            if(x < f):
                t = self.myinterface.mainWindow.layout.itemAt(x).widget().setEnabled(True)
                isNull = False
                plotIndex = x
            else:
                t = self.myinterface.mainWindow.layout.itemAt(x).widget().setEnabled(False)
        if(isNull):
            self.show_of_time_graphic(-2)
        else:
            self.show_of_time_graphic(plotIndex)

    def show_of_pipeline(self):
        for x in range(0,len(self.model.data.transformations)):
            pipelineEntry = QLabel()
            pipelineEntry.setFixedSize(100, 20)
            pipelineEntry.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            pipelineEntry.setText(self.model.data.transformations[x][0].type)  
            pipelineEntry.setAlignment(Qt.AlignCenter)
            self.myinterface.mainWindow.layout.addWidget(pipelineEntry)
            self.myinterface.mainWindow.widget.pipelineSlider.setRange(0, x+1)
        self.myinterface.mainWindow.widget.pipelineSlider.setTickInterval(1)
        self.myinterface.mainWindow.layout1.addWidget(self.myinterface.mainWindow.widget.pipelineSlider)
        self.myinterface.mainWindow.layout1.addLayout(self.myinterface.mainWindow.layout)
        self.myinterface.show_of_pipeline()


    def modifyPipeline(self):
         self.model.data.currentIndex = self.myinterface.mainWindow.widget.pipelineSlider.value()








