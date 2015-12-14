# -*- coding: utf-8 -*-
""" Vented box enclosure """
import numpy as np
import air

class VentedBox(object):
    """ Model a vented box loudspeaker enclosure """

    def __init__(self, Vab, fb):
        self._Vab = Vab
        self.Cab = Vab / (air.RHO*air.C**2)
        self._fb = fb
        self.wb = 2*np.pi*fb
        self.Tb = 1 / self.wb

    @property
    def Vab(self):
        """ Box Volume in m³"""
        return self._Vab

    @Vab.setter
    def Vab(self, Vab):
        self._Vab = Vab
        self.Cab = Vab / (air.RHO*air.C**2)

    @property
    def fb(self):
        """ Box Tuning Frequency in Hz"""
        return self._fb

    @fb.setter
    def fb(self, fb):
        self._fb = fb
        self.wb = 2*np.pi*fb
        self.Tb = 1 / self.wb
