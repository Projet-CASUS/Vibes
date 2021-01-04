class events:

    def __init__(self,controller):
        self.controller = controller

    def export_event(self):
        self.controller.model.data.export_wav(self.model.data)

    def merge_event(self):
        data = self.controller.model.data.transformations
        self.controller.Merging(data)

    def range_selection_event(self):
        first = 0
        last = len(self.controller.model.data.transformations[-1][-1])
        if (self.controller.my_interface.DashBoard_window.widget.first.text() != ''):
            first = int(self.controller.my_interface.DashBoard_window.widget.first.text())
        if (self.controller.my_interface.DashBoard_window.widget.last.text() != ''):
            last = int(self.controller.my_interface.DashBoard_window.widget.first.text())
        self.controller.time_range_selections(first, last)

    def differentiel_event(self):
        data = self.controller.model.data.transformations[-1]
        self.controller.differential(data)

    def activate_field(self):

        for x in range(0, len(self.controller.my_interface.DashBoard_window.layoutText)):
            self.controller.my_interface.DashBoard_window.layoutText.itemAt(x).widget().setEnabled(False)

