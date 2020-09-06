import vibes.Model.data as mc

class Model:
    """
    TODO Philippe: a-t-on besoin des undo  redo ici considerant qu on a deja le pipeline browser?
    """
    def __init__(self, data_file):
        pass
        self.data = mc.Data(data_file)

    def undo(self):
        pass

    def redo(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def export_Wav(self):
        pass