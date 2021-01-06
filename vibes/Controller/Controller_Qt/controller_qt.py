import vibes.Controller.Controller_Qt.Event.Events as events
import vibes.Controller.Controller_Qt.Event.filter_events as filter_events

from Vibes.vibes.Controller.controller_view import controller_view


class controller_qt(controller_view):
    def __init__(self,model,interface,controller,data_index = -1):

        self.model = model
        self.my_interface = interface
        self.my_interface.DashBoard_window.define()
        self.show_DashBoard_window()
        self.events = events.events(controller)
        self.filter_events = filter_events.filter_events(controller)
        self.define_connects(model)
        self.redefine_graphic()


    def intialisation(self, model, data_index):
        self.length = len(model.data.transformations[data_index][1])
        self.columns_name = model.data.transformations[data_index][0].names
        self.dataX = self.define_x_data(model)
        self.dataY = self.define_y_data(model)
        self.freq = model.data.transformations[data_index][0].freq
        self.fourier_no_complexe = model.data.transformations[data_index][0].fourier_no_complexe

    def define_connects(self,model):
        self.my_interface.pipeline_window.widget.pipeline_index = len(model.data.transformations[0])
        self.my_interface.pipeline_window.widget.pipeline_slider.valueChanged.connect(self.update_pipeline)

        self.my_interface.DashBoard_window.export_wav.triggered.connect(self.events.export_event)

        self.my_interface.DashBoard_window.differential.triggered.connect(self.events.differentiel_event)
        self.my_interface.DashBoard_window.range_selection.triggered.connect(self.events.range_selection_event)
        self.my_interface.DashBoard_window.merge.triggered.connect(self.events.merge_event)
        self.my_interface.DashBoard_window.passe_bas_fir.triggered.connect(self.filter_events.fir_passe_bas_event)
        self.my_interface.DashBoard_window.passe_haut_fir.triggered.connect(self.filter_events.fir_passe_haut_event)
        self.my_interface.DashBoard_window.passe_bande_fir.triggered.connect(self.filter_events.fir_passe_bande_event)
        self.my_interface.DashBoard_window.passe_bas.triggered.connect(self.filter_events.passe_bas_event)
        self.my_interface.DashBoard_window.passe_haut.triggered.connect(self.filter_events.passe_haut_event)
        self.my_interface.DashBoard_window.passe_bande.triggered.connect(self.filter_events.passe_bande_event)

    def define_x_data(self,model,data_index = -1):
        x = self.define_numpy(self.length, model.data.transformations[data_index][1], 0, data_index)
        return x

    def define_y_data(self,model,data_index = -1):
        for n in range(1, len(self.columns_name)):
            y = self.define_numpy(self.length, model.data.transformations[data_index][1], n, data_index)
        return y

    def redefine_graphic(self, data_index=-1):
        """
        Cette fonction redefinit les valeurs a afficher sur un graphique
        :param window: -> QWindow > Une QWindow d'un graphique ex: temps frequence
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        self.intialisation(self.model,data_index)
        self.redefine_graphic_time(self.my_interface.time_window)
        self.redefine_graphic_freq(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def redefine_graphic_time(self, window):
        for i in range(len(self.columns_name)):
            window.set_curve(self.dataX, self.dataY, self.columns_name[i])
            self.my_interface.show_graphic(window)

    def redefine_graphic_freq(self,window ):
        for i in range(len(self.columns_name)):
            window.set_curve(self.freq,self.fourier_no_complexe,self.columns_name[i])
        self.my_interface.show_graphic(window)


    def define_pipeline_browser(self):
        """
        fonction du controlleur qui appelle les fonctions de la vue pour loader le pipeline
        """
        self.my_interface.pipeline_window.define_pipeline_browser(self.model)
        self.my_interface.show_pipeline_browser()

    def update_pipeline(self):
        """
         Cette fonction remet a jour le pipeline browser en fonction de l endroit ou le slider s arrete
         Il recalcule ensuite les transformations successives faites sur
         les donnees a l aide de la fonction redefine_graphic()
         """
        is_null = True
        plot_index = 0
        f = len(self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value()
        for x in range(0, len(self.model.data.transformations)):
            if x < f:
                self.my_interface.pipeline_window.layout.itemAt(x).widget().setEnabled(True)
                is_null = False
                plot_index = x
            else:
                self.my_interface.pipeline_window.layout.itemAt(x).widget().setEnabled(False)
        if is_null:
            self.redefine_graphic(self.my_interface.time_window, -2)
            self.redefine_graphic(self.my_interface.fourier_window, -2)
        else:
            self.redefine_graphic(self.my_interface.time_window, plot_index)
            self.redefine_graphic(self.my_interface.fourier_window, plot_index)


    def define_numpy(self, length, datastructure, column, index=-1):
        """
        :param length: -> int > la quantite de donnees contenue dans le panda pour un parametre
        :param index: -> int > a -1 par defaut
        :param name: -> string > nom exacte du parametre de la colonne a transformer en numpy
        """
        numpy = [None] * length
        for i in range(0, len(numpy)):
            numpy[i] = datastructure[i][column]
        return numpy

    def show_DashBoard_window(self):
        self.my_interface.show_DashBoard_window()
