class filter_events:
    def __init__(self, controller):
        self.controller = controller

    def passe_bas_event(self):
        data = self.define_data()
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.filter2(data, float(cut_off), 0, float(att),
                                [self.controller.model.data.transformations[-1][0].freq,self.controller.model.data.transformations[-1][0].fourier_no_complexe], "passe_bas")

    def passe_haut_event(self):
        data = self.define_data()
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.filter2(data, float(cut_off), 0, float(att),
                                [self.controller.model.data.transformations[-1][0].freq,self.controller.model.data.transformations[-1][0].fourier_no_complexe], "passe_haut")

    def passe_bande_event(self):
        data = self.define_data()
        cut_off = self.define_cut_off1()
        cut_off2 = self.define_cut_off2()
        att = self.define_att()
        self.controller.filter2(data, float(cut_off), float(cut_off2), float(att),
                                [self.controller.model.data.transformations[-1][0].freq,self.controller.model.data.transformations[-1][0].fourier_no_complexe],
                                "passe_bande")

    def fir_passe_bas_event(self):
        data = self.define_data()
        cut_off = self.define_cut_off1()
        self.controller.filter_fir(data, data[0].sample_rate, float(cut_off), 0, "passe_bas")

    def fir_passe_haut_event(self):
        data = self.define_data()
        cut_off = self.define_cut_off1()
        self.controller.filter_fir(data, data[0].sample_rate, float(cut_off), 0, "passe_haut")

    def fir_passe_bande_event(self):
        data = self.define_data()
        cut_off = self.define_cut_off1()
        cut_off2 = self.define_cut_off2()
        self.controller.filter_fir(data, data[0].sample_rate, float(cut_off), float(cut_off2), "passe_bande")

    def define_data(self):
        return self.controller.model.data.transformations[-1]

    def define_cut_off1(self):
        cut_off = 0
        if self.controller.my_interface.dashboard_window.widget.cut_off.text() != '':
            cut_off = self.controller.my_interface.dashboard_window.widget.cut_off.text()
        return cut_off

    def define_cut_off2(self):
        cut_off = 0
        if self.controller.my_interface.dashboard_window.widget.cut_off2.text() != '':
            cut_off = self.controller.my_interface.dashboard_window.widget.cut_off2.text()
        return cut_off

    def define_att(self):
        att = 0
        if self.controller.my_interface.dashboard_window.widget.attenuation.text() != '':
            att = self.controller.my_interface.dashboard_window.widget.attenuation.text()
        return att

    def activate_field(self):
        for x in range(0, len(self.controller.my_interface.dashboard_window.widget.layout_text)):
            self.controller.my_interface.dashboard_window.layout_text.itemAt(x).widget().setEnabled(False)
