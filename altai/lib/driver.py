# -*- coding: utf-8 -*-
"""Collect driver parameters."""
import numpy as np
from . import air


class Driver(object):
    """Class to model driver units."""

    def __init__(self, manufacturer, model):
        """Create a new driver.

        Args:
            manufacturer : manufacturer of the driver
            model : model name of the driver
        """
        #: Manufacturer Name
        self.manufacturer = manufacturer
        #: Model Name
        self.model = model
        #: Driver Diameter, in inches
        self.diameter = 0.0
        #: Driver Net Weight, in kg
        self.weight = 0.0
        #: AES Power Handling, in W
        self.power = 0.0
        #: Total Q of driver
        self.Qts = 0.0
        #: Electrical Q of driver
        self.Qes = 0.0
        #: Projected area of driver diaphragm, in m²
        self.Sd = 0.0
        #: Mechanical mass (including air mass), in kg
        self.Mms = 0.0
        #: Linear peak excursion :math:`x_{max}` in m
        self.xmax = 0.0
        #: Angular frequency :math:`\omega_s = 2 \pi f_s`
        #:
        #: .. note:: Do not set this directly, use :meth:`fs`
        self.ws = 0.0
        #: Acoustic compliance of drivers suspension :math:`C_{as}`
        #:
        #: .. note:: Do not set this directly, use :meth:`Vas`
        self.Cas = 0.0
        #: Time constant of the driver :math:`T_s = \frac{1}{\omega_s}`, not to
        #: be confused with a period
        #: :math:`t = \frac{1}{f} = \frac{2\pi}{\omega}`
        #:
        #: .. note:: Do not set this directly, use :meth:`fs`
        self.Ts = 0.0
        self._fs = 0.0
        self._Vas = 0.0

    @property
    def fs(self):
        """Driver resonance frequency in Hz.

        The resonance frequency of the driver, in Hz. Setting this attributes
        also sets :attr:`Ts` and :attr:`ws`.
        """
        return self._fs

    @fs.setter
    def fs(self, fs):
        """Set Fs, as well as ws and Ts."""
        self._fs = fs
        self.ws = 2*np.pi*fs
        self.Ts = 1/self.ws

    @property
    def Vas(self):
        r"""Driver equivalent compliance volume.

        The equivalent compliance volume, i.e. that volume of air that has the
        same compliance as the drivers suspension
        :math:`V_{as} = \rho c^2 C_{as}`. Setting this attribute also sets
        :attr:`Cas`.
        """
        return self._Vas

    @Vas.setter
    def Vas(self, Vas):
        """Set Vas, as well a Cas."""
        self._Vas = Vas
        self.Cas = Vas / (air.RHO*air.C**2)

    def __repr__(self):
        """Return a string representation of the driver."""
        return self.manufacturer + " " + self.model

    def dict_representation(self):
        """Return a dict representation, useful for writing to JSON."""
        representation = {'manufacturer': self.manufacturer,
                          'model':        self.model,
                          'diameter':     self.diameter,
                          'weight':       self.weight,
                          'power':        self.power,
                          'Qts':          self.Qts,
                          'Sd':           self.Sd,
                          'xmax':         self.xmax,
                          'fs':           self.fs,
                          'Vas':          self.Vas,
                          'Qes':          self.Qes,
                          'Mms':          self.Mms
                          }
        return representation

    @classmethod
    def from_dict(cls, dictionary):
        """Create a new driver from a dictionary.

        Args:
            dictionary : dictionary that contains driver data

        Example:
            >>> driver_properties = {'manufacturer': "B&C Speakers", 
            >>>                      'model': "15SW115", 'fs': 35.0}
            >>> mydriver = Driver.from_dict(driver_properties)
        """
        driver = cls(dictionary.get('manufacturer'), dictionary.get('model'))
        driver.diameter = dictionary.get('diameter')
        driver.weight   = dictionary.get('weight')
        driver.power    = dictionary.get('power')
        driver.Qts      = dictionary.get('Qts')
        driver.Sd       = dictionary.get('Sd')
        driver.xmax     = dictionary.get('xmax')
        driver.fs       = dictionary.get('fs')
        driver.Vas      = dictionary.get('Vas')
        driver.Qes      = dictionary.get('Qes')
        driver.Mms      = dictionary.get('Mms')
        return driver
