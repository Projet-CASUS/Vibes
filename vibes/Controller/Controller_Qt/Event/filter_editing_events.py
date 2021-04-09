from vibes.Model import filter_editor


class filter_editing_events:

    def __init__(self, filter_editing_controller, my_interface):
        self.controller = filter_editing_controller
        self.my_interface = my_interface
        self.type = filter_editor.filter_editor_bode
        self.window = self.my_interface.bode_plot_window
        self.name = "bode plot"

    def merge_event(self):
        pass

    def range_selection_event(self):
        pass

    def make_filter_event(self):
        self.controller.redefine_filter_data(self.controller)

    def integral_event(self):
        pass

    def interpolation_event(self):
        pass

    def activate_phase_plot_event(self):
        self.type = filter_editor.filter_editor_phase
        self.window = self.my_interface.phase_plot_window
        self.name = "phase plot"
        self.my_interface.bode_plot_window.qwt_plot.close()
        self.controller.make_plot(self.type,self.window,self.name)

    def activate_bode_plot_event(self):
        self.type = filter_editor.filter_editor_bode
        self.window = self.my_interface.bode_plot_window
        self.name = "bode plot"
        self.my_interface.phase_plot_window.qwt_plot.close()
        self.controller.make_plot(self.type,self.window,self.name)

    def passe_bas_event(self):
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.modify_filter_response(cut_off,0,att,"passe bas",self.type,self.window,self.name)

    def passe_haut_event(self):
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.modify_filter_response(cut_off,0,att,"passe haut",self.type,self.window,self.name)

    def passe_bande_event(self):
        cut_off = self.define_cut_off1()
        cut_off2 = self.define_cut_off2()
        att = self.define_att()
        self.controller.modify_filter_response(cut_off,cut_off2,att,"passe bas",self.type,self.window,self.name)

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