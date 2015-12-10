from air import rho, c
import numpy as np

class VentedBox(object):
    """ Model a vented box loudspeaker enclosure """

    def __init__(self, Vab, Fb):
        self.Vab = Vab
        self.Cab = Vab / (rho*c**2)
        self.Fb = Fb
        self.wb = 2*np.pi*Fb
        self.Tb = 1 / self.wb

    def set_Vab(self, Vab):
        self.Vab = Vab
        self.Cab = Vab / (rho*c**2)
        
    def set_Fb(self, Fb):
        self.Fb = Fb
        self.wb = 2*np.pi*Fb
        self.Tb = 1 / self.wb
