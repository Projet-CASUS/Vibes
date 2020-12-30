class events:

    def __init__(self,controller):
        self.controller = controller

    def exporter_event(self):
        self.controller.model.data.export_wav(self.model.data)

    def merger_event(self):
        data = self.controller.model.data.transformations
        self.controller.Merging(data)

    def rangeSelection_event(self):
        first = 0
        last = len(self.controller.model.data.transformations[-1][-1])
        if (self.controller.my_interface.pipeline_window.widget.first.text() != ''):
            first = int(self.controller.my_interface.pipeline_window.widget.first.text())
        if (self.controller.my_interface.pipeline_window.widget.last.text() != ''):
            last = int(self.controller.my_interface.pipeline_window.widget.last.text())
        self.controller.time_range_selections(first, last)

    def differentiel_event(self):
        data = self.controller.model.data.transformations[-1]
        self.controller.differential(data)
