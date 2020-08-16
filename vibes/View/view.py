import sys
import numpy as np

from qwt.qt.QtGui import (QApplication, QPen, QBrush, QFrame, QFont, QWidget,
                          QMainWindow, QToolButton, QIcon, QPixmap, QToolBar,
                          QHBoxLayout, QLabel, QPrinter, QPrintDialog,
                          QFontDatabase, QWindow, QVBoxLayout, QRubberBand, QPalette)
from qwt.qt.QtCore import QSize, QRect
from qwt.qt.QtCore import Qt
from qwt import (QwtPlot, QwtPlotMarker, QwtSymbol, QwtLegend, QwtPlotGrid,
                 QwtPlotCurve, QwtPlotItem, QwtLogScaleEngine, QwtText,
                 QwtPlotRenderer)
from scipy import fftpack
from scipy import signal
from scipy.fft import fftshift

#TODO fenetre pipline browser



class graphical_interface():
    def __init__(self):
        """
        TODO Philippe Créer une fenêtre vide.
        """
        self.mytimeplot = time_plot()
        self.mainWindow = QMainWindow()
        self.pipelineWidget = pipeline_widget()
        self.mainWindow.setCentralWidget(self.pipelineWidget)
    def show_of_time_plot(self):
        self.mytimeplot.resize(600, 300)
        self.mytimeplot.replot()
        self.mytimeplot.show()

    def show_of_pipeline(self):
        self.mainWindow.setLayout(self.pipelineWidget.layout)
        self.mainWindow.show()


class pipeline_widget(QWidget):
    def __init__(self):
        super(pipeline_widget, self).__init__()
        self.layout = QVBoxLayout()
        self.pipelineEntry = QLabel()


class QBrush(object):
    pass


class time_plot(QwtPlot):
    def __init__(self):
        super(time_plot, self).__init__("Two curve")
        self.origin = None
        self.rubberBand = None
    def mousePressEvent(self, event):
        origin = event.pos()
        if not self.rubberBand:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
            palette = QPalette()
            palette.setBrush()
            self.rubberBand.setPalette(palette)
        self.rubberBand.setGeometry(QRect(origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

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
