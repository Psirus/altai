"""Unit tests for Altai."""
import unittest
import filecmp
import os
import driver_database


class DriverDataBaseTest(unittest.TestCase):
    """Testing the driver database."""

    def test_load_and_write_db(self):
        """Testing the loading and writing of the DB to/from JSON."""
        driver_db = driver_database.DriverDB.from_file('driver_db.ddb')
        driver_db.write_to_disk('test.ddb')
        self.assertTrue(filecmp.cmp('driver_db.ddb', 'test.ddb'))
        os.remove('test.ddb')

if __name__ == '__main__':
    unittest.main()
