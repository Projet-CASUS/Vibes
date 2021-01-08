class filter_events:
    """
    Contient toute les événements pour filter les données
    """
    def __init__(self, controller, my_interface):
        """
        :param controller: -> controller > référence au controller
        """
        self.controller = controller
        self.my_interface = my_interface

    def passe_bas_event(self):
        """
        evenement permetant de filtrer en passe_bas avec les filtre manuelle
        """
        data = self.define_data()
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.filter(data, float(cut_off), 0, float(att),
                               [self.controller.model.data.transformations[-1][0].freq,self.controller.model.data.transformations[-1][0].fourier_no_complexe], "passe_bas")

    def passe_haut_event(self):
        """
        evenement permetant de filtrer en passe_haut avec les filtre manuelle
        """
        data = self.define_data()
        cut_off = self.define_cut_off1()
        att = self.define_att()
        self.controller.filter(data, float(cut_off), 0, float(att),
                               [self.controller.model.data.transformations[-1][0].freq,self.controller.model.data.transformations[-1][0].fourier_no_complexe], "passe_haut")

    def passe_bande_event(self):
        """
        evenement permetant de filtrer en passe_bande avec les filtre manuelle
        """
        data = self.define_data()
        cut_off = self.define_cut_off1()
        cut_off2 = self.define_cut_off2()
        att = self.define_att()
        self.controller.filter(data, float(cut_off), float(cut_off2), float(att),
                               [self.controller.model.data.transformations[-1][0].freq,self.controller.model.data.transformations[-1][0].fourier_no_complexe],
                                "passe_bande")

    def fir_passe_bas_event(self):
        """
        evenement permetant de filtrer en passe_bas avec les filtre fir
        """
        data = self.define_data()
        cut_off = self.define_cut_off1()
        num_taps = self.define_att()
        self.controller.filter_fir(data, data[0].sample_rate, float(cut_off), 0,"passe_bas", int(num_taps))

    def fir_passe_haut_event(self):
        """
        evenement permetant de filtrer en passe_haut avec les filtre fir
        """
        data = self.define_data()
        cut_off = self.define_cut_off1()
        num_taps = self.define_att()
        self.controller.filter_fir(data, data[0].sample_rate, float(cut_off), 0,"passe_haut", int(num_taps))

    def fir_passe_bande_event(self):
        """
        evenement permetant de filtrer en passe_bande avec les filtre fir
        """
        data = self.define_data()
        cut_off = self.define_cut_off1()
        cut_off2 = self.define_cut_off2()
        num_taps = self.define_att()
        self.controller.filter_fir(data, data[0].sample_rate, float(cut_off), float(cut_off2),"passe_bande", int(num_taps))

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
        if self.my_interface.dashboard_window.widget.cut_off.text() != '':
            cut_off = self.my_interface.dashboard_window.widget.cut_off.text()
        return cut_off

    def define_cut_off2(self):
        """
        :return: -> la valeur du deuxième cut-off utile pour les passes-bandes
        """
        cut_off = 0
        if self.my_interface.dashboard_window.widget.cut_off2.text() != '':
            cut_off = self.my_interface.dashboard_window.widget.cut_off2.text()
        return cut_off

    def define_att(self):
        """
        :return: -> la valeur de l'atténuation
        """
        att = 0
        if self.my_interface.dashboard_window.widget.attenuation_num_taps.text() != '':
            att = self.my_interface.dashboard_window.widget.attenuation_num_taps.text()
        return att
