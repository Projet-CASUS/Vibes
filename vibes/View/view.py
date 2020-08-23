import sys
import numpy as np
import vibes.Model.model as models
from qwt.qt.QtGui import (QApplication, QPen, QBrush, QFrame, QFont, QWidget,
                          QMainWindow, QToolButton, QIcon, QPixmap, QToolBar,
                          QHBoxLayout, QLabel, QPrinter, QPrintDialog,
                          QFontDatabase, QWindow, QVBoxLayout, QRubberBand, QPalette, QSlider)
from qwt.qt.QtCore import QSize, QRect, QPoint
from qwt.qt.QtCore import Qt
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
        self.myfourierplot =fourier()
        self.mainWindow = pipeline()

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
        self.firstSelection = QwtPlotCurve("First Selection")
        self.lastSelection = QwtPlotCurve("Last Selection")

    def mouseReleaseEvent(self, event):
        self.rubberBand.show()

class fourier(QwtPlot):
    def __init__(self):
        super(fourier, self).__init__("Chuba_Hawk")
        self.origin = None
        self.rubberBand = None

    def define(self, data, key, sample_rate):
        fourier = fftpack.fft(data[key])
        freq = fftpack.fftfreq(len(data[key])) * sample_rate
        return fourier, freq

class spectrogram(QwtPlot):
    def __init__(self):
        super(spectrogram, self).__init__("Old_dirty_V")
        self.origin = None
        self.rubberBand = None

    def define(self, values, sampling_freq):
        f, t, Sxx = signal.spectrogram(values, sampling_freq)
        return f, t, Sxx

