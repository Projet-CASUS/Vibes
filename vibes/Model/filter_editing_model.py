import vibes.Model.filter_editing_data as data

class filter_editing_model:

    def __init__(self, data_in, data_out, fc1, fc2, type):
        self.data = data.Data(data_in, data_out, fc1, fc2 ,type)
    def save(self):
        pass

    def load(self):
        pass

    def export_Wav(self):
        pass