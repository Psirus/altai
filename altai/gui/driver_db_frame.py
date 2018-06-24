# -*- coding: utf-8 -*-
"""Display the driver database as a table."""
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from . import config
from ..lib.driver import Driver


class DriverDatabaseFrame(QtGui.QWidget):
    """Display, sort, filter, etc the database of availabe drive units."""

    new_manufacturer_added = QtCore.Signal(set)

    def __init__(self):
        """Initialize database frame."""
        QtGui.QWidget.__init__(self)

        self.table_widget = QtGui.QTableWidget(self)
        self.table_widget.setSortingEnabled(True)
        labels = ["Manufacturer", "Model", "d [in]", "Fs [Hz]", u"Vas [m³]",
                  u"Sd [m²]", "Qts", "Qes", "xmax [mm]", "m [kg]", 
                  "P (AES) [W]"]
        self.table_widget.setColumnCount(len(labels))
        self.table_widget.setHorizontalHeaderLabels(labels)

        # populate table
        for driver in config.driver_db:
            self.add_driver_entry(driver)

        add_driver_button = QtGui.QPushButton(self)
        add_driver_button.setIcon(QtGui.QIcon.fromTheme('list-add'))
        add_driver_button.setText("Add new driver")
        add_driver_button.clicked.connect(self.add_driver)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(add_driver_button, stretch=0)
        vbox.addWidget(self.table_widget)
        self.setLayout(vbox)

    def add_driver_entry(self, driver):
        """Add a new driver entry to the QTableWidget.

        Args:
            driver : driver to add to the table
        """
        rows = self.table_widget.rowCount()
        self.table_widget.setRowCount(rows+1)

        items = []
        items.append(QtGui.QTableWidgetItem(driver.manufacturer))
        items.append(QtGui.QTableWidgetItem(driver.model))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.diameter)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.fs)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.Vas)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.Sd)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.Qts)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.Qes)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(1e3*driver.xmax)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.weight)))
        items.append(QtGui.QTableWidgetItem("{0:4g}".format(driver.power)))

        for i, item in enumerate(items):
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(rows, i, item)

    def add_driver(self):
        """Dialog for adding a new driver to the database."""
        self.add_driver_dialog = QtGui.QDialog()

        # Driver general specification
        general_info = QtGui.QGroupBox("General Specification")
        info_form = QtGui.QFormLayout()
        info_form.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)

        manuf_label = QtGui.QLabel()
        manuf_label.setText("Manufacturer")
        self.manuf_line = QtGui.QLineEdit()

        model_label = QtGui.QLabel()
        model_label.setText("Model")
        self.model_line = QtGui.QLineEdit()

        diameter_label = QtGui.QLabel()
        diameter_label.setText("Diameter")
        self.diameter_box = QtGui.QDoubleSpinBox()
        self.diameter_box.setSuffix(' "')
        self.diameter_box.setRange(0.5, 40.0)

        weight_label = QtGui.QLabel()
        weight_label.setText("Net Weight")
        self.weight_box = QtGui.QDoubleSpinBox()
        self.weight_box.setSuffix(" kg")
        self.weight_box.setRange(0.1, 40.0)

        power_label = QtGui.QLabel()
        power_label.setText("AES Power Handling")
        self.power_box = QtGui.QDoubleSpinBox()
        self.power_box.setSuffix(" W")
        self.power_box.setRange(1.0, 4000.0)

        info_form.addRow(manuf_label, self.manuf_line)
        info_form.addRow(model_label, self.model_line)
        info_form.addRow(diameter_label, self.diameter_box)
        info_form.addRow(weight_label, self.weight_box)
        info_form.addRow(power_label, self.power_box)
        general_info.setLayout(info_form)

        # Thiele/Small parameters
        ts_info = QtGui.QGroupBox("Thiele/Small Parameters")
        ts_form = QtGui.QFormLayout()

        fs_label = QtGui.QLabel()
        fs_label.setText("Resonance Frequency: fs")
        self.fs_box = QtGui.QDoubleSpinBox()
        self.fs_box.setSuffix(" Hz")
        self.fs_box.setRange(10.0, 2e4)

        Qts_label = QtGui.QLabel()
        Qts_label.setText("Total Q of Driver at fs: Qts")
        self.Qts_box = QtGui.QDoubleSpinBox()
        self.Qts_box.setRange(0.0, 1.0)

        Sd_label = QtGui.QLabel()
        Sd_label.setText("Diaphragm Area: Sd")
        self.Sd_box = QtGui.QDoubleSpinBox()
        self.Sd_box.setSuffix(u" cm²")
        self.Sd_box.setRange(0.0, 1e3)

        xmax_label = QtGui.QLabel()
        xmax_label.setText("Maximum linear peak excursion: xmax")
        self.xmax_box = QtGui.QDoubleSpinBox()
        self.xmax_box.setSuffix(" mm")
        self.xmax_box.setRange(0.0, 20.0)

        Vas_label = QtGui.QLabel()
        Vas_label.setText("Equivalent Compliance Volume: Vas")
        self.Vas_box = QtGui.QDoubleSpinBox()
        self.Vas_box.setSuffix(" l")
        self.Vas_box.setRange(0.0, 1e3)

        ts_form.addRow(fs_label, self.fs_box)
        ts_form.addRow(Qts_label, self.Qts_box)
        ts_form.addRow(Sd_label, self.Sd_box)
        ts_form.addRow(xmax_label, self.xmax_box)
        ts_form.addRow(Vas_label, self.Vas_box)
        ts_info.setLayout(ts_form)

        # Accept/cancel buttons
        buttons_hbox = QtGui.QHBoxLayout()
        accept_button = QtGui.QPushButton(self)
        accept_button.setIcon(QtGui.QIcon.fromTheme('dialog-apply'))
        accept_button.setText("Accept")
        accept_button.clicked.connect(self.write_driver_to_db)
        cancel_button = QtGui.QPushButton(self)
        cancel_button.setIcon(QtGui.QIcon.fromTheme('gtk-close'))
        cancel_button.setText("Cancel")
        cancel_button.clicked.connect(self.add_driver_dialog.reject)
        buttons_hbox.addWidget(cancel_button)
        buttons_hbox.addWidget(accept_button)

        # putting it together
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(general_info)
        vbox.addWidget(ts_info)
        vbox.addLayout(buttons_hbox)
        self.add_driver_dialog.setLayout(vbox)
        self.add_driver_dialog.exec_()

    def write_driver_to_db(self):
        """Add the newly created driver to the database."""
        new_driver = Driver(self.manuf_line.text(), self.model_line.text())
        new_driver.diameter = self.diameter_box.value()
        new_driver.power = self.power_box.value()
        new_driver.weight = self.weight_box.value()
        new_driver.fs = self.fs_box.value()
        new_driver.Vas = self.Vas_box.value()/1e3  # l to m³
        new_driver.Qts = self.Qts_box.value()
        new_driver.Sd = self.Sd_box.value()/1e4  # cm² to m²
        new_driver.xmax = self.xmax_box.value()/1e3  # mm to m

        config.driver_db.append(new_driver)
        config.driver_db.write_to_disk(config.local_db_fname)
        self.add_driver_entry(new_driver)

        if new_driver.manufacturer not in config.driver_db.manufacturers:
            config.driver_db.manufacturers.add(new_driver.manufacturer)
            self.new_manufacturer_added.emit(config.driver_db.manufacturers)
        self.add_driver_dialog.accept()
