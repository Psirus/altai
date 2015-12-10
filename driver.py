from air import rho, c
import numpy as np

class Driver(object):
    """ Class to model drivers """
    def __init__(self, manufacturer, model):
        self.manufacturer = manufacturer
        self.model = model

    def set_fs(self, Fs):
        self.Fs = Fs
        self.ws = 2*np.pi*Fs
        self.Ts = 1/self.ws

    def set_Vas(self, Vas):
        self.Vas = Vas
        self.Cas = Vas / (rho*c**2)

    def set_Sd(self, Sd):
        self.Sd = Sd

    def set_Qts(self, Qts):
        self.Qts = Qts

    def __repr__(self):
        return self.manufacturer + " " + self.model
