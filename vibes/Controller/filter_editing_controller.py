import vibes

import vibes.Model.model as models
import vibes.Model.filter_editing_model as filter_editing_model
import vibes.Model.filter_editor as filter_editor


from vibes.Controller.Controller_Qt.controller_qt import controller_qt

class filter_editing_controller():
    """
    class qui permet d'ajouter les nouvelles transformation dans le pipeline en plus de trigger le controlleur d'affichage
    """
    def __init__(self, data_file):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.model = models.Model(data_file)

    def set_view_controller(self,controller):
        self.controller_qt = controller

    def set_controller(self,controller):
        self.controller = controller

    def modify_filter_response(self,first, last, attenuation,type, editor_type,window_type,name):
        self.controller.filter_editing_model.data.transformations[-1].set_type_plot(editor_type)
        self.controller.filter_editing_model.data.insert_transformation(filter_editor.filter_editor,-1)
        self.controller.filter_editing_model.data.transformations[-1].modify_response(first,last,attenuation,type)
        self.controller.filter_editing_model.data.transformations[-1].get_data_for_graphic()
        self.controller_qt.define_plot(self.controller.filter_editing_model.data.transformations[-1].get_plot_editor().freq,self.controller.filter_editing_model.data.transformations[-1].get_plot_editor().impulsion_db_positive,window_type,name)

    def make_plot(self, editor_type,window_type,name):
        self.controller.filter_editing_model.data.transformations[-1].set_type_plot(editor_type)
        self.controller.filter_editing_model.data.insert_transformation(filter_editor.filter_editor, -1)
        self.controller.filter_editing_model.data.transformations[-1].get_data_for_graphic()
        self.controller_qt.define_plot(self.controller.filter_editing_model.data.transformations[-1].get_plot_editor().freq,
                                       self.controller.filter_editing_model.data.transformations[-1].get_plot_editor().impulsion_db_positive, window_type, name)

    def redefine_filter_data(self,filter_editing):
        data_modified = self.model.data.transformations[-1]
        data_modified[0].freq = filter_editing.controller.filter_editing_model.data.transformations[-1][0].freq
        data_modified[0].freq_complete = filter_editing.controller.filter_editing_model.data.transformations[-1][0].freq_complete
        data_modified[0].fourier_no_complexe = filter_editing.controller.filter_editing_model.data.transformations[-1][0].vout
        data_modified[0].fourier_no_complexe_positive = filter_editing.controller.filter_editing_model.data.transformations[-1][0].vout_positive
        self.controller_qt.redefine_vue()

    def send_transformation(self,data):
        self.transformation = data