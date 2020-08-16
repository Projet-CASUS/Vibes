import numpy as np
import scipy.signal as signal
convolve = np.convolve
import transform


class FIR (Filter):
    def __init__(self, sample_rate, numtaps = 5):
        super().__init__()
        self.sample_rate = sample_rate
        self.numtaps = numtaps

    def __call__(self, data, type, cutoff):
        self.data = data
        self.cutoff = cutoff

        fir_filter = None

        # On définit le filtre à utiliser
        if type == "passe_bas":
            fir_filter = self.passe_bas()
        elif type == "passe_haut":
            fir_filter = self.passe_haut()
        elif type == "passe_bande":
            fir_filter = self.passe_bande()

        # On effectue la convolution du filtre FIR
        filtered_data = convolve(data, fir_filter, 'same')
        return filtered_data

    def passe_bas(self):  # Définit le vecteur de filtre FIR pour un passe bas
        f = self.cutoff / self.sample_rate
        return signal.firwin(self.numtaps, f)

    def passe_haut(self):  # Définit le vecteur de filtre FIR pour un passe haut
        f = self.cutoff / self.sample_rate
        return signal.firwin(self.numtaps, f, pass_zero=False)

    def passe_bande(self):  # Définit le vecteur de filtre FIR pour un passe bande
        f1 = float(self.cutoff[0] / self.sample_rate)
        f2 = float(self.cutoff[1] / self.sample_rate)
        return signal.firwin(self.numtaps, self.cutoff, pass_zero=False)