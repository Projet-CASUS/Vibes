class events:
    """
    class permettant d'appeler des evenements pour créer des transformation
    """
    def __init__(self, controller, my_interface):
        """
        :param controller: -> controller > la référence au controller
        """
        self.controller = controller
        self.my_interface = my_interface

    def export_event(self):
        """
        Permet d'exporter un fichier en wav
        """
        self.controller.model.data.export_wav(self.model.data)

    def merge_event(self):
        """
        permet de prendre une fourchette de donnée modifier et de la réintégrer dans l'ensemble des données
        """
        data = self.controller.model.data.transformations
        self.controller.merging(data)

    def range_selection_event(self):
        """
        permet de prendre une fourchette de données
        """
        first = 0
        last = len(self.controller.model.data.transformations[-1][-1])
        if self.my_interface.dashboard_window.widget.first.text() != '':
            first = int(self.my_interface.dashboard_window.widget.first.text())
        if self.my_interface.dashboard_window.widget.last.text() != '':
            last = int(self.my_interface.dashboard_window.widget.last.text())
        self.controller.time_range_selections(first, last)

    def differentiel_event(self):
        """
        permet de calculer la différentielle des données temporelles
        """
        data = self.controller.model.data.transformations[-1]
        self.controller.differential(data)

