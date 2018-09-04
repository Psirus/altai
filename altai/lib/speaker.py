import numpy as np
import scipy.signal as signal
from . import air


class Speaker(object):

    def __init__(self, driver, box):
        self.driver = driver
        self.box = box


class VentedSpeaker(Speaker):

    def __init__(self, driver, box):
        Speaker.__init__(self, driver, box)

        # Response parameters
        self.T_0 = np.sqrt(driver.Ts * box.Tb)
        self.f_0 = 1.0 / (2.0*np.pi*self.T_0)
        # tuning ratio
        h = driver.Ts / box.Tb
        # compliance ratio
        c = driver.Cas / box.Cab

        self.a = np.zeros(5)
        self.b = np.zeros(5)
        self.b[0] = 1.0

        self.a[0] = 1.0
        self.a[1] = (box.Ql + h*driver.Qts)/(np.sqrt(h) * box.Ql * driver.Qts)
        self.a[2] = (h + (c + 1 + h**2) * driver.Qts * box.Ql) / (
            h * driver.Qts * box.Ql)
        self.a[3] = (h*box.Ql + driver.Qts)/(np.sqrt(h) * driver.Qts * box.Ql)
        self.a[4] = 1.0

    def f_3(self):
        A1 = self.a[1]**2 - 2.0*self.a[2]
        A2 = self.a[2]**2 + 2.0 - 2*self.a[1]*self.a[3]
        A3 = self.a[3]**2 - 2.0*self.a[2]
        d_poly = np.poly1d([1.0, -A1, -A2, -A3, -1.0])
        roots = d_poly.r
        d = np.abs(roots[2])
        f3 = np.sqrt(d) * self.f_0
        return f3

    def frequency_response(self, f_min=20.0, f_max=300.0):
        """ Calculate frequency response of the speaker (box/driver combination)

        Calculate system response of a certain driver in a vented box,
        according to Small [1]_.

        Parameters
        ----------
        f_min :
            Lower frequency
        f_max :
            Upper frequency

        EReturns
        -------
        freqs : ndarray
            the frequencies at which h was computed
        amplitude : ndarray
            the frequency response

        References
        ----------
        .. [1] Richard H. Small, "Vented-Box Loudspeaker Systems -- Part I"
        """
        start = np.log10(2*np.pi*f_min)
        stop = np.log10(2*np.pi*f_max)
        frequencies = np.logspace(start, stop, num=100)
        a = self.a
        b = self.b
        b[0] *= self.T_0**4

        a[0] *= self.T_0**4
        a[1] *= self.T_0**3
        a[2] *= self.T_0**2
        a[3] *= self.T_0

        w, h = signal.freqs(b, a, worN=frequencies)
        freqs = w / (2*np.pi)
        amplitude = 20.0*np.log10(h)
        return (freqs, amplitude)

    def displacement(self, f_min=20.0, f_max=300.0):
        start = np.log10(2*np.pi*f_min)
        stop = np.log10(2*np.pi*f_max)
        frequencies = np.logspace(start, stop, num=100)

        a = self.a

        a[0] *= self.T_0**4
        a[1] *= self.T_0**3
        a[2] *= self.T_0**2
        a[3] *= self.T_0

        b2 = np.zeros(5)
        b2[2] = self.box.Tb**2
        b2[3] = self.box.Tb / self.box.Ql
        b2[4] = 1.0

        w, displacement = signal.freqs(b2, a, worN=frequencies)
        freqs = w / (2*np.pi)
        return (freqs, np.abs(np.real(displacement)))

    def step_response(self):
        a = self.a
        b = self.b
        b[0] *= self.T_0**4

        a[0] *= self.T_0**4
        a[1] *= self.T_0**3
        a[2] *= self.T_0**2
        a[3] *= self.T_0

        system = signal.lti(b, a)
        return system.step(N=1000)

    def reference_efficiency(self):
        f3 = self.f_3()
        factor = 4.0*np.pi**2 / (air.C**3)
        v_ratio = self.driver.Vas / self.box.Vab
        tuning_ratio = self.driver.fs / f3
        k_eta = factor * v_ratio * tuning_ratio**3 / self.driver.Qes
        return k_eta * f3**3 * self.box.Vab
