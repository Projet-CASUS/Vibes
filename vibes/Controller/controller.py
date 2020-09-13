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
        self.my_interface.pipeline_window.widget.pipeline_index = len(self.model.data.transformations[0])
        self.my_interface.pipeline_window.widget.pipeline_slider.valueChanged.connect(self.update_pipeline)
        self.redefine_graphic(self.my_interface.time_window)
        self.redefine_graphic(self.my_interface.fourier_window)

    def add_data(self, type, data_file):
        """
        Permet d instancier un objet de data dans le model
        Note: is it useful if so we need to modify add_transformation to review the tuple
        """
        self.model.data.add_transformation(trans.import_file, type, data_file)

    def data_range_selections(self, first, last , index=-1):
         """
         fait une selection de donnée dans la section des données temporelles.
         update le view en mettant en evidence les limites
         ***definire comment modifier Model.data en conséquence***
         :param first: -> int > Temps du debut de la fourchette de temps
         :param last: -> int > Temps de fin de la fourchette de temps selectionne
         :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
         """
         self.model.data.add_transformation(vibes.Controller.transform.Range_selection, index, first, last)
         self.redefine_graphic(self.my_interface.time_window)
         self.redefine_graphic(self.my_interface.fourier_window)
         self.define_pipeline_browser()

    def redefine_graphic(self, window, data_index =-1):
        panda_columns_name = self.model.data.transformations[data_index][1].columns
        if (window.widget.wrapper_widget_qwt.refresh_graphic(data_index)):
            length = len(self.model.data.transformations[data_index][1])
            x = self.define_numpy(length, data_index, panda_columns_name[0])
            if(window.name == "Freq"):
                x = window.defineX(x,200)
            for n in range(1, len(panda_columns_name)):
                y = self.define_numpy(length, data_index, panda_columns_name[n])
                if(window.name == "Freq"):
                    y = window.defineY(y,200)
                # decoupler element de la vue
                window.widget.wrapper_widget_qwt.set_curve(x, y, window.name)
            self.my_interface.show_graphic(window)



    def define_pipeline_browser(self):
        """
        TODO philippe: Decrire ce que fait cette fonction (i.e. le scope de ses actions & ou et quand elle est call)
        faire samedi
        """
        self.my_interface.pipeline_window.define_pipeline_browser(self.model)
        self.my_interface.show_pipeline_browser()

    def update_pipeline(self):
        """
         Decrire ce que fait cette fonction (i.e. le scope de ses actions & ou et quand elle est call)
         TODO Philippe samedi
         """
        is_null = True
        plot_index = 0
        for x in range(0, len(self.model.data.transformations[0])):
            f = len(self.model.data.transformations[0]) - self.my_interface.pipeline_window.widget.pipeline_slider.value()
            if(x < f ):
                t = self.my_interface.pipeline_window.layout.itemAt(x).widget().setEnabled(True)
                is_null = False
                plot_index = x
            else:
                t = self.my_interface.pipeline_window.layout.itemAt(x).widget().setEnabled(False)
        if(is_null):
            self.redefine_graphic(self.my_interface.fourier_window, -2)
            self.redefine_graphic(self.my_interface.time_window, -2)
        else:
            self.redefine_graphic(self.my_interface.fourier_window, plot_index)
            self.redefine_graphic(self.my_interface.time_window, plot_index)

    def modify_pipeline(self):
         self.model.data.currentIndex = self.my_interface.pipeline_window.widget.pipeline_slider.value()


    def define_numpy(self,length, index, name):
        numpy = [None] * length
        for i in range(0, len(numpy)):
            numpy[i] = float(self.model.data.transformations[index][1].loc[:, name][i].replace(',', '.'))
        return numpy

