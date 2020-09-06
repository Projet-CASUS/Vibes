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
        self.my_interface.main_window.widget.pipeline_slider.valueChanged.connect(self.value_changed)

    def add_data(self, type, data_file):
        """
        Permet d instancier un objet de data dans le model
        Note: is it useful if so we need to modify add_transformation to review the tuple
        """
        self.model.data.add_transformation(trans.import_file, type, data_file)

    def data_range_selections(self, first, last , index=-1):
         """
         TODO Philippe que veut dire index ??? - first et last sont des secondes ou autre ???
         fait une selection de donnée dans la section des données temporelles.
         update le view en mettant en evidence les limites
         ***definire comment modifier Model.data en conséquence***
         :param first: -> int > Temps du debut de la fourchette de temps
         :param last: -> int > Temps de fin de la fourchette de temps selectionne
         :param index:
         """
         self.model.data.add_transformation(vibes.Controller.transform.Range_selection, index, first, last)

    def pop_up_graphic(self):
        """
        TODO philippe : encore besoin de cette fct?
        retire le graphics du model
        :return:
        """
        pass

    def define_freq_graphic(self, w=-1):
        """

        :param w: TODO Philippe decrire ce que veut dire w
        """
        name_array = ["time","gforce"]
        if(w == -2):
            self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot.close()
        else:
            self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot.close()
            self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot = view.qwt()
            length = len(self.model.data.transformations[w][1])
            if (self.model.data.transformations[w][0].type == "range_selection"):
                length = self.model.data.transformations[w][0].last - self.model.data.transformations[w][0].first
            x = [None] * length
            for i in range(0, len(x)):
                x[i] = float(self.model.data.transformations[w][1].loc[:, name_array[0]][i].replace(',', '.'))
            freq = self.my_interface.fourier_window.defineX(x, 200)
            for n in range(1, len(name_array)):
                y = [None] * length
                for i in range(0, len(y)):
                    y[i] = float(self.model.data.transformations[w][1].loc[:, name_array[n]][i].replace(',', '.'))
                fourier = self.my_interface.fourier_window.defineY(y, 200)
                curve = QwtPlotCurve(name_array[n])
                curve.setData(freq, fourier)
                curve.attach(self.my_interface.fourier_window.widget.wrapper_widget_qwt.qwtPlot)
            self.my_interface.show_fourier()

    def define_time_graphic(self, w=-1):
        """
        afficher le graphique en temporelle du model
        :param w: TODO Philippe decrire ce que veut dire w
        """
        name_array = ["time", "x", "y", "z", "gforce"]
        if(w == -2):
            self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot.close()
        else:
            self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot.close()
            self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot = view.qwt()
            length =len(self.model.data.transformations[w][1])
            if(self.model.data.transformations[w][0].type == "range_selection"):
                length = self.model.data.transformations[w][0].last - self.model.data.transformations[w][0].first
            x = [None]*length
            for i in range(0, len(x)):
                x[i] = float(self.model.data.transformations[w][1].loc[:, name_array[0]][i].replace(',', '.'))
            for n in range(1, len(name_array)-1):
                y = [None]*length
                for i in range(0, len(y)):
                    y[i] = float(self.model.data.transformations[w][1].loc[:, name_array[n]][i].replace(',', '.'))
                curve = QwtPlotCurve(name_array[n])
                curve.setData(x, y)
                curve.attach(self.my_interface.time_window.widget.wrapper_widget_qwt.qwtPlot)

            self.my_interface.show_time_graphic()

    def value_changed(self):
        # TODO philippe: a-t-on vraiment besoin de call value_changed pour call update_pipeline?
        self.update_pipeline()

    def update_pipeline(self):
        """
        Decrire ce que fait cette fonction (i.e. le scope de ses actions & ou et quand elle est call)
        TODO philippe: mettre plus de commentaire dans cette fonction
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
            self.define_time_graphic(-2)
            self.define_freq_graphic(-2)
        else:
            self.define_time_graphic(plot_index)
            self.define_freq_graphic(plot_index)

    def define_pipeline_browser(self):
        """
        TODO philippe: Decrire ce que fait cette fonction (i.e. le scope de ses actions & ou et quand elle est call)
        """
        for x in range(0, len(self.model.data.transformations)):
            pipeline_entry = QLabel()
            pipeline_entry.setFixedSize(100, 20)
            pipeline_entry.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            pipeline_entry.setText(self.model.data.transformations[x][0].type)
            pipeline_entry.setAlignment(Qt.AlignCenter)
            self.my_interface.main_window.layout.addWidget(pipeline_entry)
            self.my_interface.main_window.widget.pipeline_slider.setRange(0, x + 1)
        self.my_interface.main_window.widget.pipeline_slider.setTickInterval(1)
        self.my_interface.main_window.layout1.addWidget(self.my_interface.main_window.widget.pipeline_slider)
        self.my_interface.main_window.layout1.addLayout(self.my_interface.main_window.layout)
        self.my_interface.show_pipeline_browser()


    def modify_pipeline(self):
         self.model.data.currentIndex = self.my_interface.main_window.widget.pipeline_slider.value()








