import numpy as np
import scipy.signal as signal
convolve = np.convolve


class FIR:
    def __init__(self, sample_rate, num_taps = 5):
        super().__init__()
        self.sample_rate = sample_rate
        self.num_taps = num_taps

    def __call__(self, data, type, cut_off):
    # data   = Vecteur de données à filtrer
    # type   = Type de filtre [format texte] (passe_bas || passe_haut || passe_bande || coupe_bande)
    # cutoff = Fréquence de coupure passe_bas   & passe_haut  =>[int || float] 
    #                               passe_bande & coupe_bande =>[vect de 2 int || float]
    # ref: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.firwin.html
        self.data = data
        self.cut_off = cut_off

        fir_filter = None

        # On définit le filtre à utiliser
        if type == "passe_bas":
            fir_filter = self.passe_bas()
        elif type == "passe_haut":
            fir_filter = self.passe_haut()
        elif type == "passe_bande":
            fir_filter = self.passe_bande()
        elif type == "coupe_bande":
            fir_filter = self.coupe_bande()

        # On effectue la convolution du filtre FIR
        filtered_data = convolve(data, fir_filter, 'same')
        return filtered_data

    def passe_bas(self):  # Définit le vecteur de filtre FIR pour un passe bas
        f = self.cut_off / self.sample_rate
        return signal.firwin(self.num_taps, f)

    def passe_haut(self):  # Définit le vecteur de filtre FIR pour un passe haut
        f = self.cut_off / self.sample_rate
        return signal.firwin(self.num_taps, f, pass_zero=False)

    def passe_bande(self):  # Définit le vecteur de filtre FIR pour un passe bande
        f1 = float(self.cut_off[0] / self.sample_rate)
        f2 = float(self.cut_off[1] / self.sample_rate)
        return signal.firwin(self.num_taps, [f1, f2], pass_zero=False)

    def coupe_bande(self):  # Définit le vecteur de filtre FIR pour un passe bande
        f1 = float(self.cut_off[0] / self.sample_rate)
        f2 = float(self.cut_off[1] / self.sample_rate)
        return signal.firwin(self.num_taps, [f1, f2])
