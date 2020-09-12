import sys
import vibes
import vibes.View.view as view
import vibes.Model.model as models
import vibes.Controller.transform as trans
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QFrame, QSlider, QHBoxLayout
from PyQt5.Qt import QApplication
from qwt import QwtPlot, QwtPlotCurve


class Controller():
    def __init__(self, data_file):
        """
        Init: reçois les argument sys.argv pour contruire un Qt application
        data_file: fichier contenant les donnees
        """
        self.app = QApplication(sys.argv)
        self.model = models.Model(data_file)
        self.my_interface = view.graphical_interface()
        self.my_interface.main_window.widget.pipeline_slider = QSlider()
        self.my_interface.main_window.widget.pipeline_index = len(self.model.data.transformations[0])
        self.my_interface.main_window.widget.pipeline_slider.valueChanged.connect(self.update_pipeline)

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

    def define_freq_graphic_x(self, x,index=-1):
        """
        TODO Philippe redo samedi
        Definit les valurs en x et y du graphique en temporelle.
        (1) determiner la derniere action dans le pipeline (csv, selection de donnee)
        (2)
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        -2 est un code pour indiquer que l'on devrais retirer tout graphique du main window
        """
        return self.my_interface.fourier_window.defineX(x, 200)

    def define_freq_graphic_y(self, y,index=-1):
        """
        TODO Philippe redo samedi
        Definit les valurs en x et y du graphique en temporelle.
        (1) determiner la derniere action dans le pipeline (csv, selection de donnee)
        (2)
        :param index: -> int > index du placement dans le pipeline (-1 est un shortcut de python pour acceder au dernier element du array);
        -2 est un code pour indiquer que l'on devrais retirer tout graphique du main window
        """
        return self.my_interface.fourier_window.defineY(y, 200)

    def define_graphic(self, window,index =-1):
        name_array = self.model.data.transformations[index][1].columns
        if (window.widget.wrapper_widget_qwt.refresh_graphic(index)):
            length = len(self.model.data.transformations[index][1])
            x = self.define_numpy(length,index,name_array[0])
            if(window.name == "Freq"):
                x = self.define_freq_graphic_x(x)
            for n in range(1, len(name_array) - 1):
                y = self.define_numpy(length, index, name_array[n])
                if(window.name == "Freq"):
                    y = self.define_freq_graphic_y(y)
                # decoupler element de la vue
                window.widget.wrapper_widget_qwt.set_curve(x, y, window.name)
            self.my_interface.show_graphic(window)


    def update_pipeline(self):
        """
        Decrire ce que fait cette fonction (i.e. le scope de ses actions & ou et quand elle est call)
        TODO Philippe samedi
        """
        is_null = True
        plot_index = 0
        for x in range(0, len(self.model.data.transformations[0])):
            f = len(self.model.data.transformations[0]) - self.my_interface.main_window.widget.pipeline_slider.value()
            if(x < f):
                t = self.my_interface.main_window.layout.itemAt(x).widget().setEnabled(True)
                is_null = False
                plot_index = x
            else:
                t = self.my_interface.main_window.layout.itemAt(x).widget().setEnabled(False)
        if(is_null):
            self.define_graphic(self.my_interface.fourier_window,-2)
            self.define_graphic(self.my_interface.time_window ,-2)
        else:
            self.define_graphic(self.my_interface.fourier_window,plot_index)
            self.define_graphic(self.my_interface.time_window,plot_index)

    def define_pipeline_browser(self):
        """
        TODO philippe: Decrire ce que fait cette fonction (i.e. le scope de ses actions & ou et quand elle est call)
        faire samedi
        """
        for x in range(0, len(self.model.data.transformations)):
            pipeline_entry = QLabel()
            pipeline_entry.setFixedSize(100, 20)
            pipeline_entry.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            pipeline_entry.setText(self.model.data.transformations[x][0].type)
            pipeline_entry.setAlignment(Qt.AlignCenter)
            self.my_interface.main_window.layout.addWidget(pipeline_entry)
        self.my_interface.main_window.widget.pipeline_slider.setRange(0,len(self.model.data.transformations))
        self.my_interface.main_window.widget.pipeline_slider.setTickInterval(1)
        self.my_interface.main_window.layout1.addWidget(self.my_interface.main_window.widget.pipeline_slider)
        self.my_interface.main_window.layout1.addLayout(self.my_interface.main_window.layout)
        self.my_interface.show_pipeline_browser()


    def modify_pipeline(self):
         self.model.data.currentIndex = self.my_interface.main_window.widget.pipeline_slider.value()


    def define_numpy(self,length, index, name):
        numpy = [None] * length
        for i in range(0, len(numpy)):
            numpy[i] = float(self.model.data.transformations[index][1].loc[:, name][i].replace(',', '.'))
        return numpy

