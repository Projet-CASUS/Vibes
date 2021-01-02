import sys

from PyQt5.Qt import (QWidget, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QSlider, QApplication, QPushButton, QLineEdit
import pyqtgraph as pg

import numpy as np

from qwt import (QwtPlot, QwtPlotCurve, QwtText)
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
        self.filter_window = Filters()

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

    def show_filter_window(self):
        self.filter_window.show()

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
        self.layoutDashBoard = QVBoxLayout()
        self.layoutAction = QHBoxLayout()
        self.layoutText = QHBoxLayout()
        self.widget = pipeline_content()

    def define_pipeline_browser(self,model):
        """
        La fonction defini quel transformation son dans le pipeline
        :param model: -> Model > Reference du model de l'application
        """

        for x in range(len(model.data.transformations)-1, len(model.data.transformations)):
            pipeline_entry = QLabel()
            pipeline_entry.setFixedSize(100, 20)
            pipeline_entry.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            pipeline_entry.setText(model.data.transformations[x][0].type)
            pipeline_entry.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(pipeline_entry)

        self.widget.pipeline_slider.setRange(0, len(model.data.transformations))
        self.widget.pipeline_slider.setTickInterval(1)
        self.widget.pipeline_slider.setValue(0)
        self.layoutAction.addWidget(self.widget.exportWav)
        self.layoutAction.addWidget(self.widget.differentiel)
        self.layoutAction.addWidget(self.widget.merger)
        self.layoutAction.addWidget(self.widget.rangeSelection)
        self.layoutAction.addWidget(self.widget.FirPasseBas)
        self.layoutAction.addWidget(self.widget.FirPasseHaut)
        self.layoutAction.addWidget(self.widget.FirPasseBande)
        self.layoutAction.addWidget(self.widget.PasseBas)
        self.layoutAction.addWidget(self.widget.PasseHaut)
        self.layoutAction.addWidget(self.widget.PasseBande)
        self.layout1.addWidget(self.widget.pipeline_slider)

        self.layoutText.addWidget(self.widget.firstLabel)
        self.layoutText.addWidget(self.widget.first)
        self.layoutText.addWidget(self.widget.lastLabel)
        self.layoutText.addWidget(self.widget.last)
        self.layoutText.addWidget(self.widget.cut_off_label)
        self.layoutText.addWidget(self.widget.cut_off)
        self.layoutText.addWidget(self.widget.cut_off_label2)
        self.layoutText.addWidget(self.widget.cut_off2)
        self.layoutText.addWidget(self.widget.attenuation_label)
        self.layoutText.addWidget(self.widget.attenuation)

        self.layoutDashBoard.addLayout(self.layoutAction)
        self.layoutDashBoard.addLayout(self.layoutText)

        self.layout1.addLayout(self.layout)
        self.layout1.addLayout(self.layoutDashBoard)

class pipeline_content(QWidget):
    """
    Defini les outils Qt utiliser dans la pipeline
    """
    def __init__(self):
        super(pipeline_content, self).__init__()
        self.pipeline_index = None
        self.pipeline_slider =  QSlider()
        self.differentiel = QPushButton("Differentiel")
        self.merger = QPushButton("Merger")
        self.rangeSelection = QPushButton("Range Selection")
        self.firstLabel = QLabel("First:")
        self.first = QLineEdit()
        self.lastLabel = QLabel("Last:")
        self.last = QLineEdit()
        self.cut_off_label = QLabel("cut_off(1):")
        self.cut_off_label2 = QLabel("cut_off(2):")
        self.attenuation_label = QLabel("Attenuation:")
        self.cut_off = QLineEdit()
        self.cut_off2 = QLineEdit()
        self.attenuation = QLineEdit()
        self.exportWav = QPushButton("Export Wav")
        self.FirPasseBas = QPushButton("FIR Passe Bas")
        self.FirPasseHaut = QPushButton("FIR Passe Haut")
        self.FirPasseBande = QPushButton("FIR Passe Bande")
        self.PasseBas = QPushButton("Passe Bas")
        self.PasseHaut = QPushButton("Passe Haut")
        self.PasseBande = QPushButton("Passe Bande")

class Filters(QMainWindow):
   def __init__(self):
       super(Filters, self).__init__()

class plot_state():
    """
    Classe abstraite qui definit le minimum dans un état d'un graphique
   :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        self.qwtPlot = QwtPlot

    def set_curve(self,x,y,name):

        self.curve.setData(x, y)
        self.curve.attach(self.qwtPlot)

class time_state(plot_state):
    """
    sous cette état le graphique affiche une courbe en temporelle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(time_state, self).__init__(qwtPlot)
        self.name = "Time"
        self.curve = QwtPlotCurve(self.name)
        self.qwtPlot = QwtPlot(self.name)

class freq_state(plot_state):
    """
    sous cette etat la graphique affiche une courbe en frequentielle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(freq_state, self).__init__(qwtPlot)
        self.name = "frequency"
        self.curve = QwtPlotCurve(self.name)
        self.qwtPlot = QwtPlot(self.name)


class spectro_state(plot_state):
    """
    Pas encore utiliser devrait avoir besoin certaine redefinition lorsqu'on voudra l'utiliser
    """
    def __init__(self,qwtPlot):
        super(spectro_state, self).__init__(qwtPlot)
        self.name ="Spectro"
        self.qwtPlot = QwtPlot(self.name)

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


    def set_curve(self,x,y,name):
        """
        appelle la bonne definition pour definir la courbe selon l'etat
        """
        return self.state.set_curve(x,y,name)
