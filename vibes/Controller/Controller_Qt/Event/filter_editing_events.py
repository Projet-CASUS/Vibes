class filter_editing_events:

    def __init__(self, controller, my_interface):
        self.controller = controller
        self.my_interface = my_interface

    def merge_event(self):
        pass

    def range_selection_event(self):
        pass

    def make_filter_event(self):
        self.controller.redefine_filter_data(self.controller.filter_model)

    def integral_event(self):
        pass

    def interpolation_event(self):
        pass

    def passe_bas_event(self):
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.modify_filter_response(cut_off,0,att,"passe bas")

    def define_data(self):
        """
        :return: -> les dernières valuer de transformation dans le pipeline
        """
        return self.controller.model.data.transformations[-1]

    def define_cut_off1(self):
        """
        :return: -> la valeur du premier cut-off
        """
        cut_off = 0
        if self.my_interface.dashboard_filter_editing_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.dashboard_filter_editing_window.widget.cut_off.text()
        return cut_off

    def define_cut_off2(self):
        """
        :return: -> la valeur du deuxième cut-off utile pour les passes-bandes
        """
        cut_off = 0
        if self.my_interface.dashboard_filter_editing_window.widget.cut_off2.text() != '':
            cut_off = self.my_interface.dashboard_filter_editing_window.widget.cut_off2.text()
        return cut_off

    def define_att(self):
        """
        :return: -> la valeur de l'atténuation
        """
        att = 0
        if self.my_interface.dashboard_filter_editing_window.widget.attenuation_num_taps.text() != '':
            att = self.my_interface.dashboard_filter_editing_window.widget.attenuation_num_taps.text()
        return att