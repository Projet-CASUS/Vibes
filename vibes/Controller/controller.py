import vibes

import vibes.Model.model as models
import vibes.Model.filter_editing_model as filter_editing_model
import vibes.Model.filter_editor as filter_editor
import vibes.Controller.filter_editing_controller as filter_editing_controller
from vibes.Controller.Controller_Qt.controller_qt import controller_qt

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
        self.filter_editing_controller = filter_editing_controller.filter_editing_controller(data_file)
        if(view_type == "controller_qt"):
            self.controller_qt = controller_qt(self.model,self)
        self.filter_editing_controller.set_view_controller(self.controller_qt)
        self.filter_editing_controller.set_controller(self)

    def time_range_selections(self, first, last,index=-1):
        """
        :param first: -> la première sélection de donnée dans la structure
        :param last: -> la deuxième sélection de donnée dans la structure
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Range_selection, index, first, last,
                                                self.model.data.transformations[0])
        self.controller_qt.redefine_vue()

    def differential(self, data, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Differential, index, data)
        self.controller_qt.redefine_vue()


    def integral(self, data, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Integral, index, data)
        self.controller_qt.redefine_vue()


    def merging(self, data, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Merge, index, data)
        self.controller_qt.redefine_vue()


    def filter_fir(self, data, sample_rate, cut_off, cut_off2, type, num_taps, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Filter_Fir, index,
                                              sample_rate, cut_off, cut_off2,
                                              data, type, num_taps)
        self.controller_qt.redefine_vue()


    def filter(self, data, cut_off, cut_off2, attenuation, fourier, type, index=-1):
        """
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        :param index -> int > la position de la transformation dans le pipeline
        """
        self.model.data.insert_transformation(vibes.Controller.transform.Filter, index, data, fourier, cut_off, cut_off2, attenuation, type)
        data_out = self.model.data.transformations[-1]
        data_in = self.model.data.transformations[len(self.model.data.transformations)-2]
        self.filter_editing_model = filter_editing_model.filter_editing_model(data_in, data_out,cut_off, cut_off2, type)
        self.filter_editing_model.data.transformations[-1][0].set_data_for_graphic()
        self.controller_qt.show_dashboard_window()
        self.controller_qt.define_plot(self.filter_editing_model.data.transformations[-1][0].freq, self.filter_editing_model.data.transformations[-1][0].impulsion_db_positive,self.controller_qt.my_interface.bode_plot_window,"bode plot")
        self.filter_editing_controller.send_transformation(self.filter_editing_model)