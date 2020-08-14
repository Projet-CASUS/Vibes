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
#TODO fenetre pipline browser
class graphical_interface():
    def __init__(self):
        """
        TODO Philippe Créer une fenêtre vide.
        """
        self.mytimeplot = time_plot()
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

