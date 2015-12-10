# Matplotlib setup
import matplotlib as mpl
mpl.use('Qt4Agg')
mpl.rcParams['backend.qt4'] = 'PySide'
mpl.rcParams['lines.linewidth'] = 2.0
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.figure as figure
# system imports
import numpy as np
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import scipy.signal as signal
# altay imports
from driver_database import driver_db, manufacturers
from vented_box import VentedBox

def get_response(driver, box):
    """ Calculate system response of box and driver combination """

    a = np.zeros(5)
    b = np.zeros(5)
    b[0] = 1.0

    # Response parameters
    a[0] = 1.0
    a[1] = 1/(driver.Qts * driver.Ts)
    a[2] = 1/driver.Ts**2 + 1/box.Tb**2 + driver.Cas/(box.Cab*driver.Ts**2)
    a[3] = 1/(box.Tb**2*driver.Ts*driver.Qts)
    a[4] = 1/(driver.Ts**2*box.Tb**2)

    frequencies = np.logspace(np.log10(2*np.pi*20), np.log10(2*np.pi*300), num=100)
    w, h = signal.freqs(b, a, worN=frequencies)
    return (w, h)

class VentedBoxFrame(QtGui.QWidget):
    """ Predict frequency response of vented boxes according to Thiele & Small """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Initialize plot
        self.fig = figure.Figure((5.0, 4.0))
        bg_color = self.palette().color(QtGui.QPalette.Window).getRgbF()
        self.fig.set_facecolor(bg_color)
        self.canvas = FigureCanvas(self.fig)
        self.amplitude_axes = self.fig.add_subplot(111)
        self.amplitude_line, = self.amplitude_axes.semilogx(100.0, 0.0)
        self.set_plot_options()
        self.canvas.draw()

        # Box parameter setup
        box_param_group = QtGui.QGroupBox("Box Parameters")
        box_param_hbox = QtGui.QFormLayout(self)
        box_param_hbox.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
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
        box_param_hbox.addRow(box_volume_label, box_volume_spinbox)
        box_param_hbox.addRow(box_fb_label, box_fb_spinbox)
        box_param_group.setLayout(box_param_hbox)

        qb3_box = VentedBox(Vab=0.022, fb=55.3)
        self.current_box = qb3_box
        box_volume_spinbox.setValue(1e3*self.current_box.Vab)
        box_volume_spinbox.valueChanged.connect(self.change_box_size)
        box_fb_spinbox.setValue(self.current_box.fb)
        box_fb_spinbox.valueChanged.connect(self.change_box_fb)

        # Driver selection setup
        driver_selection = QtGui.QGroupBox("Driver Selection")
        driver_selection_form = QtGui.QFormLayout(self)
        driver_selection_form.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)

        driver_manuf_label = QtGui.QLabel(self)
        driver_manuf_label.setText("Manufacturer")
        self.driver_manuf_box = QtGui.QComboBox(self)
        for manufacturer in manufacturers:
            self.driver_manuf_box.addItem(manufacturer)
        self.driver_manuf_box.activated.connect(self.set_manufacturer)
        current_manuf_index = self.driver_manuf_box.currentIndex()
        self.current_manuf = self.driver_manuf_box.itemText(current_manuf_index)

        driver_model_label = QtGui.QLabel(self)
        driver_model_label.setText("Model")
        self.driver_model_box = QtGui.QComboBox(self)
        self.driver_model_box.currentIndexChanged.connect(self.set_model)
        self.update_model_box()
        current_model_index = self.driver_model_box.currentIndex()
        self.current_model = self.driver_model_box.itemText(current_model_index)
        for driver in driver_db:
            if ((self.current_model == driver.model)
                    and (self.current_manuf == driver.manufacturer)):
                self.current_driver = driver

        driver_selection_hbox.addRow(driver_manuf_label, self.driver_manuf_box)
        driver_selection_hbox.addRow(driver_model_label, self.driver_model_box)
        driver_selection.setLayout(driver_selection_hbox)

        # Assemble main view
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(box_param_group)
        hbox.addWidget(driver_selection)

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

    def set_manufacturer(self, index):
        """ Change manufacturer and update driver models"""
        self.current_manuf = self.driver_manuf_box.itemText(index)
        self.update_model_box()

    def update_model_box(self):
        """ Clear model list and add all models of current manufacturer"""
        self.driver_model_box.clear()
        for driver in driver_db:
            if driver.manufacturer == self.current_manuf:
                self.driver_model_box.addItem(driver.model)

    def set_model(self, index):
        """ Change driver and update response plot"""
        self.current_model = self.driver_model_box.itemText(index)
        for driver in driver_db:
            if ((self.current_model == driver.model)
                    and (self.current_manuf == driver.manufacturer)):
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
        w, h = get_response(self.current_driver, self.current_box)
        self.amplitude_line, = self.amplitude_axes.semilogx(w/(2*np.pi), 20*np.log10(abs(h)))
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
