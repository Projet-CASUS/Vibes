from PyQt5.Qt import (QWidget, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout)

from qwt import (QwtPlot)
from scipy import fftpack
from scipy import signal

class graphical_interface():
    def __init__(self):

        self.time_window = time_plot()
        self.fourier_window = fourier()
        self.main_window = pipeline()

    def show_of_freq(self):
        self.fourier_window.resize(600, 300)
        self.fourier_window.widget.wrapper_widget_qwt.qwtPlot.replot()
        self.fourier_window.widget.wrapper_widget_qwt.qwtPlot.show()

    def show_of_time(self):
        self.time_window.resize(600, 300)
        self.time_window.widget.wrapper_widget_qwt.qwtPlot.replot()
        self.time_window.widget.wrapper_widget_qwt.qwtPlot.show()

    def show_of_pipeline(self):
        self.main_window.widget.setLayout(self.main_window.layout1)
        self.main_window.setCentralWidget(self.main_window.widget)
        self.main_window.show()


class pipeline(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(pipeline, self).__init__(*args,**kwargs)
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.widget = pipeline_content()

class pipeline_content(QWidget):
    def __init__(self):
        super(pipeline_content, self).__init__()
        self.pipelineIndex = None
        self.pipelineSlider = None

class time_plot(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(time_plot, self).__init__(*args,**kwargs)
        self.widget = time_plot_content()
        self.setCentralWidget(self.widget)

class time_plot_content(QWidget):
    def __init__(self):
        super(time_plot_content, self).__init__()
        self.wrapper_widget_qwt = wrapper_qwt()
        self.layoutV = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        self.FirstTime = QLabel("First Time")
        self.LastTime = QLabel("Last Time")
        self.layoutH.addWidget(self.FirstTime)
        self.layoutH.addWidget(self.LastTime)
        self.layoutV.addWidget(self.wrapper_widget_qwt)
        self.layoutV.addLayout(self.layoutH)
        self.setLayout(self.layoutV)



class fourier(QMainWindow):
    def __init__(self):
        super(fourier, self).__init__()
        self.widget = fourier_content()
        self.setCentralWidget(self.widget)

    def defineX(self,data,sample_rate):
        freq = fftpack.fftfreq(len(data)) * sample_rate
        return freq

    def defineY(self, data, sample_rate):
        fourier = fftpack.fft(data)
        return fourier

class fourier_content(QWidget):
    def __init__(self):
        super(fourier_content, self).__init__()
        self.wrapper_widget_qwt = wrapper_qwt()
        self.layoutV = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        self.FirstTime = QLabel("First Time")
        self.LastTime = QLabel("Last Time")
        self.layoutH.addWidget(self.FirstTime)
        self.layoutH.addWidget(self.LastTime)
        self.layoutV.addWidget(self.wrapper_widget_qwt)
        self.layoutV.addLayout(self.layoutH)
        self.setLayout(self.layoutV)

class spectrogram(QMainWindow):
    def __init__(self):
        super(spectrogram, self).__init__()
        self.widget = spectrogram_content()
        self.setCentralWidget(self.widget)

    def define(self, values, sampling_freq):
        f, t, Sxx = signal.spectrogram(values, sampling_freq)
        return f, t, Sxx

class spectrogram_content(QWidget):
    def __init__(self):
        super(spectrogram_content, self).__init__()
        self.wrapper_widget_qwt = wrapper_qwt()
        self.layoutV = QVBoxLayout()
        self.layoutH = QHBoxLayout()
        self.FirstTime = QLabel("First Time")
        self.LastTime = QLabel("Last Time")
        self.layoutH.addWidget(self.FirstTime)
        self.layoutH.addWidget(self.LastTime)
        self.layoutV.addWidget(self.wrapper_widget_qwt)
        self.layoutV.addLayout(self.layoutH)
        self.setLayout(self.layoutV)


class wrapper_qwt(QWidget):
    def __init__(self):
        super(wrapper_qwt, self).__init__()
        self.qwtPlot = QwtPlot()

class qwt(QwtPlot):
    def __init__(self):
        super(qwt, self).__init__()
