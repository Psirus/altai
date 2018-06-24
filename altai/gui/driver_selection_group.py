""" Group from which to select manufacturer and model """
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
from . import config
from ..lib.driver import Driver


class DriverSelectionGroup(QtGui.QGroupBox):
    """ Group from which to select manufacturer and model """

    driver_changed = QtCore.Signal(Driver)

    def __init__(self):
        # Driver selection setup
        QtGui.QGroupBox.__init__(self, "Driver Selection")
        driver_selection_form = QtGui.QFormLayout(self)
        driver_selection_form.setFieldGrowthPolicy(
            QtGui.QFormLayout.FieldsStayAtSizeHint)

        driver_manuf_label = QtGui.QLabel(self)
        driver_manuf_label.setText("Manufacturer")
        self.driver_manuf_box = QtGui.QComboBox(self)
        self.driver_manuf_box.activated.connect(self.set_manufacturer)

        driver_model_label = QtGui.QLabel(self)
        driver_model_label.setText("Model")
        self.driver_model_box = QtGui.QComboBox(self)
        self.driver_model_box.activated.connect(self.change_driver)

        for manufacturer in config.driver_db.manufacturers:
            self.driver_manuf_box.addItem(manufacturer)
        self.current_manuf = self.driver_manuf_box.currentText()
        for driver in config.driver_db:
            if driver.manufacturer == self.current_manuf:
                self.driver_model_box.addItem(driver.model)
        self.current_model = self.driver_model_box.currentText()
        for driver in config.driver_db:
            if ((self.current_model == driver.model) and
                    (self.current_manuf == driver.manufacturer)):
                self.current_driver = driver

        driver_selection_form.addRow(driver_manuf_label, self.driver_manuf_box)
        driver_selection_form.addRow(driver_model_label, self.driver_model_box)
        self.setLayout(driver_selection_form)

    def update_drivers(self, manufacturers):
        """ When manufacturer is added to DB, update the comboboxes in this
        group """
        self.driver_manuf_box.clear()
        for manufacturer in manufacturers:
            self.driver_manuf_box.addItem(manufacturer)
        self.set_manufacturer(0)

    def set_manufacturer(self, index):
        """ Change manufacturer, repopulate model box and emit driver change
            signal"""
        self.current_manuf = self.driver_manuf_box.itemText(index)
        self.driver_model_box.clear()
        for driver in config.driver_db:
            if driver.manufacturer == self.current_manuf:
                self.driver_model_box.addItem(driver.model)
        self.change_driver()

    def change_driver(self):
        """ A new driver is selected; emit signal containing the currently
        selected driver """
        self.current_manuf = self.driver_manuf_box.currentText()
        self.current_model = self.driver_model_box.currentText()
        for driver in config.driver_db:
            if ((self.current_model == driver.model) and
                    (self.current_manuf == driver.manufacturer)):
                self.current_driver = driver
        self.driver_changed.emit(self.current_driver)
