# -*- coding: utf-8 -*-
"""Collecting multiple drivers in a database."""
import json
from driver import Driver


class DriverDB(list):
    """Representing the database (inherits from ``list``)."""

    def __init__(self):
        """Create an empty database.

        Take a look at ``from_file`` for loading an existing database file.
        """
        list.__init__(self)
        self.manufacturers = set()

    def load_from_disk(self, filename):
        """Load a database from file.

        Args:
            filename : file to load database from
        """
        self.clear()
        self.manufacturers.clear()
        with open(filename, 'r') as f:
            driver_list = json.load(f)
        for entry in driver_list:
            driver = Driver.from_dict(entry)
            self.manufacturers.add(driver.manufacturer)
            self.append(driver)

    def write_to_disk(self, filename):
        """Write database to disk.

        Args:
            filename : file in which to store database
        """
        driver_list = []
        for driver in self:
            driver_list.append(driver.dict_representation())
        with open(filename, 'w') as f:
            json.dump(driver_list, f, indent=4, sort_keys=True)

    @classmethod
    def from_file(cls, filename):
        """Create a new database from existing file.

        Args:
            filename : file from which to initialize database
        Example:
            >>> mydatabase = DriverDB.from_file("mypersonaldb.json")
        """
        driver_db = cls()
        driver_db.load_from_disk(filename)
        return driver_db
