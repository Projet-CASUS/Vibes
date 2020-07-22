import sys
import numpy as np

from qwt.qt.QtGui import (QApplication, QPen, QBrush, QFrame, QFont, QWidget,
                          QMainWindow, QToolButton, QIcon, QPixmap, QToolBar,
                          QHBoxLayout, QLabel, QPrinter, QPrintDialog,
                          QFontDatabase, QWindow, QVBoxLayout)
from qwt.qt.QtCore import QSize
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
        self.mytimeplot = QwtPlot("Two curve")
        self.mainWindow = QMainWindow()
        self.pipelineWidget = pipeline_widget()
        self.mainWindow.setCentralWidget(self.pipelineWidget)
    def show_of_time_plot(self):
        self.mytimeplot.resize(600, 300)
        self.mytimeplot.replot()
        self.mytimeplot.show()

    def show_of_pipeline(self):
        self.mainWindow.show()

class pipeline_widget(QWidget):
    def __init__(self):
        super(pipeline_widget, self).__init__()
        self.layout = QVBoxLayout()
        self.pipelineEntry = QLabel()
