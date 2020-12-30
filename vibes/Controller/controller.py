import sys
import vibes
import vibes.View.qt_view as view
import vibes.Model.model as models
import vibes.Controller.transform as trans
from PyQt5.Qt import QApplication

class Controller():
    def __init__(self, data_file):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.model = models.Model(data_file)
        self.my_interface = view.graphical_interface()
        ### todo DECOUPLER DU CONTROLLER
        ## Ne peut pas être découpler puisque connect dois être fais dans le controlleur sinon on créer plein de fonction inutile
        self.my_interface.pipeline_window.widget.pipeline_index = len(self.model.data.transformations[0])
        self.my_interface.pipeline_window.widget.pipeline_slider.valueChanged.connect(self.update_pipeline)
        self.my_interface.pipeline_window.widget.differentiel.clicked.connect(self.differentiel_event)
        self.my_interface.pipeline_window.widget.rangeSelection.clicked.connect(self.rangeSelection_event)
        self.my_interface.pipeline_window.widget.merger.clicked.connect(self.merger_event)
        self.my_interface.pipeline_window.widget.exportWav.clicked.connect(self.exporter_event)
        self.my_interface.pipeline_window.widget.FirPasseBas.clicked.connect(self.fir_passe_bas_event)
        self.my_interface.pipeline_window.widget.FirPasseHaut.clicked.connect(self.fir_passe_haut_event)
        self.my_interface.pipeline_window.widget.FirPasseBande.clicked.connect(self.fir_passe_bande_event)
        self.my_interface.pipeline_window.widget.PasseBas.clicked.connect(self.passe_bas_event)
        self.my_interface.pipeline_window.widget.PasseHaut.clicked.connect(self.passe_haut_event)
        self.my_interface.pipeline_window.widget.PasseBande.clicked.connect(self.passe_bande_event)
        ### DECOUPLER DU CONTROLLER

        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()
        self.show_Filter_Window()

    def passe_bas_event(self):
        data = self.model.data.transformations[-1]
        cut_off = 0
        if self.my_interface.pipeline_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.pipeline_window.widget.cut_off.text()
        self.filter2(data,int(cut_off),0,0, self.model.data.transformations_fourier[-1],"passe_bas")
    def passe_haut_event(self):
        data = self.model.data.transformations[-1]
        cut_off = 0
        if self.my_interface.pipeline_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.pipeline_window.widget.cut_off.text()
        self.filter2(data, int(cut_off), 0, 0, self.model.data.transformations_fourier[-1], "passe_haut")
    def passe_bande_event(self):
        data = self.model.data.transformations[-1]
        cut_off = 0
        cut_off2 = 0
        if self.my_interface.pipeline_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.pipeline_window.widget.cut_off.text()
        if self.my_interface.pipeline_window.widget.cut_off2.text() != '':
            cut_off2 = self.my_interface.pipeline_window.widget.cut_off2.text()
        self.filter2(data, int(cut_off), int(cut_off2), 0, self.model.data.transformations_fourier[-1], "passe_bande")
    def fir_passe_bas_event(self):
        data = self.model.data.transformations[-1]
        cut_off = 0
        if self.my_interface.pipeline_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.pipeline_window.widget.cut_off.text()
        self.filter(data,int(cut_off),0,"passe_bas")

    def fir_passe_haut_event(self):
        data = self.model.data.transformations[-1]
        cut_off = 0
        if self.my_interface.pipeline_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.pipeline_window.widget.cut_off.text()
        self.filter(data,int(cut_off),0,"passe_haut")

    def fir_passe_bande_event(self):
        data = self.model.data.transformations[-1]
        cut_off = 0
        cut_off2 = 0
        if self.my_interface.pipeline_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.pipeline_window.widget.cut_off.text()
        if self.my_interface.pipeline_window.widget.cut_off2.text() != '':
            cut_off2 = self.my_interface.pipeline_window.widget.cut_off2.text()
        self.filter(data,int(cut_off),int(cut_off2),"passe_bande")

    def exporter_event(self):
        self.model.data.export_wav(self.model.data)

    def merger_event(self):
        data = self.model.data.transformations
        self.Merging(data)

    def rangeSelection_event(self):
        first = 0
        last = len(self.model.data.transformations[-1][-1])
        if(self.my_interface.pipeline_window.widget.first.text() != ''):
            first = int(self.my_interface.pipeline_window.widget.first.text())
        if(self.my_interface.pipeline_window.widget.last.text() != ''):
            last = int(self.my_interface.pipeline_window.widget.last.text())
        self.time_range_selections(first,last)

    def differentiel_event(self):
        data = self.model.data.transformations[-1]
        self.differential(data)

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
        self.model.data.insert_transformation(vibes.Controller.transform.Range_selection, index,first,last, self.model.data.transformations[0])
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def differential(self, data, index= -1):
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Differential,index,data)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def integral(self,data, index =-1):
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Integral,index,data)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def Merging(self,data,index = -1):
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Merge,index,data)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def filter(self,data, cut_off,cut_off2, type,index = -1):
        if(data[1][-1][0] <=1):
            sample_rate = len(data[1])*1/data[1][-1][0]
        else:
            sample_rate = len(data[1])/data[1][-1][0]
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Filter,index,sample_rate,cut_off,cut_off2,data,type)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()

    def filter2(self,data,cut_off, cut_off2, attenuation,fourier,type,index = -1):
        if(data[1][-1][0] <=1):
            sample_rate = len(data[1])*1/data[1][-1][0]
        else:
            sample_rate = len(data[1])/data[1][-1][0]
        self.deactivate_transformation()
        self.model.data.insert_transformation(vibes.Controller.transform.Filter2,index,data,fourier,cut_off,cut_off2,attenuation,type)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)
        self.define_pipeline_browser()


    def redefine_graphic(self, window, data_index=-1):
        """
        Cette fonction redefinit les valeurs a afficher sur un graphique
        :param window: -> QWindow > Une QWindow d'un graphique ex: temps frequence
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        """
        columns_name = self.model.data.transformations[data_index][0].names
        if (window.refresh_graphic(data_index)):
            length = len(self.model.data.transformations[data_index][1])
            x = self.define_numpy(length, self.model.data.transformations[data_index][1], 0, data_index)
            for n in range(1, len(columns_name)):
                y = self.define_numpy(length, self.model.data.transformations[data_index][1], n, data_index)
                # decoupler element de la vue
                freq, fourier = window.set_curve(x, y, columns_name[n])
                if(len(fourier) > 2):
                    self.model.data.insert_transformation_fourier([freq,fourier])
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
            self.redefine_graphic(self.my_interface.fourier_window, -2)
            self.redefine_graphic(self.my_interface.time_window, -2)
        else:
            self.redefine_graphic(self.my_interface.fourier_window, plot_index)
            self.redefine_graphic(self.my_interface.time_window, plot_index)

    def define_numpy(self, length, datastructure, column,index=-1):
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
        if (len(self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value()) < len(self.model.data.transformations):
            cpt = len(self.model.data.transformations) - (len(self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value())
            for i in range(0, cpt):
                self.model.data.transformations[len(self.model.data.transformations) - self.my_interface.pipeline_window.widget.pipeline_slider.value()+i][0].state = False

    def show_Filter_Window(self):
        self.my_interface.show_filter_window()



