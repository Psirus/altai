"""Unit tests for Altai."""
import unittest
import filecmp
import os
import driver_database


class DriverDataBaseTest(unittest.TestCase):
    """Testing the driver database."""

    def test_load_and_write_db(self):
        """Testing the loading and writing of the DB to/from JSON."""
        driver_db = driver_database.DriverDB.from_file('driver_db.json')
        driver_db.write_to_disk('test.json')
        self.assertTrue(filecmp.cmp('driver_db.json', 'test.json'))
        os.remove('test.json')

if __name__ == '__main__':
    unittest.main()
