import PySide.QtGui as QtGui
from driver import Driver

bc15sw115 = Driver("B&C Speakers", "15SW115")
bc15sw115.set_fs(35.0)
bc15sw115.set_Vas(0.11)
bc15sw115.set_Qts(0.24)
bc15sw115.set_Sd(0.0855)

eighteen15nlw9401 = Driver("Eighteen Sound", "15NLW9401")
eighteen15nlw9401.set_fs(39.0)
eighteen15nlw9401.set_Vas(0.134)
eighteen15nlw9401.set_Qts(0.26)
eighteen15nlw9401.set_Sd(0.09)

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
            "Fs [Hz]", u"Vas [m³]", u"Sd [m²]", "Qts"])


        for driver in driver_db:
            self.addDriver(driver)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.tableWidget)
        self.setLayout(vbox)

    def addDriver(self, driver):
        rows = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rows+1)

        manuf = QtGui.QTableWidgetItem(driver.manufacturer)
        model = QtGui.QTableWidgetItem(driver.model)
        Fs    = QtGui.QTableWidgetItem(str(driver.Fs))
        Vas   = QtGui.QTableWidgetItem(str(driver.Vas))
        Sd    = QtGui.QTableWidgetItem(str(driver.Sd))
        Qts   = QtGui.QTableWidgetItem(str(driver.Qts))

        self.tableWidget.setItem(rows, 0, manuf)
        self.tableWidget.setItem(rows, 1, model)
        self.tableWidget.setItem(rows, 2, Fs)
        self.tableWidget.setItem(rows, 3, Vas)
        self.tableWidget.setItem(rows, 4, Sd)
        self.tableWidget.setItem(rows, 5, Qts)

