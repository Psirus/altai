import numpy as np
from air import rho, c

class Driver(object):
    """ Class to model drivers """
    def __init__(self, manufacturer, model):
        self.manufacturer = manufacturer
        self.model = model
        self.Qts = 0.0
        self.Sd = 0.0

    @property
    def fs(self):
        """ Driver resonance frequency """
        return self._fs

    @fs.setter
    def fs(self, fs):
        """ Set Fs as well as ws (:math:`\omega_s = 2 \pi f_s`) and 
            Ts (:math:`T_s = \frac{1}{\omega_s}."""
        self._fs = fs
        self.ws = 2*np.pi*fs
        self.Ts = 1/self.ws

    @property
    def Vas(self):
        """ Driver equivalent compliance volume

        .. math:: C_{as} = \frac{V_{as}}{\rho c^2}
        """
        return self._Vas

    @Vas.setter
    def Vas(self, Vas):
        self._Vas = Vas
        self.Cas = Vas / (rho*c**2)

    def __repr__(self):
        return self.manufacturer + " " + self.model
