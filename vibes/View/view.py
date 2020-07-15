import sys
import numpy as np

from qwt.qt.QtGui import (QApplication, QPen, QBrush, QFrame, QFont, QWidget,
                          QMainWindow, QToolButton, QIcon, QPixmap, QToolBar,
                          QHBoxLayout, QLabel, QPrinter, QPrintDialog,
                          QFontDatabase)
from qwt.qt.QtCore import QSize
from qwt.qt.QtCore import Qt
from qwt import (QwtPlot, QwtPlotMarker, QwtSymbol, QwtLegend, QwtPlotGrid,
                 QwtPlotCurve, QwtPlotItem, QwtLogScaleEngine, QwtText,
                 QwtPlotRenderer)
#TODO fenetre pipline browser
class GraphicalInterface(QMainWindow):
    def __init__(self,*args):
        """
        TODO Philippe Créer une fenêtre vide.
        """
        QMainWindow.__init__(self, *args)

