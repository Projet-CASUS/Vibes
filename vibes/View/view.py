import sys
import numpy as np
import vibes.Model.model as models
from PyQt5.Qt import (QApplication, QPen, QBrush, QFrame, QFont, QWidget,
                          QMainWindow, QToolButton, QIcon, QPixmap, QToolBar,
                          QHBoxLayout, QLabel, QPrinter, QPrintDialog,
                          QFontDatabase, QWindow, QVBoxLayout, QRubberBand, QPalette, QSlider)
from PyQt5.Qt import QSize, QRect, QPoint
from PyQt5.Qt import Qt
from qwt import (QwtPlot, QwtPlotMarker, QwtSymbol, QwtLegend, QwtPlotGrid,
                 QwtPlotCurve, QwtPlotItem, QwtLogScaleEngine, QwtText,
                 QwtPlotRenderer)
from scipy import fftpack
from scipy import signal


#TODO fenetre pipline browser



class graphical_interface():
    def __init__(self):
        """
        TODO Philippe Créer une fenêtre vide.
        """
        self.mytimeplot = time_plot()
        self.myfourierplot = fourier()
        self.mainWindow = pipeline()

    def show_of_freq_plot(self):
        self.myfourierplot.resize(600,300)
        self.myfourierplot.replot()
        self.myfourierplot.show()

    def show_of_time_plot(self):
        self.mytimeplot.resize(600, 300)
        self.mytimeplot.replot()
        self.mytimeplot.show()

    def show_of_pipeline(self):
        self.mainWindow.widget.setLayout(self.mainWindow.layout1)
        self.mainWindow.setCentralWidget(self.mainWindow.widget)
        self.mainWindow.show()


class pipeline(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(pipeline, self).__init__(*args,**kwargs)
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.widget = pipeline_widget()

class pipeline_widget(QWidget):
    def __init__(self):
        super(pipeline_widget,self).__init__()
        self.pipelineIndex = None
        self.pipelineSlider = None

class time_plot(QwtPlot):
    def __init__(self):
        super(time_plot, self).__init__()


class fourier(QwtPlot):
    def __init__(self):
        super(fourier, self).__init__("Chuba_Hawk")
        self.origin = None
        self.rubberBand = None

    def defineX(self,data,sample_rate):
        freq = fftpack.fftfreq(len(data)) * sample_rate
        return freq

    def defineY(self, data, sample_rate):
        fourier = fftpack.fft(data)
        return fourier

class spectrogram(QwtPlot):
    def __init__(self):
        super(spectrogram, self).__init__("Old_dirty_V")
        self.origin = None
        self.rubberBand = None

    def define(self, values, sampling_freq):
        f, t, Sxx = signal.spectrogram(values, sampling_freq)
        return f, t, Sxx

