import vibes
import vibes.View.qt_view as view
import vibes.Model.model as models

from Vibes.vibes.Controller.Controller_Qt.controller_qt import controller_qt


class Controller():
    """
    class qui permet d'ajouter les nouvelles transformation dans le pipeline en plus de trigger le controlleur d'affichage
    """
    def __init__(self, data_file,view_type):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.model = models.Model(data_file)
        self.my_interface = view.graphical_interface()
        if(view_type == "controller_qt"):
            self.controller_qt = controller_qt(self.model,self.my_interface,self)

    def time_range_selections(self, first, last,index=-1):
        """
        :param first: -> la première sélection de donnée dans la structure
        :param last: -> la deuxième sélection de donnée dans la structure
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Range_selection, index, first, last,
                                              self.model.data.transformations[0])
        self.controller_qt.redefine_graphic()

    def differential(self, data, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Differential, index, data)
        self.controller_qt.redefine_graphic()


    def integral(self, data, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Integral, index, data)
        self.controller_qt.redefine_graphic()


    def Merging(self, data, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Merge, index, data)
        self.controller_qt.redefine_graphic()


    def filter_fir(self, data, sample_rate, cut_off, cut_off2, type, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Filter_Fir, index, sample_rate, cut_off, cut_off2,
                                              data, type)
        self.controller_qt.redefine_graphic()


    def filter2(self, data, cut_off, cut_off2, attenuation, fourier, type, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Filter, index, data, fourier, cut_off, cut_off2, attenuation, type)
        self.controller_qt.redefine_graphic()


