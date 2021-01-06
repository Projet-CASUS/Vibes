import sys

from PyQt5.Qt import (QWidget, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QSlider, QApplication, QPushButton, QLineEdit, QAction
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
        self.dashboard_window = dashboard()

    def show_graphic(self,window):
        """
        affichage d'un graphique
        """
        window.state.qwt_plot.resize(600, 300)
        window.state.qwt_plot.replot()
        window.state.qwt_plot.show()

    def show_pipeline_browser(self):
        """
        affichage du pipeline
        """
        self.pipeline_window.widget.setLayout(self.pipeline_window.layout1)
        self.pipeline_window.setCentralWidget(self.pipeline_window.widget)
        self.pipeline_window.show()

    def show_DashBoard_window(self):
        self.dashboard_window.widget.setLayout(self.dashboard_window.layout_text)
        self.dashboard_window.setCentralWidget(self.dashboard_window.widget)
        self.dashboard_window.show()

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

class dashboard(QMainWindow):
   def __init__(self):
       super(dashboard, self).__init__()

       self.layout_text = QHBoxLayout()

       self.widget = DashBoard_content()

       self.bar = self.menuBar()


       self.file = self.bar.addMenu("File")
       self.export_wav = QAction("export wav", self)
       self.file.addAction(self.export_wav)



       self.actions = self.bar.addMenu("Actions")

       self.differential = QAction("differential", self)
       self.range_selection = QAction("range selection", self)
       self.merge = QAction("merge", self)

       self.actions.addAction(self.differential)
       self.actions.addAction(self.range_selection)
       self.actions.addAction(self.merge)




       self.Filters = self.bar.addMenu("Filters")

       self.passe_bas = QAction("passe bas", self)
       self.passe_haut = QAction("passe haut", self)
       self.passe_bande = QAction("passe_bande", self)

       self.Filters.addAction(self.passe_bas)
       self.Filters.addAction(self.passe_haut)
       self.Filters.addAction(self.passe_bande)




       self.FIR = self.bar.addMenu("Filters FIR")

       self.passe_bas_fir = QAction("passe bas fir", self)
       self.passe_haut_fir = QAction("passe haut fir", self)
       self.passe_bande_fir = QAction("passe bande fir", self)

       self.FIR.addAction(self.passe_bas_fir)
       self.FIR.addAction(self.passe_haut_fir)
       self.FIR.addAction(self.passe_bande_fir)

   def define(self):
       self.layout_text.addWidget(self.widget.first_label)
       self.layout_text.addWidget(self.widget.first)
       self.layout_text.addWidget(self.widget.last_label)
       self.layout_text.addWidget(self.widget.last)
       self.layout_text.addWidget(self.widget.cut_off_label)
       self.layout_text.addWidget(self.widget.cut_off)
       self.layout_text.addWidget(self.widget.cut_off_label2)
       self.layout_text.addWidget(self.widget.cut_off2)
       self.layout_text.addWidget(self.widget.attenuation_label)
       self.layout_text.addWidget(self.widget.attenuation)


class DashBoard_content(QWidget):
    """
    Defini les outils Qt utiliser dans la pipeline
    """
    def __init__(self):
        super(DashBoard_content, self).__init__()

        self.first_label = QLabel("First:")
        self.first = QLineEdit()
        self.last_label = QLabel("Last:")
        self.last = QLineEdit()
        self.cut_off_label = QLabel("cut_off(1):")
        self.cut_off_label2 = QLabel("cut_off(2):")
        self.attenuation_label = QLabel("Attenuation:")
        self.cut_off = QLineEdit()
        self.cut_off2 = QLineEdit()
        self.attenuation = QLineEdit()

class plot_state(QMainWindow):
    """
    Classe abstraite qui definit le minimum dans un état d'un graphique
   :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(plot_state, self).__init__()
        self.qwt_plot = QwtPlot

    def set_curve(self,x,y,name):

        self.curve.setData(x, y)
        self.curve.attach(self.qwt_plot)

class time_state(plot_state):
    """
    sous cette état le graphique affiche une courbe en temporelle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(time_state, self).__init__(qwtPlot)
        self.name = "Time"
        self.curve = QwtPlotCurve(self.name)
        self.qwt_plot = QwtPlot(self.name)

class freq_state(plot_state):
    """
    sous cette etat la graphique affiche une courbe en frequentielle
    :param qwtPlot: -> qwtPlot > Recois un graphique
    """
    def __init__(self,qwtPlot):
        super(freq_state, self).__init__(qwtPlot)
        self.name = "frequency"
        self.curve = QwtPlotCurve(self.name)
        self.qwt_plot = QwtPlot(self.name)


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
