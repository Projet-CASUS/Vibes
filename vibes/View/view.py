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

class graphical_interface():
    def __init__(self):

        self.mytimeplot = time_plot()
        self.myfourierplot = fourier()
        self.mainWindow = pipeline()

    def show_of_freq_plot(self):
        self.myfourierplot.resize(600,300)
        self.myfourierplot.replot()
        self.myfourierplot.show()

    def show_of_time_plot(self):
        self.mytimeplot.resize(600, 300)
        self.mytimeplot.widget.widgetWrapperForQWTplot.qwtPlot.replot()
        self.mytimeplot.widget.widgetWrapperForQWTplot.qwtPlot.show()

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

class time_plot(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(time_plot, self).__init__(*args,**kwargs)
        self.widget = widget_time_plot()
        self.setCentralWidget(self.widget)

class widget_time_plot(QWidget):
    def __init__(self):
        super(widget_time_plot, self).__init__()
        self.widgetWrapperForQWTplot = wrapper_qwt_time_plot()
        self.layoutV = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        self.FirstTime = QLabel("First Time")
        self.LastTime = QLabel("Last Time")
        self.layoutH.addWidget(self.FirstTime)
        self.layoutH.addWidget(self.LastTime)
        self.layoutV.addWidget(self.widgetWrapperForQWTplot)
        self.layoutV.addLayout(self.layoutH)
        self.setLayout(self.layoutV)

class wrapper_qwt_time_plot(QWidget):
    def __init__(self):
        super(wrapper_qwt_time_plot, self).__init__()
        self.qwtPlot = qwt_time_plot()

class qwt_time_plot(QwtPlot):
    def __init__(self):
        super(qwt_time_plot, self).__init__()

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

