import sys

from PyQt5.Qt import (QWidget, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QSlider, QApplication
import pyqtgraph as pg

import numpy as np

from qwt import (QwtPlot, QwtPlotCurve)
from scipy import fftpack
from scipy import signal


def instanciate_qt_application():
    """
    Instanciation d'une QApplication
    """
    return QApplication(sys.argv)


class graphical_interface():
    """
    Contient des attributs qui contient le différente QWindow
    Contient les fonction d'affichage
    """

    def __init__(self):
        """
        Instantiation des 3 différentes types de fenêtres
        """
        self.time_window = wrapper_qwt(time_state(QwtPlot()))
        self.fourier_window = wrapper_qwt(freq_state(QwtPlot()))
        self.pipeline_window = pipeline()

    def show_graphic(self,window):
        """
        affichage d'un graphique
        """
        window.state.qwtPlot.resize(600, 300)
        window.state.qwtPlot.replot()
        window.state.qwtPlot.show()

    def show_pipeline_browser(self):
        """
        affichage du pipeline
        """
        self.pipeline_window.widget.setLayout(self.pipeline_window.layout1)
        self.pipeline_window.setCentralWidget(self.pipeline_window.widget)
        self.pipeline_window.show()


class pipeline(QMainWindow):
    """
    Le pipeline est un QMainWindow
    contient des layouts pour placer les objets dans sa fenetre
    contient un widget de type pipeline_content
    contieent une fonction qui definie le contenue dans le pipeline
    """
    def __init__(self,*args,**kwargs):
        super(pipeline, self).__init__(*args,**kwargs)
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.widget = pipeline_content()

    def define_pipeline_browser(self,model):
        """
        La fonction defini quel transformation son dans le pipeline
        :param model: -> Model > Reference du model de l'application
        """
        for x in range(0, len(model.data.transformations)):
            pipeline_entry = QLabel()
            pipeline_entry.setFixedSize(100, 20)
            pipeline_entry.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            pipeline_entry.setText(model.data.transformations[x][0].type)
            pipeline_entry.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(pipeline_entry)
        self.widget.pipeline_slider.setRange(0, len(model.data.transformations))
        self.widget.pipeline_slider.setTickInterval(1)
        self.layout1.addWidget(self.widget.pipeline_slider)
        self.layout1.addLayout(self.layout)


class pipeline_content(QWidget):
    """
    Defini les outils Qt utiliser dans la pipeline
    """
    def __init__(self):
        super(pipeline_content, self).__init__()
        self.pipeline_index = None
        self.pipeline_slider =  QSlider()

class operation_dashboard(QMainWindow):
   pass

class plot_state():
    """
    Classe abstraite qui definit le minimum dans un état d'un graphique
   :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        self.qwtPlot = qwtPlot
    def set_curve(self):
        pass

class time_state(plot_state):
    """
    sous cette état le graphique affiche une courbe en temporelle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(time_state, self).__init__(qwtPlot)
        self.qwtPlot = qwtPlot
    def set_curve(self,x,y,name):
        """
        definit la courbe avec des valeur en temporelle
        """
        curve = QwtPlotCurve(name)
        curve.setData(x, y)
        curve.attach(self.qwtPlot)

class freq_state(plot_state):
    """
    sous cette etat la graphique affiche une courbe en frequentielle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(freq_state, self).__init__(qwtPlot)
        self.qwtPlot = qwtPlot

    def set_curve(self,x,y,name):
        """
        :param x: -> numpy > Recois un numpy des valeurs en x
        :param y: -> numpy > recois un numpy des valeurs en y
        :param name -> string > recois une string du nom de la courbe
        definit la courbe avec des valeur en temporelle

        """
        sample_rate = 0
        while(sample_rate < len(x)  and x[sample_rate] <=1):
            sample_rate = sample_rate+1
        if(sample_rate >= len(x)):
            sample_rate =sample_rate-1
        if(x[sample_rate]<=1):
            sample_rate = sample_rate*1/x[sample_rate]
        curve = QwtPlotCurve(name)
        freq, count =self.defineX(x,sample_rate)
        fourier = self.defineY(y,count)
        curve.setData(freq,fourier)
        curve.attach(self.qwtPlot)

    def defineX(self, data, sample_rate):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
       Convertie les donnee temporelle en frequentielle

        """

        n = len(data)
        freq = fftpack.fftfreq(n) * sample_rate

        i = 0
        while(freq[i] >= 0):
            i= i+1
        freqreturn = [0]*i
        for x in range(0,i):
            freqreturn[x] = freq[x]
        return freqreturn,i

    def defineY(self, data, count):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
        Convertie les donnee temporelle en frequentielle
        """
        fourier = fftpack.fft(data)
        fourierreturn = [0]*count
        for x in range(0,count):
            fourierreturn[x] = fourier[x]
        return fourierreturn

class specto_state(plot_state):
    """
    Pas encore utiliser devrait avoir besoin certaine redefinition lorsqu'on voudra l'utiliser
    """
    def __init__(self,qwtPlot):
        super(specto_state, self).__init__(qwtPlot)
        self.qwtPlot = qwtPlot

    def set_curve(self,x,y,name):
        curve = QwtPlotCurve(name)
        curve.setData(self.define(x,200,1), self.define(y,200,1))
        curve.attach(self.qwtPlot)

    def define(self, values, sampling_freq):
        f, t, Sxx = signal.spectrogram(values, sampling_freq)
        return f, t, Sxx


class wrapper_qwt():
    """
    classe ajoutant des fonctionnalite a un qwtPlot
    """
    def __init__(self, state):
        super(wrapper_qwt, self).__init__()
        self.state = state

    def refresh_graphic(self,index):
        """
        TODO: il devrait avoir une meilleur maniere de proceder
        """
        self.state.qwtPlot.close()
        if(index > -2):
            self.state.qwtPlot = QwtPlot()
            return True
        return False;


    def set_curve(self,x,y,name):
        """
        appelle la bonne definition pour definir la courbe selon l'etat
        """
        self.state.set_curve(x,y,name)
