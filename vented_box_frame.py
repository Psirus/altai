""" Calculate and plot the frequency response of box/driver combinations """
# Matplotlib setup
import matplotlib as mpl
mpl.use('Qt4Agg')
mpl.rcParams['backend.qt4'] = 'PySide'
mpl.rcParams['lines.linewidth'] = 2.0
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import matplotlib.figure as figure
# system imports
import numpy as np
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import scipy.signal as signal
# altay imports
from driver_selection_group import DriverSelectionGroup
from vented_box import VentedBox


def get_response(driver, box):
    """ Calculate system response of box and driver combination

    Calculate system response of a certain driver in a vented box, according
    to Small [1]_.

    Parameters
    ----------
    driver : Driver
        Driver to be used
    box : VentedBox
        Box to be used

    Returns
    -------
    w : ndarray
        the angular frequencies at which h was computed
    h : ndarray
        the frequency response

    References
    ----------
    .. [1] Richard H. Small, "Vented-Box Loudspeaker Systems -- Part I"
    """

    a = np.zeros(5)
    b = np.zeros(5)

    # Response parameters
    T_0 = np.sqrt(driver.Ts * box.Tb)
    # tuning ratio
    h = driver.Ts / box.Tb
    # compliance ratio
    c = driver.Cas / box.Cab

    b[0] = T_0**4

    a[0] = T_0**4
    a[1] = T_0**3 * (box.Ql + h*driver.Qts)/(np.sqrt(h) * box.Ql * driver.Qts)
    a[2] = T_0**2 * (h + (c + 1 + h**2) * driver.Qts * box.Ql) / (
        h * driver.Qts * box.Ql)
    a[3] = T_0 * (h*box.Ql + driver.Qts) / (np.sqrt(h) * driver.Qts * box.Ql)
    a[4] = 1.0

    start = np.log10(2*np.pi*20.0)
    stop = np.log10(2*np.pi*300.0)
    frequencies = np.logspace(start, stop, num=100)
    w, h = signal.freqs(b, a, worN=frequencies)
    return (w, h)


