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
        self.f_0 = 1.0 / (2.0 * np.pi * self.T_0)
        # tuning ratio
        h = driver.Ts / box.Tb
        # compliance ratio
        c = driver.Cas / box.Cab

        self._a = np.zeros(5)
        self._b = np.zeros(5)
        self._b[0] = self.T_0 ** 4

        self._a[0] = self.T_0 ** 4
        self._a[1] = (
            self.T_0 ** 3
            * (box.Ql + h * driver.Qts)
            / (np.sqrt(h) * box.Ql * driver.Qts)
        )
        self._a[2] = (
            self.T_0 ** 2
            * (h + (c + 1 + h ** 2) * driver.Qts * box.Ql)
            / (h * driver.Qts * box.Ql)
        )
        self._a[3] = (
            self.T_0 * (h * box.Ql + driver.Qts) / (np.sqrt(h) * driver.Qts * box.Ql)
        )
        self._a[4] = 1.0

        self._system = signal.lti(self._b, self._a)

    def f_3(self):
        A1 = (self._a[1] / self.T_0 ** 3) ** 2 - 2.0 * self._a[2] / self.T_0 ** 2
        A2 = (
            (self._a[2] / self.T_0 ** 2) ** 2
            + 2.0
            - 2 * self._a[1] * self._a[3] / self.T_0 ** 4
        )
        A3 = (self._a[3] / self.T_0) ** 2 - 2.0 * self._a[2] / self.T_0 ** 2
        d_poly = np.poly1d([1.0, -A1, -A2, -A3, -1.0])
        roots = d_poly.r
        d = np.abs(roots[2])
        f3 = np.sqrt(d) * self.f_0
        return f3

    def frequency_response(self, f_min=20.0, f_max=300.0):
        """Calculate frequency response of the speaker (box/driver combination)

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
        start = np.log10(2 * np.pi * f_min)
        stop = np.log10(2 * np.pi * f_max)
        frequencies = np.logspace(start, stop, num=100)

        w, h = self._system.freqresp(w=frequencies)
        freqs = w / (2 * np.pi)
        amplitude = 20.0 * np.log10(np.abs(h))
        return (freqs, amplitude)

    def displacement(self, f_min=20.0, f_max=300.0):
        start = np.log10(2 * np.pi * f_min)
        stop = np.log10(2 * np.pi * f_max)
        frequencies = np.logspace(start, stop, num=50)

        b2 = np.zeros(5)
        b2[2] = self.box.Tb ** 2
        b2[3] = self.box.Tb / self.box.Ql
        b2[4] = 1.0

        w, displacement = signal.freqs(b2, self._a, worN=frequencies)
        freqs = w / (2 * np.pi)
        return (freqs, np.abs(np.real(displacement)))

    def step_response(self):
        return self._system.step(N=200)

    def reference_efficiency(self):
        f3 = self.f_3()
        factor = 4.0 * np.pi ** 2 / (air.C ** 3)
        v_ratio = self.driver.Vas / self.box.Vab
        tuning_ratio = self.driver.fs / f3
        k_eta = factor * v_ratio * tuning_ratio ** 3 / self.driver.Qes
        return k_eta * f3 ** 3 * self.box.Vab

    def displacement_limited_output(self):
        P_ar = 3.0 * self.f_3() ** 4.0 * self.driver.Vd ** 2.0
        print(P_ar)
        return 112.0 + 10.0 * np.log10(P_ar)
