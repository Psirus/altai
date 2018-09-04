"""Unit tests for Altai."""
import unittest
import filecmp
import os

import context
from altai.lib import driver_database, vented_box, speaker

class DriverDataBaseTest(unittest.TestCase):
    """Testing the driver database."""

    def test_load_and_write_db(self):
        """Testing the loading and writing of the DB to/from JSON."""
        driver_db = driver_database.DriverDB.from_file(context.database_file)
        driver_db.write_to_disk('test.json')
        self.assertTrue(filecmp.cmp(context.database_file, 'test.json'))
        os.remove('test.json')

class SpeakerComputationTests(unittest.TestCase):

    def test_cutoff_calculation(self):
        driver_db = driver_database.DriverDB.from_file(context.database_file)
        driver = driver_db[0]
        box = vented_box.VentedBox(Vab=0.09, fb=43.0, Ql=20.0)
        ls = speaker.VentedSpeaker(driver, box)
        self.assertAlmostEqual(ls.f_3(), 39.28176248051)

if __name__ == '__main__':
    unittest.main()
