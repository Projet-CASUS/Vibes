import sys

from PyQt5.Qt import (QWidget, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QSlider, QApplication

from qwt import (QwtPlot, QwtPlotCurve)
from scipy import fftpack
from scipy import signal


def instanciate_qt_application():
    return QApplication(sys.argv)


class graphical_interface():
    """
    Contient des attributs qui contient le différente QWindow
    Contient les fonction d'affichage
    """
    def __init__(self):
        self.time_window = time_plot()
        self.fourier_window = fourier()
        self.pipeline_window = pipeline()

    def show_graphic(self,window):
        window.resize(600, 300)
        window.widget.wrapper_widget_qwt.qwtPlot.replot()
        window.widget.wrapper_widget_qwt.qwtPlot.show()

    def show_pipeline_browser(self):
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

class time_plot(QMainWindow):
    """
    Defini la QMainWindow du time_plot
    Contient le widget de type time_plot_content
    Contient un nom
    """
    def __init__(self,*args,**kwargs):
        super(time_plot, self).__init__(*args,**kwargs)
        self.widget = time_plot_content()
        self.setCentralWidget(self.widget)
        self.name = "Time"

class time_plot_content(QWidget):
    """

    """
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
        self.name = "Freq"

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

    def refresh_graphic(self,index):
        self.qwtPlot.close()
        if(index > -2):
            self.qwtPlot = qwt()
            return True
        return False;
      
    def set_curve(self,x,y,name):
        curve = QwtPlotCurve(name)
        curve.setData(x, y)
        curve.attach(self.qwtPlot)

class qwt(QwtPlot):
    def __init__(self):
        super(qwt, self).__init__()
