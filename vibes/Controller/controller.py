import vibes

import vibes.Model.model as models
import vibes.Model.filter_editor as filter_editor

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

        if(view_type == "controller_qt"):
            self.controller_qt = controller_qt(self.model,self)

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
        self.model.data.insert_transformation(vibes.Controller.transform.Filter_Fir, index, sample_rate, cut_off, cut_off2,
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
        self.filter_model = filter_editor.filter_editer(data_in,data_out)
        self.filter_model.get_data_for_graphic()
        self.controller_qt.define_bode_plot(self.filter_model.freq, self.filter_model.impulsion_db_positive)



    def modify_filter_response(self,first, last, attenuation,type):
        self.filter_model.modify_response(first,last,attenuation,type)
        self.filter_model.get_data_for_graphic()
        self.controller_qt.define_bode_plot(self.filter_model.freq,self.filter_model.impulsion_db_positive)

    def redefine_filter_data(self,filter_editing):
        data_modified = self.model.data.transformations[-1]
        data_modified[0].freq = filter_editing.freq
        data_modified[0].freq_complete = filter_editing.freq_complete
        data_modified[0].fourier_no_complexe = filter_editing.vout
        data_modified[0].fourier_no_complexe_positive = filter_editing.vout_positive
        self.controller_qt.redefine_vue()


