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
    def __init__(self, data_file):
        """
        Init:
            reçois les argument sys.argv pour contruire un Qt application

        """
        self.app = QApplication(sys.argv)
        self.model = models.Model(data_file)
        self.my_interface = view.graphical_interface()
        self.my_interface.main_window.widget.pipeline_slider = QSlider()
        self.my_interface.main_window.widget.pipeline_index = len(self.model.data.transformations[0])
        self.my_interface.main_window.widget.pipeline_slider.valueChanged.connect(self.value_changed)

    def add_data(self, type, data_file):
        """
        todo Daniel
        instancier un objet de data dans le datavibes du model
        Note: is it useful if so we need to modify add_transformation to review the tuple
        :return: none
        """
        self.model.data.add_transformation(vibes.ImportFile, type, data_file)


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

    def define_freq_graphic(self, w=-1):

        name_array = ["time","gforce"]
        if(w == -2):
            self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot.close()
        else:
            self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot.close()
            self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot = view.qwt()
            length = len(self.model.data.transformations[w][1])
            if (self.model.data.transformations[w][0].type == "range_selection"):
                length = self.model.data.transformations[w][0].last - self.model.data.transformations[w][0].first
            x = [None] * length
            for i in range(0, len(x)):
                x[i] = float(self.model.data.transformations[w][1].loc[:, name_array[0]][i].replace(',', '.'))
            freq = self.my_interface.fourier_window.defineX(x, 200)
            for n in range(1, len(name_array)):
                y = [None] * length
                for i in range(0, len(y)):
                    y[i] = float(self.model.data.transformations[w][1].loc[:, name_array[n]][i].replace(',', '.'))
                fourier = self.my_interface.fourier_window.defineY(y, 200)
                curve = QwtPlotCurve(name_array[n])
                curve.setData(freq, fourier)
                curve.attach(self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot)
            self.my_interface.show_of_freq()

    def define_time_graphic(self, w = -1):
        """
        TODO Philippe
        afficher le graphique en temporelle du model
        :return:
        """
        NameArray = ["time", "x", "y", "z", "gforce"]
        if(w == -2):
            self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot.close()
        else:
            self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot.close()
            self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot = view.qwt()
            length =len(self.model.data.transformations[w][1])
            if(self.model.data.transformations[w][0].type == "range_selection"):
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
                curve.attach(self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot)

            self.my_interface.show_of_time()

    def value_changed(self):
        self.update_pipeline()

    def update_pipeline(self):
        isNull = True
        plotIndex = 0
        for x in range(0,len(self.model.data.transformations[0])):
            f= len(self.model.data.transformations[0]) - self.my_interface.main_window.widget.pipeline_slider.value()
            if(x < f):
                t = self.my_interface.main_window.layout.itemAt(x).widget().setEnabled(True)
                isNull = False
                plotIndex = x
            else:
                t = self.my_interface.main_window.layout.itemAt(x).widget().setEnabled(False)
        if(isNull):
            self.define_time_graphic(-2)
            self.define_freq_graphic(-2)
        else:
            self.define_time_graphic(plotIndex)
            self.define_freq_graphic(plotIndex)

    def show_of_pipeline(self):
        for x in range(0,len(self.model.data.transformations)):
            pipeline_entry = QLabel()
            pipeline_entry.setFixedSize(100, 20)
            pipeline_entry.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            pipeline_entry.setText(self.model.data.transformations[x][0].type)
            pipeline_entry.setAlignment(Qt.AlignCenter)
            self.my_interface.main_window.layout.addWidget(pipeline_entry)
            self.my_interface.main_window.widget.pipeline_slider.setRange(0, x + 1)
        self.my_interface.main_window.widget.pipeline_slider.setTickInterval(1)
        self.my_interface.main_window.layout1.addWidget(self.my_interface.main_window.widget.pipeline_slider)
        self.my_interface.main_window.layout1.addLayout(self.my_interface.main_window.layout)
        self.my_interface.show_of_pipeline()


    def modifyPipeline(self):
         self.model.data.currentIndex = self.my_interface.main_window.widget.pipeline_slider.value()








