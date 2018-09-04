""" Calculate and plot the frequency response of box/driver combinations """
# system imports
import numpy as np
import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import scipy.signal as signal
# altai imports
from .driver_selection_group import DriverSelectionGroup
from ..lib.vented_box import VentedBox
from ..lib.speaker import VentedSpeaker
# Matplotlib setup
import matplotlib as mpl
mpl.use('Qt5Agg')
mpl.rcParams['lines.linewidth'] = 2.0
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.figure as figure


class VentedBoxFrame(QtWidgets.QWidget):
    """ Predict frequency response of vented boxes according to Thiele & Small

    This is one of the main tabs of the application atm. You can choose your
    box size and tuning, select a driver and it will plot the frequency
    response of this combination.

    The button "Freeze and Compare" keeps the current response and adds a new
    one, whose parameters can be modified.
    """

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

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
        box_param_group = QtWidgets.QGroupBox("Box Parameters")
        box_param_form = QtWidgets.QFormLayout(self)
        box_param_form.setFieldGrowthPolicy(
            QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        box_volume_label = QtWidgets.QLabel(self)
        box_volume_label.setText("Box Volume")
        box_volume_spinbox = QtWidgets.QDoubleSpinBox(self)
        box_volume_spinbox.setSuffix(" l")
        box_volume_spinbox.setRange(10.0, 400.0)
        box_fb_label = QtWidgets.QLabel(self)
        box_fb_label.setText("Box Tuning Frequency")
        box_fb_spinbox = QtWidgets.QDoubleSpinBox(self)
        box_fb_spinbox.setSuffix(" Hz")
        box_fb_spinbox.setRange(20.0, 200.0)
        box_ql_label = QtWidgets.QLabel(self)
        box_ql_label.setText("Box Leakage Losses Ql")
        box_ql_spinbox = QtWidgets.QDoubleSpinBox(self)
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
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(box_param_group)
        hbox.addWidget(self.driver_selection)

        compare_button = QtWidgets.QPushButton("Freeze and Compare", self)
        compare_button.clicked.connect(self.add_new_response)

        vbox = QtWidgets.QVBoxLayout()
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
        speaker = VentedSpeaker(self.current_driver, self.current_box)
        freqs, amplitude, _ = speaker.frequency_response()
        self.amplitude_line.set_xdata(freqs)
        self.amplitude_line.set_ydata(amplitude)
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
        speaker = VentedSpeaker(self.current_driver, self.current_box)
        freqs, amplitude, _ = speaker.frequency_response()
        self.amplitude_line, = self.amplitude_axes.semilogx(
                freqs, amplitude)
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
