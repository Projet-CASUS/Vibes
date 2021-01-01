import sys
import vibes
import vibes.View.qt_view as view
import vibes.Model.model as models
import vibes.Controller.Event.events as events
import vibes.Controller.Event.filter_events as filter_events
from scipy import fftpack

from Vibes.vibes.Controller.Event import events


class Controller():
    def __init__(self, data_file):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.model = models.Model(data_file)
        self.my_interface = view.graphical_interface()
        self.events = events.events(self)
        self.filter_events = filter_events.filter_events(self)
        self.x = []
        self.y = []
        ### todo DECOUPLER DU CONTROLLER
        ## Ne peut pas être découpler puisque connect dois être fais dans le controlleur sinon on créer plein de fonction inutile
        self.my_interface.pipeline_window.widget.pipeline_index = len(self.model.data.transformations[0])
        self.my_interface.pipeline_window.widget.pipeline_slider.valueChanged.connect(self.update_pipeline)
        self.my_interface.pipeline_window.widget.differentiel.clicked.connect(self.events.differentiel_event)
        self.my_interface.pipeline_window.widget.rangeSelection.clicked.connect(self.events.rangeSelection_event)
        self.my_interface.pipeline_window.widget.merger.clicked.connect(self.events.merger_event)
        self.my_interface.pipeline_window.widget.exportWav.clicked.connect(self.events.exporter_event)
        self.my_interface.pipeline_window.widget.FirPasseBas.clicked.connect(self.filter_events.fir_passe_bas_event)
        self.my_interface.pipeline_window.widget.FirPasseHaut.clicked.connect(self.filter_events.fir_passe_haut_event)
        self.my_interface.pipeline_window.widget.FirPasseBande.clicked.connect(self.filter_events.fir_passe_bande_event)
        self.my_interface.pipeline_window.widget.PasseBas.clicked.connect(self.filter_events.passe_bas_event)
        self.my_interface.pipeline_window.widget.PasseHaut.clicked.connect(self.filter_events.passe_haut_event)
        self.my_interface.pipeline_window.widget.PasseBande.clicked.connect(self.filter_events.passe_bande_event)
        ### DECOUPLER DU CONTROLLER

        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()
        self.show_Filter_Window()

    def time_range_selections(self, first, last, index=-1):
        """
        fait une selection de donnée dans la section des données temporelles.
        update le view en mettant en evidence les limites
        ***definire comment modifier Model.data en conséquence***
        :param first: -> int > Temps du debut de la fourchette de temps
        :param last: -> int > Temps de fin de la fourchette de temps selectionne
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Range_selection, index, first, last,
                                              self.model.data.transformations[0])
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def differential(self, data, index=-1):
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Differential, index, data)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def integral(self, data, index=-1):
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Integral, index, data)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def Merging(self, data, index=-1):
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Merge, index, data)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def filter(self, data, cut_off, cut_off2, type, index=-1):
        if (data[1][-1][0] <= 1):
            sample_rate = len(data[1]) * 1 / data[1][-1][0]
        else:
            sample_rate = len(data[1]) / data[1][-1][0]
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Filter, index, sample_rate, cut_off, cut_off2,
                                              data, type)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def filter2(self, data, cut_off, cut_off2, attenuation, fourier, type, index=-1):

        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Filter2, index, data, fourier, cut_off,
                                              cut_off2, attenuation, type)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def redefine_graphic(self, window, data_index=-1):
        """
        Cette fonction redefinit les valeurs a afficher sur un graphique
        :param window: -> QWindow > Une QWindow d'un graphique ex: temps frequence
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        if(window.state.name == "Time"):
            self.x,self.y = self.redefine_graphic_time(window,data_index)
        else:
            self.redefine_graphic_freq(self.x,self.y,window,data_index)

    def redefine_graphic_time(self, window, data_index=-1):
        columns_name = self.model.data.transformations[data_index][0].names
        if (window.refresh_graphic(data_index)):
            length = len(self.model.data.transformations[data_index][1])
            x = self.define_numpy(length, self.model.data.transformations[data_index][1], 0, data_index)
        for n in range(1, len(columns_name)):
            y = self.define_numpy(length, self.model.data.transformations[data_index][1], n, data_index)
            window.set_curve(x, y, columns_name[n])
        self.my_interface.show_graphic(window)
        return x,y

    def redefine_graphic_freq(self,x,y ,window, data_index=-1):
        if (x[-1] <= 1):
            sample_rate = len(x) * 1 / x[-1]
        else:
            sample_rate = len(x) / x[-1]
        columns_name = self.model.data.transformations[data_index][0].names
        if (window.refresh_graphic(data_index)):
            freq, count, freq_complete = self.defineX(x, sample_rate)
            for n in range(1, len(columns_name)):
                fourier_complete, fourier_no_complexe = self.defineY(y, count)
                window.set_curve(freq, fourier_no_complexe, columns_name[n])
                self.model.data.insert_transformation_fourier([freq_complete, fourier_complete])
        self.my_interface.show_graphic(window)

    def defineX(self, data, sample_rate):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
       Convertie les donnee temporelle en frequentielle

        """
        n = len(data)
        freq = fftpack.fftfreq(n) * sample_rate
        i = 0
        while (freq[i] >= 0):
            i = i + 1
        freqreturn = [0] * i
        for x in range(0, i):
            freqreturn[x] = freq[x]
        return freqreturn, i, freq

    def defineY(self, data, count):
        """
        :param data: -> numpy > donnee que l'on veut convertire
        :param sample_rate -> int > le sample rate a laquelle les donnees sont calculer
        Convertie les donnee temporelle en frequentielle
        """
        fourier = fftpack.fft(data)
        fourierNoComplex = [0] * count;
        for x in range(0, count):
            fourierNoComplex[x] = fourier[x].real
        return fourier, fourierNoComplex

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
            self.redefine_graphic(self.my_interface.fourier_window, -2)
            self.redefine_graphic(self.my_interface.time_window, -2)
        else:
            self.redefine_graphic(self.my_interface.fourier_window, plot_index)
            self.redefine_graphic(self.my_interface.time_window, plot_index)

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

    def deactivate_transformation(self):
        if (len(
                self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value()) < len(
                self.model.data.transformations):
            cpt = len(self.model.data.transformations) - (len(
                self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value())
            for i in range(0, cpt):
                self.model.data.transformations[len(
                    self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value() + i][
                    0].state = False

    def show_Filter_Window(self):
        self.my_interface.show_filter_window()
