# -*- coding: utf-8 -*-
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import pickle
import os
import sys
import shutil

from driver import Driver

# generate altay config dir if if does not exist;
# under Unix '~/.local/share/data/altay'
data_dir = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DataLocation)
altay_config_dir = os.path.join(data_dir[:-1], 'altay')
try: 
    os.makedirs(altay_config_dir)
except OSError:
    if not os.path.isdir(altay_config_dir):
        raise

# check if local driver database exists; if not copy it from altay source dir
local_db_fname = os.path.join(altay_config_dir, 'driver_db.ddb')
if not os.path.isfile(local_db_fname):
    altay_bin_dir = os.path.dirname(sys.argv[0])
    included_db_fname = os.path.join(altay_bin_dir, 'driver_db.ddb')
    shutil.copy(included_db_fname, local_db_fname)

with open(local_db_fname, 'rb') as f:
    driver_db = pickle.load(f)

manufacturers = set()
for driver in driver_db:      
    manufacturers.add(driver.manufacturer)

class DriverDatabaseFrame(QtGui.QWidget):
    """ Display, sort, filter, etc the database of availabe drive units """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.table_widget = QtGui.QTableWidget(self)
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ["Manufacturer", "Model", "Fs [Hz]", u"Vas [m³]", u"Sd [m²]", "Qts",
             "xmax [mm]"])

        # populate table
        for driver in driver_db:
            self.add_driver_entry(driver)

        add_driver_button = QtGui.QPushButton(self)
        add_driver_button.setIcon(QtGui.QIcon.fromTheme('list-add'))
        add_driver_button.setText("Add new driver")
        add_driver_button.clicked.connect(self.add_driver)
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(add_driver_button, stretch=0)
        vbox.addWidget(self.table_widget)
        self.setLayout(vbox)

    def add_driver(self):
        add_driver_dialog = QtGui.QDialog()

        # Driver general specification
        general_info = QtGui.QGroupBox("General Specification")
        info_form = QtGui.QFormLayout()
        info_form.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)

        manuf_label = QtGui.QLabel()
        manuf_label.setText("Manufacturer")
        manuf_line = QtGui.QLineEdit()

        model_label = QtGui.QLabel()
        model_label.setText("Model")
        model_line = QtGui.QLineEdit()
        
        info_form.addRow(manuf_label, manuf_line)
        info_form.addRow(model_label, model_line)
        general_info.setLayout(info_form)

        # Thiele/Small parameters
        ts_info = QtGui.QGroupBox("Thiele/Small Parameters")
        ts_form = QtGui.QFormLayout()

        fs_label = QtGui.QLabel()
        fs_label.setText("Resonance Frequency: fs")
        fs_box = QtGui.QDoubleSpinBox()
        fs_box.setSuffix(" Hz")
        fs_box.setRange(10.0, 2e4)

        Qts_label = QtGui.QLabel()
        Qts_label.setText("Total Q of Driver at fs: Qts")
        Qts_box = QtGui.QDoubleSpinBox()
        Qts_box.setRange(0.0, 1.0)

        Sd_label = QtGui.QLabel()
        Sd_label.setText("Diaphragm Area: Sd")
        Sd_box = QtGui.QDoubleSpinBox()
        Sd_box.setSuffix(u" cm²")
        Sd_box.setRange(0.0, 1e3)

        xmax_label = QtGui.QLabel()
        xmax_label.setText("Maximum linear peak excursion: xmax")
        xmax_box = QtGui.QDoubleSpinBox()
        xmax_box.setSuffix(" mm")
        xmax_box.setRange(0.0, 20.0)

        Vas_label = QtGui.QLabel()
        Vas_label.setText("Equivalent Compliance Volume: Vas")
        Vas_box = QtGui.QDoubleSpinBox()
        Vas_box.setSuffix(" l")
        Vas_box.setRange(0.0, 1e3)
        
        ts_form.addRow(fs_label, fs_box)
        ts_form.addRow(Qts_label, Qts_box)
        ts_form.addRow(Sd_label, Sd_box)
        ts_form.addRow(xmax_label, xmax_box)
        ts_form.addRow(Vas_label, Vas_box)
        ts_info.setLayout(ts_form)

        # Accept/cancel buttons
        buttons_hbox = QtGui.QHBoxLayout()
        accept_button = QtGui.QPushButton(self)
        accept_button.setIcon(QtGui.QIcon.fromTheme('dialog-apply'))
        accept_button.setText("Accept")
        cancel_button = QtGui.QPushButton(self)
        cancel_button.setIcon(QtGui.QIcon.fromTheme('gtk-close'))
        cancel_button.setText("Cancel")
        buttons_hbox.addWidget(cancel_button)
        buttons_hbox.addWidget(accept_button)

        # putting it together
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(general_info)
        vbox.addWidget(ts_info)
        vbox.addLayout(buttons_hbox)
        add_driver_dialog.setLayout(vbox)
        add_driver_dialog.exec_()

    def add_driver_entry(self, driver):
        """ Add a new driver entry to the QTableWidget """
        rows = self.table_widget.rowCount()
        self.table_widget.setRowCount(rows+1)

        items = []
        items.append(QtGui.QTableWidgetItem(driver.manufacturer))
        items.append(QtGui.QTableWidgetItem(driver.model))
        items.append(QtGui.QTableWidgetItem(str(driver.fs)))
        items.append(QtGui.QTableWidgetItem(str(driver.Vas)))
        items.append(QtGui.QTableWidgetItem(str(driver.Sd)))
        items.append(QtGui.QTableWidgetItem(str(driver.Qts)))
        items.append(QtGui.QTableWidgetItem(str(driver.xmax)))

        for i, item in enumerate(items):
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.table_widget.setItem(rows, i, item)
