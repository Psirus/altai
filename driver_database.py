import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from driver import Driver

bc15sw115     = Driver("B&C Speakers", "15SW115")
bc15sw115.fs  = 35.0
bc15sw115.Vas = 0.11
bc15sw115.Qts = 0.24
bc15sw115.Sd  = 0.0855

eighteen15nlw9401     = Driver("Eighteen Sound", "15NLW9401")
eighteen15nlw9401.fs  = 39.0
eighteen15nlw9401.Vas = 0.134
eighteen15nlw9401.Qts = 0.26
eighteen15nlw9401.Sd  = 0.09

driver_db = [bc15sw115, eighteen15nlw9401]

manufacturers = set()
for driver in driver_db:      
    manufacturers.add(driver.manufacturer)

class DriverDatabaseFrame(QtGui.QWidget):
    """ Display, sort, filter, etc the database of availabe drive units """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.tableWidget = QtGui.QTableWidget(self)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["Manufacturer", "Model", 
            "Fs [Hz]", "Vas [m³]", "Sd [m²]", "Qts"])

        for driver in driver_db:
            self.addDriver(driver)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tableWidget)
        self.setLayout(vbox)

    def addDriver(self, driver):
        rows = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rows+1)

        items = []
        items.append(QtGui.QTableWidgetItem(driver.manufacturer))
        items.append(QtGui.QTableWidgetItem(driver.model))
        items.append(QtGui.QTableWidgetItem(str(driver.fs)))
        items.append(QtGui.QTableWidgetItem(str(driver.Vas)))
        items.append(QtGui.QTableWidgetItem(str(driver.Sd)))
        items.append(QtGui.QTableWidgetItem(str(driver.Qts)))

        for i, item in enumerate(items):
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            self.tableWidget.setItem(rows, i, item)

