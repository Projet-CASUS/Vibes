import sys
import vibes.View.view as view
import vibes.Model.model as model
from qwt.qt.QtGui import (QApplication)
class Controller():
    def __init__(self):
        """
        Init:
            reçois les argument sys.argv pour contruire un Qt application

        """
        self.app = QApplication(sys.argv)
        self.view = view.GraphicalInterface()
        self.model = model.Model()

    def addData(self):
     """
     instancier un objet de data dans le datavibes du model
     :return: none
     """
        pass

    def addTransform(self):
    """
    ajouter une transformation dans l'objet datavibes du model
    """
        pass

    def dataRangeSelections(self):
         """
         fait une selection de donnée dans la section des données temporelles.
         update le view en mettant en evidence les limites
         ***definire comment modifier datavibes en conséquence***
         :param self:
         :return:
         """
        pass

    def popUpGrphic(self):
        """

        :param self:
        :return:
        """
        pass


