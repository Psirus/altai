# -*- coding: utf-8 -*-
import numpy as np
import PySide.QtGui as QtGui

from air import rho
from vented_box import VentedBox
from driver_database import driver_db, manufacturers

class VentDimensionsFrame(QtGui.QWidget):
    """ Find vent dimensions for given tuning """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        # Box parameter setup
        box_param_group = QtGui.QGroupBox("Box Parameters")
        box_param_form = QtGui.QFormLayout(self)
        box_param_form.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
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
        box_param_form.addRow(box_volume_label, box_volume_spinbox)
        box_param_form.addRow(box_fb_label, box_fb_spinbox)
        box_param_group.setLayout(box_param_form)

        sc4_box = VentedBox(Vab=0.09, fb=40.0)
        self.current_box = sc4_box
        box_volume_spinbox.setValue(1e3*self.current_box.Vab)
        box_volume_spinbox.valueChanged.connect(self.change_box_size)
        box_fb_spinbox.setValue(self.current_box.fb)
        box_fb_spinbox.valueChanged.connect(self.change_box_fb)

        vent_geom_group = QtGui.QGroupBox("Vent Geometry")
        vent_geom_form = QtGui.QFormLayout(self)
        vent_geom_form.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)

        # Vent radius
        vent_radius_label = QtGui.QLabel(self)
        vent_radius_label.setText("Effective Vent Radius")
        self.vent_radius_spinbox = QtGui.QDoubleSpinBox(self)
        self.vent_radius_spinbox.setSuffix(" mm")
        self.vent_radius_spinbox.setRange(0.0, 2e3)
        self.vent_radius_spinbox.setValue(25.0)
        self.vent_radius_spinbox.valueChanged.connect(self.radius_changed)

        # Vent area, just fyi
        vent_area_label = QtGui.QLabel(self)
        vent_area_label.setText("<i>Vent Area</i>")
        self.vent_area_value = QtGui.QLabel(self)
        radius = self.vent_radius_spinbox.value()
        vent_area = np.pi*radius**2
        self.vent_area_value.setText(u"{0:4g}mm²".format(vent_area))

        # Vent length
        vent_length_label = QtGui.QLabel(self)
        vent_length_label.setText("Vent Length")
        self.vent_length_spinbox = QtGui.QDoubleSpinBox(self)
        self.vent_length_spinbox.setSuffix(" mm")
        self.vent_length_spinbox.setRange(0.0, 2e3)
        length = self.find_length(1e-3*radius)
        self.vent_length_spinbox.setValue(1e3*length)
        self.vent_length_spinbox.valueChanged.connect(self.length_changed)

        vent_geom_form.addRow(vent_radius_label, self.vent_radius_spinbox)
        vent_geom_form.addRow(vent_area_label, self.vent_area_value)
        vent_geom_form.addRow(vent_length_label, self.vent_length_spinbox)
        vent_geom_group.setLayout(vent_geom_form)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(box_param_group)
        hbox.addWidget(vent_geom_group)

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

        self.minimum_vent_area = QtGui.QLabel(self)
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
        self.update_model_vent_area()

        driver_selection_form.addRow(driver_manuf_label, self.driver_manuf_box)
        driver_selection_form.addRow(driver_model_label, self.driver_model_box)
        driver_selection_form.addRow(self.minimum_vent_area)
        driver_selection.setLayout(driver_selection_form)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(driver_selection)
        self.setLayout(vbox)

    def find_radius(self, length):
        """ Find required vent radius for achieving given tuning """
        Mav = 1 / ((2*np.pi*self.current_box.fb)**2 * self.current_box.Cab)
        c = [-length*rho, -1.7*rho, Mav*np.pi]
        roots = np.polynomial.polynomial.polyroots(c)
        radius = roots[roots > 0][0]
        return radius

    def find_length(self, radius):
        """ Find required vent length for achieving given tuning """
        Mav = 1 / ((2*np.pi*self.current_box.fb)**2 * self.current_box.Cab)
        length = (np.pi*radius**2*Mav - 1.7*radius*rho)/rho
        return length

    def radius_changed(self, radius):
        """ When radius is changed, recompute area and length """
        vent_area = np.pi*radius**2
        self.vent_area_value.setText(u"{0:4g}mm²".format(vent_area))
        # convert to m
        length = self.find_length(1e-3*radius)
        self.vent_length_spinbox.setValue(1e3*length)

    def length_changed(self, length):
        """ When length is changed, recompute area and radius """
        radius = self.find_radius(1e-3*length)
        vent_area = np.pi*(1e3*radius)**2
        self.vent_area_value.setText(u"{0:4g}mm²".format(vent_area))
        self.vent_radius_spinbox.setValue(1e3*radius)

    def change_box_size(self, Vab):
        """ When box volume is changed, recompute length """
        self.current_box.Vab = 1e-3*Vab
        radius = self.vent_radius_spinbox.value()
        length = self.find_length(1e-3*radius)
        self.vent_length_spinbox.setValue(1e3*length)

    def change_box_fb(self, fb):
        """ When box tuning is changed, recompute length and minimum vent area"""
        self.current_box.fb = fb
        radius = self.vent_radius_spinbox.value()
        length = self.find_length(1e-3*radius)
        self.vent_length_spinbox.setValue(1e3*length)
        self.update_model_vent_area()

    def set_manufacturer(self, index):
        """ Change manufacturer and update driver models"""
        self.current_manuf = self.driver_manuf_box.itemText(index)
        self.update_model_box()

    def set_model(self, index):
        """ Change driver and update response plot"""
        self.current_model = self.driver_model_box.itemText(index)
        for driver in driver_db:
            if ((self.current_model == driver.model)
                    and (self.current_manuf == driver.manufacturer)):
                self.current_driver = driver
        self.update_model_vent_area()

    def update_model_box(self):
        """ Clear model list and add all models of current manufacturer"""
        self.driver_model_box.clear()
        for driver in driver_db:
            if driver.manufacturer == self.current_manuf:
                self.driver_model_box.addItem(driver.model)

    def update_model_vent_area(self):
        """ Update the minimum vent area required """
        driver = self.current_driver
        Vd = driver.Sd * driver.xmax
        Sp_min = 1e6*0.8*self.current_box.fb*Vd
        label = (u"With the {0} {1},\n"
                 u"in an enclosure tuned to {2}Hz,\n"
                 u"the vent area should be at least {3:3g}mm²\n"
                 u"to prevent large losses or excessive vent noise."
                 "".format(driver.manufacturer, driver.model,
                           self.current_box.fb, Sp_min))
        self.minimum_vent_area.setText(label)
