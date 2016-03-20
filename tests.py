"""Unit tests for Altai."""
import unittest
import filecmp
import os
import driver_database
import vented_box
from speaker import VentedSpeaker


class DriverDataBaseTest(unittest.TestCase):
    """Testing the driver database."""

    def test_load_and_write_db(self):
        """Testing the loading and writing of the DB to/from JSON."""
        driver_db = driver_database.DriverDB.from_file('driver_db.json')
        driver_db.write_to_disk('test.json')
        self.assertTrue(filecmp.cmp('driver_db.json', 'test.json'))
        os.remove('test.json')

class SpeakerComputationTests(unittest.TestCase):

    def test_cutoff_calculation(self):
        driver_db = driver_database.DriverDB.from_file('driver_db.json')
        driver = driver_db[0]
        box = vented_box.VentedBox(Vab=90.0, fb=43.0, Ql=20.0)
        speaker = VentedSpeaker(driver, box)
        self.assertAlmostEqual(speaker.f_3(), 36.9606852)

if __name__ == '__main__':
    unittest.main()
