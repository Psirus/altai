# -*- coding: utf-8 -*-
""" Vented box enclosure """
import numpy as np
from . import air


class VentedBox(object):
    """ Model a vented box loudspeaker enclosure """

    def __init__(self, Vab, fb, Ql):
        self._Vab = Vab
        #: Acoustic compliance of box :math:`C_{ab}`
        #:
        #: .. note:: Do not set this directly, use :meth:`Vab`
        self.Cab = Vab / (air.RHO*air.C**2)
        self._fb = fb
        #: Angular frequency :math:`\omega_b = 2 \pi f_b`
        #:
        #: .. note:: Do not set this directly, use :meth:`fb`
        self.wb = 2.0*np.pi*fb
        #: Time constant of the box :math:`T_b = \frac{1}{\omega_b}`; not to
        #: be confused with a period
        #: :math:`t = \frac{1}{f} = \frac{2\pi}{\omega}`
        #:
        #: .. note:: Do not set this directly, use :meth:`fb`
        self.Tb = 1.0 / self.wb
        #: Enclosure leakage losses
        self.Ql = Ql

    @property
    def Vab(self):
        """ Box Volume in m³

        The box volume in m³. Setting this attribute also sets :attr:`Cab`.
        """
        return self._Vab

    @Vab.setter
    def Vab(self, Vab):
        """ Sets Vab, as well as Cab """
        self._Vab = Vab
        self.Cab = Vab / (air.RHO*air.C**2)

    @property
    def fb(self):
        """ Box Tuning Frequency in Hz

        The tuning frequency of the box. Setting this attribute also sets
        :attr:`wb` and :attr:`Tb`.
        """
        return self._fb

    @fb.setter
    def fb(self, fb):
        """ Sets fb, as well as wb and Tb """
        self._fb = fb
        self.wb = 2*np.pi*fb
        self.Tb = 1 / self.wb