class VentedBoxFrame(QtGui.QWidget):
    """ Predict frequency response of vented boxes according to Thiele & Small

    This is one of the main tabs of the application atm. You can choose your
    box size and tuning, select a driver and it will plot the frequency
    response of this combination.

    The button "Freeze and Compare" keeps the current response and adds a new
    one, whose parameters can be modified.
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Initialize plot
        self.fig = figure.Figure((5.0, 4.0))
        bg_color = self.palette().color(QtGui.QPalette.Window).getRgbF()
        self.fig.set_facecolor(bg_color)
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.amplitude_axes = self.fig.add_subplot(111)
        self.amplitude_line, = self.amplitude_axes.semilogx(100.0, 0.0)
        self.set_plot_options()
        self.canvas.draw()

        # Box parameter setup
        box_param_group = QtGui.QGroupBox("Box Parameters")
        box_param_form = QtGui.QFormLayout(self)
        box_param_form.setFieldGrowthPolicy(
            QtGui.QFormLayout.FieldsStayAtSizeHint)
        box_volume_label = QtGui.QLabel(self)
        box_volume_label.setText("Box Volume")
        box_volume_spinbox = QtGui.QDoubleSpinBox(self)
        box_volume_spinbox.setSuffix(" l")
        box_volume_spinbox.setRange(10.0, 400.0)
        box_fb_label = QtGui.QLabel(self)
        box_fb_label.setText("Box Tuning Frequency")
        box_fb_spinbox = QtGui.QDoubleSpinBox(self)
        box_fb_spinbox.setSuffix(" Hz")
        box_fb_spinbox.setRange(20.0, 200.0)
        box_ql_label = QtGui.QLabel(self)
        box_ql_label.setText("Box Leakage Losses Ql")
        box_ql_spinbox = QtGui.QDoubleSpinBox(self)
        box_ql_spinbox.setRange(2.0, 100.0)
        box_param_form.addRow(box_volume_label, box_volume_spinbox)
        box_param_form.addRow(box_fb_label, box_fb_spinbox)
        box_param_form.addRow(box_ql_label, box_ql_spinbox)
        box_param_group.setLayout(box_param_form)

        qb3_box = VentedBox(Vab=0.022, fb=55.3, Ql=20.0)
        self.current_box = qb3_box
        box_volume_spinbox.setValue(1e3*self.current_box.Vab)
        box_volume_spinbox.valueChanged.connect(self.change_box_size)
        box_fb_spinbox.setValue(self.current_box.fb)
        box_fb_spinbox.valueChanged.connect(self.change_box_fb)
        box_ql_spinbox.setValue(self.current_box.Ql)
        box_ql_spinbox.valueChanged.connect(self.change_box_ql)

        self.driver_selection = DriverSelectionGroup()
        self.driver_selection.driver_changed.connect(self.driver_changed)
        self.current_driver = self.driver_selection.current_driver
        self.update_response()

        # Assemble main view
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(box_param_group)
        hbox.addWidget(self.driver_selection)

        compare_button = QtGui.QPushButton("Freeze and Compare", self)
        compare_button.clicked.connect(self.add_new_response)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(compare_button, alignment=QtCore.Qt.AlignHCenter)
        vbox.addWidget(self.canvas, stretch=1)
        self.setLayout(vbox)

    def change_box_size(self, volume):
        """ Change box size and update response plot """
        self.current_box.Vab = 1e-3*volume
        self.update_response()

    def change_box_fb(self, fb):
        """ Change box tuning and update response plot """
        self.current_box.fb = fb
        self.update_response()

    def change_box_ql(self, Ql):
        """ Change box losses and update response plot """
        self.current_box.Ql = Ql
        self.update_response()

    def driver_changed(self, driver):
        """ Update response when selected driver changes """
        self.current_driver = driver
        self.update_response()

    def update_response(self):
        """ Update the response plot """
        w, h = get_response(self.current_driver, self.current_box)
        self.amplitude_line.set_xdata(w/(2*np.pi))
        self.amplitude_line.set_ydata(20*np.log10(abs(h)))
        manufacturer = self.current_driver.manufacturer
        model = self.current_driver.model
        box_volume = 1e3*self.current_box.Vab
        box_tuning = self.current_box.fb
        label = '{0} {1} in {2:2g}l / {3}Hz'.format(
            manufacturer, model, box_volume, box_tuning)
        self.amplitude_line.set_label(label)
        self.amplitude_axes.legend(loc='lower right')
        self.canvas.draw()

    def add_new_response(self):
        """ Add an additional response to the plot """
        w, h = get_response(self.current_driver, self.current_box)
        self.amplitude_line, = self.amplitude_axes.semilogx(
            w/(2*np.pi), 20*np.log10(abs(h)))
        manufacturer = self.current_driver.manufacturer
        model = self.current_driver.model
        box_volume = 1e3*self.current_box.Vab
        box_tuning = self.current_box.fb
        label = '{0} {1} in {2:2g}l / {3}Hz'.format(
            manufacturer, model, box_volume, box_tuning)
        self.amplitude_line.set_label(label)
        self.amplitude_axes.legend(loc='lower right')
        self.set_plot_options()
        self.canvas.draw()

    def set_plot_options(self):
        """ Set the appearance of the plot """
        # Axis limits and grid
        self.amplitude_axes.set_xlim(20, 300)
        self.amplitude_axes.set_ylim(-36, 6)
        self.amplitude_axes.grid(True, which='both')

        # x-ticks
        ticks = [30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 250]
        ticklabels = [str(x) for x in ticks]
        self.amplitude_axes.set_xticks(ticks)
        self.amplitude_axes.set_xticklabels(ticklabels)

        # y-ticks
        multiples_of_six = mpl.ticker.MultipleLocator(6)
        multiples_of_three = mpl.ticker.MultipleLocator(3)
        self.amplitude_axes.yaxis.set_major_locator(multiples_of_six)
        self.amplitude_axes.yaxis.set_minor_locator(multiples_of_three)

        # Titles and labels
        self.amplitude_axes.set_title("Frequency Response")
        self.amplitude_axes.set_xlabel("Frequency [Hz]")
        self.amplitude_axes.set_ylabel("Amplitude [dB]")
