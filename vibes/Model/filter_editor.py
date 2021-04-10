from casus.filter_editor.editors import bode_plot_editor as bode_plot_editor
from casus.filter_editor.editors import phase_plot_editor as phase_plot_editor
from casus.filter_editor.editors import pole_plot_editor as pole_plot_editor
import math

class filter_editor():
    def __init__(self):
        """
        :param first: -> int > premiere donne de temps
        :param last: -> int > derniere donnee de temps
        :param data: -> transformation > contient la dernière transformation dans le pipeline
        """
        self.type = "filter_editor"

    def stand_in(self, filter_editor):
        self.type = filter_editor.type
        self.type_plot = filter_editor.type_plot
        self.bode_plot_editor = bode_plot_editor.bode_plot_editor()
        self.bode_plot_editor.plug(filter_editor.get_plot_editor())
        self.phase_plot_editor = phase_plot_editor.phase_plot_editor()
        self.phase_plot_editor.plug(filter_editor.get_plot_editor())
        self.pole_plot_editor = pole_plot_editor.pole_plot_editor()
        self.pole_plot_editor.plug(filter_editor.get_plot_editor())

    def __call__(self, data_in, data_out,fc1,fc2,type_filter,type_plot):
        self.type = type
        self.type_plot = type_plot
        self.bode_plot_editor = bode_plot_editor.bode_plot_editor()
        self.bode_plot_editor.plug2(data_in, data_out,fc1,fc2,type_filter)
        self.phase_plot_editor = phase_plot_editor.phase_plot_editor()
        self.phase_plot_editor.plug2(data_in, data_out,fc1,fc2,type_filter)
        self.pole_plot_editor = pole_plot_editor.pole_plot_editor()
        self.pole_plot_editor.plug2(data_in, data_out,fc1,fc2,type_filter)

    def get_data_for_graphic(self):

        if(self.type_plot == bode_plot_editor.bode_plot_editor):
            self.bode_plot_editor.get_data_for_graphic()
        elif(self.type_plot == phase_plot_editor.phase_plot_editor):
            self.phase_plot_editor.get_data_for_graphic()
        elif(self.type_plot == pole_plot_editor.pole_plot_editor):
            self.pole_plot_editor.get_data_for_graphic()

    def modify_response(self, first, last, attenuation, type):

        if(self.type_plot == bode_plot_editor.bode_plot_editor):
            self.bode_plot_editor.modify_response(first, last, attenuation, type)
        elif(self.type_plot == phase_plot_editor.phase_plot_editor):
            self.phase_plot_editor.modify_response(first, last, attenuation, type)
        elif(self.type_plot == pole_plot_editor.pole_plot_editor):
            self.pole_plot_editor.modify_response(first, last, attenuation, type)

    def get_plot_editor(self):
        if(self.type_plot == bode_plot_editor.bode_plot_editor):
            return self.bode_plot_editor
        elif(self.type_plot == phase_plot_editor.phase_plot_editor):
            return self.phase_plot_editor
        elif(self.type_plot == pole_plot_editor.pole_plot_editor):
            return self.pole_plot_editor

    def set_type_plot(self, type):
        self.type_plot = type


