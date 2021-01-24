import vibes.Controller.Controller_Qt.Event.Events as events
import vibes.Controller.Controller_Qt.Event.filter_events as filter_events
import vibes.View.qt_view as view
from vibes.Controller.controller_view import controller_view


class controller_qt(controller_view):
    """
    Control l'orchestration ainsi que les appelles de fonction de la vue nécessaires pour que celle-ci soit mis à jours
    """
    def __init__(self,model,controller):
        """
        :param model: -> pipeline > le pipeline du controlleur
        :param interface -> graphical_interface > l'interface graphique du controlleur
        :param controller -> controller > l'objet controller
        """
        self.model = model
        self.my_interface = view.graphical_interface()
        self.my_interface.dashboard_window.define()
        self.show_dashboard_window()
        self.events = events.events(controller, self.my_interface)
        self.filter_events = filter_events.filter_events(controller, self.my_interface)
        self.define_connects(model)
        self.redefine_vue()


    def intialisation(self, model, data_index):
        """
        sert à initialiser les dernières informations nécessaires pour la vue
        :param model: -> pipeline > le pipeline du controlleur
        :param data_index: -> int > position de la transformation dans le pipeline
        """
        self.length = len(model.data.transformations[data_index][1])
        self.columns_name = model.data.transformations[data_index][0].names
        self.dataX = self.define_x_data(model,data_index)
        self.dataY = self.define_y_data(model,data_index)
        self.freq = model.data.transformations[data_index][0].freq
        self.fourier_no_complexe = model.data.transformations[data_index][0].fourier_no_complexe

    def define_connects(self,model):
        """
        :param model: -> pipeline > le pipeline du controlleur
        Définie toute les connection entre les objets qt et les événements
        """
        self.my_interface.pipeline_window.widget.pipeline_index = len(model.data.transformations[0])
        self.my_interface.pipeline_window.widget.pipeline_slider.valueChanged.connect(self.update_pipeline)

        self.my_interface.dashboard_window.export_wav.triggered.connect(self.events.export_event)

        self.my_interface.dashboard_window.differential.triggered.connect(self.events.differentiel_event)
        self.my_interface.dashboard_window.range_selection.triggered.connect(self.events.range_selection_event)
        self.my_interface.dashboard_window.merge.triggered.connect(self.events.merge_event)
        self.my_interface.dashboard_window.passe_bas_fir.triggered.connect(self.filter_events.fir_passe_bas_event)
        self.my_interface.dashboard_window.passe_haut_fir.triggered.connect(self.filter_events.fir_passe_haut_event)
        self.my_interface.dashboard_window.passe_bande_fir.triggered.connect(self.filter_events.fir_passe_bande_event)
        self.my_interface.dashboard_window.passe_bas.triggered.connect(self.filter_events.passe_bas_event)
        self.my_interface.dashboard_window.passe_haut.triggered.connect(self.filter_events.passe_haut_event)
        self.my_interface.dashboard_window.passe_bande.triggered.connect(self.filter_events.passe_bande_event)

    def define_x_data(self,model,data_index = -1):
        """
        :param model: -> pipeline > le pipeline du controlleur
        :param data_index: -> int > position de la transformation dans le pipeline
        :return: -> x
        sert à définir les données en x temporelle
        """
        x = self.define_numpy(self.length, model.data.transformations[data_index][1], 0)
        return x

    def define_y_data(self,model,data_index = -1):
        """
        :param model: -> pipeline > le pipeline du controlleur
        :param data_index: -> int > position de la transformation dans le pipeline
        :return: -> y
        sert à définir les données en y temporelle
        """

        for n in range(1, len(self.columns_name)):
            y = self.define_numpy(self.length, model.data.transformations[data_index][1], n)
        return y

    def redefine_vue(self, data_index=-1):
        """
        Cette fonction orchestre toute les changement nécessaire pour mettre à jours la vue
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        self.intialisation(self.model,data_index)
        self.redefine_graphic_time(self.my_interface.time_window)
        self.redefine_graphic_freq(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def redefine_graphic_time(self, window):
        """
        :param window: -> QWindow > la fenêtre que l'on veut modifier
        redéfinir le graphique du temps
        """
        for i in range(len(self.columns_name)):
            window.set_curve(self.dataX, self.dataY, self.columns_name[i])
            self.my_interface.show_graphic(window)

    def redefine_graphic_freq(self,window ):
        """
        :param window: -> QWindow > la fenêtre que l'on veut modifier
        redéfinir le graphique de la fréquence
        """
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
         les donnees a l aide de la fonction redefine_graphic_time() et redefine_graphic_freq()
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
            self.intialisation(self.model, -2)
            self.redefine_graphic_time(self.my_interface.time_window)
            self.redefine_graphic_freq(self.my_interface.fourier_window)
        else:
            self.intialisation(self.model, plot_index)
            self.redefine_graphic_time(self.my_interface.time_window)
            self.redefine_graphic_freq(self.my_interface.fourier_window)


    def define_numpy(self, length, data_structure, column):
        """
        :param length: -> int > la quantite de donnees contenue dans le panda pour un parametre
        :param data_structure -> la structure de données que l'on transforme en numpy
        :param column: -> string > nom exacte du parametre de la colonne a transformer en numpy
        :return:-> numpy
        """
        numpy = [None] * length
        for i in range(0, len(numpy)):
            numpy[i] = data_structure[i][column]
        return numpy

    def show_dashboard_window(self):
        """
        permet d'afficher le dashboard
        """
        self.my_interface.show_dashboard_window()
