# -*- coding: utf-8 -*-
""" Loading/saving of driver database, adding new drivers and displaying the
database in a table"""
import json
from driver import Driver


class DriverDB(list):

    def __init__(self):
        list.__init__(self)
        self.manufacturers = set()

    def load_from_disk(self, filename):
        self.clear()
        self.manufacturers.clear()
        with open(filename, 'r') as f:
            driver_list = json.load(f)
        for entry in driver_list:
            driver = Driver.from_dict(entry)
            self.manufacturers.add(driver.manufacturer)
            self.append(driver)

    def write_to_disk(self, filename):
        driver_list = []
        for driver in self:
            driver_list.append(driver.dict_representation())
        with open(filename, 'w') as f:
            json.dump(driver_list, f, indent=4, sort_keys=True)

    @classmethod
    def from_file(cls, filename):
        driver_db = cls()
        driver_db.load_from_disk(filename)
        return driver_db
