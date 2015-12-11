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

        for driver in driver_db:
            self.add_driver(driver)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.table_widget)
        self.setLayout(vbox)

    def add_driver(self, driver):
        """ Add a new driver to the QTableWidget """
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
