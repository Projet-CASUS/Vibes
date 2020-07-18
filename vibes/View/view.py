import sys
import numpy as np

from qwt.qt.QtGui import (QApplication, QPen, QBrush, QFrame, QFont, QWidget,
                          QMainWindow, QToolButton, QIcon, QPixmap, QToolBar,
                          QHBoxLayout, QLabel, QPrinter, QPrintDialog,
                          QFontDatabase, QWindow)
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